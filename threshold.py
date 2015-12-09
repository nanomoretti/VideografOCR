# -*- coding: utf-8 -*-
# pylint: disable=unused-argument
"""
python implementation of the kind of funcitionality found in
c++/Threshold.cpp
"""

import os
import cv2

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
        self.img_index = 0

        self.thr = None
        self.max_val = 127

        self.cropping = False
        self.mouse_handler = MouseCropCallback()


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
            self.cropping = False


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
        while True:
            current_image = self.images[self.img_index].copy()
            if self.thr > 0:
                thr_type = self.THR_TYPES[self.thr][1]
                _, current_image = cv2.threshold(current_image,
                                                 self.max_val,
                                                 255,
                                                 thr_type)
            if self.mouse_handler.drawing or self.cropping:
                self.cropping = True
                cv2.rectangle(current_image,
                              self.mouse_handler.upper_left,
                              self.mouse_handler.bottom_right,
                              (0, 255, 0), 1)
            cv2.imshow(self.window_name, current_image)
            key = cv2.waitKey(self._LOOPTIME) & 0xFF
            if key != 255:
                self.handle_key(key)

    @staticmethod
    def quit():
        """Clean-up and end loop"""
        print 'Chau!'
        exit(0)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(os.path.basename(__file__))
    MainWindow().loop()


