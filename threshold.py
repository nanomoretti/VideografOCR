# -*- coding: utf-8 -*-
# pylint: disable=unused-argument
"""
python implementation of the kind of funcitionality found in
c++/Threshold.cpp
"""

import os
import cv2
import commands

from crops import crop_image

class MouseCropCallback(object):
    """A callback to handle mouse interactions and crop image"""

    def __init__(self):
        self.drawing = False
        self.crop_rect = None

    def __call__(self, event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.crop_start(x, y)
        elif event == cv2.EVENT_LBUTTONUP:
            self.crop_end(x, y)
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.drawing:
                self.crop_update(x, y)
        else:
            self.crop_rect = None

    def crop_start(self, x, y):
        """Record coords of initial selection point"""
        self.drawing = True
        self.crop_rect = [x, y, x, y]

    def crop_end(self, x, y):
        """Record coords of final selection point"""
        self.crop_update(x, y)
        self.drawing = False

    def crop_update(self, x, y):
        """Update final coords when cropping"""
        self.crop_rect[2] = x
        self.crop_rect[3] = y

    @property
    def upper_left(self):
        """upper left crop corner"""
        return tuple(min(self.crop_rect[:2], self.crop_rect[2:]))

    @property
    def bottom_right(self):
        """bottom right crop corner"""
        return tuple(max(self.crop_rect[:2], self.crop_rect[2:]))


class MainWindow(object):
    """The main window of the application"""

    _LOOPTIME = 30
    THR_TYPES = {
        0: ('', None),
        1: ('Binary', cv2.THRESH_BINARY),
        2: ('Binary Inverted', cv2.THRESH_BINARY_INV),
        3: ('Truncate', cv2.THRESH_TRUNC),
        4: ('To Zero', cv2.THRESH_TOZERO),
        5: ('To Zero Inverted', cv2.THRESH_TOZERO_INV),
    }

    def __init__(self):
        self.window_name = os.path.basename(__file__)

        self.images = ['c++/1.jpeg', 'c++/2.jpeg', 'c++/3.jpeg', 'c++/4.jpeg']
        self.current_image = None
        self.img_index = 0

        self.thr = None
        self.max_val = 127

        self._crop = None
        self.mouse_handler = MouseCropCallback()

    @property
    def crop(self):
        """Return coordinates of crop, making some checks"""
        result = None
        if self._crop:
            ul = self.mouse_handler.upper_left
            br = self.mouse_handler.bottom_right
            if ul[0] != br[0] and ul[1] != br[1]:
                result =  list(ul) + list(br)
        return result

    def thr_changed(self, thr, *args):
        """Function executed upon threshold type slider is changed"""
        self.thr = thr

    def max_val_changed(self, mv, *args):
        """Function executed upon max value slider is changed"""
        self.max_val = mv

    def handle_key(self, key):
        """Respond to user keyboard input"""
        if key in [ord('q'), ord('Q')]:
            self.quit()
        elif key in [ord('c'), ord('C')]:
            self.img_index = (self.img_index + 1) % len(self.images)
        elif key == 27: # <ESC>
            self._crop = None
        elif key in [ord('t'), ord('T')]:
            self.exec_tesseract()
        elif key in [ord('h'), ord('H')]:
            self.print_help()
        else:
            print 'Presione "h" para ver una lista de comandos'

    def exec_tesseract(self):
        """Call tesseract and show results"""
        if self.crop:
            # re-process image, just to get rid of crop rectangle...
            raw_image = self.images[self.img_index].copy()
            if self.thr:
                thr_type = self.THR_TYPES[self.thr][1]
                _, raw_image = cv2.threshold(raw_image,
                                             self.max_val,
                                             255,
                                             thr_type)
            roi = crop_image(raw_image, self.crop)
            cv2.imshow('ROI', roi)
            img_path = '/tmp/threshold_py.jpg'
            cv2.imwrite(img_path, roi)
            cmd = 'tesseract {} stdout -l spa'.format(img_path)
            status, output = commands.getstatusoutput(cmd)
            if status == 0:
                print '---------------------------------'
                print output
                print '---------------------------------'
            else:
                print 'problemas al ejecutar "{}"'.format(cmd)
        else:
            print 'no hay rectángulo seleccionado...'


    def loop(self):
        """main"""

        def read_image_grayscale(path):
            """Return image as grayscale"""
            im = cv2.imread(path)
            return cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

        # load images
        self.images = map(read_image_grayscale, self.images)

        # build gui
        cv2.namedWindow(self.window_name)
        cv2.setMouseCallback(self.window_name, self.mouse_handler)
        cv2.createTrackbar('Threshold type',
                           self.window_name,
                           0, len(self.THR_TYPES) - 1,
                           self.thr_changed)
        cv2.createTrackbar('Max Value',
                           self.window_name,
                           0, 255,
                           self.max_val_changed)

        last_crop = None

        while True:
            self.current_image = self.images[self.img_index].copy()

            # apply thresholding
            if self.thr > 0:
                thr_type = self.THR_TYPES[self.thr][1]
                _, self.current_image = cv2.threshold(self.current_image,
                                                      self.max_val,
                                                      255,
                                                      thr_type)
            # if drawing rectangle, update crop coordinates
            if self.mouse_handler.drawing:
                self._crop = self.mouse_handler.crop_rect

            # draw rectangle box
            if self.crop:
                self.current_image = cv2.cvtColor(self.current_image,
                                                  cv2.COLOR_GRAY2BGR)
                cv2.rectangle(self.current_image,
                              self.mouse_handler.upper_left,
                              self.mouse_handler.bottom_right,
                              (0, 255, 0), 1)

            cv2.imshow(self.window_name, self.current_image)
            key = cv2.waitKey(self._LOOPTIME) & 0xFF
            if key != 255:
                self.handle_key(key)

    @staticmethod
    def quit():
        """Clean-up and end loop"""
        print 'Chau!'
        exit(0)

    @staticmethod
    def print_help():
        """Show list of usefull commands"""
        print ('c:     Continuar, pasar a la siguiente imagen\n'
               't:     Tesseract, ejecutar tesseract con la región de interés\n'
               '<ESC>: Borrar rectángulo\n'
               'q:     Quit, salir\n')




if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(os.path.basename(__file__))
    MainWindow().loop()


