# -*- coding: utf-8 -*-
"""
Functions and classes to handle image cropping
"""


def crop_image(cv2_mat, coords, as_css=False):
    """Return a rectangular section of the image received,
    (cv2_mat), using (coords).

    Return value is a numpy array

    If (as_css) is True,
       coords (left, up, right, bottom)
       are float values in [0, 100] interpreted as
       css padding property:

        +-----------------------------------------------+
        |                                               |
        |                             20%               |
        |                                               |
        |                       +--------------+        |
        |          50%          |              |  20%   |
        |                       |              |        |
        |                       |              |        |
        |                       |              |        |
        |                       |              |        |
        |                       +--------------+        |
        |                                               |
        |                                               |
        |                                               |
        |                             40%               |
        |                                               |
        |                                               |
        +-----------------------------------------------+

    If (as_css) is False (default value),
        coords (x1, y1, x2, y2) are pixel numbers
        of the upper-left and bottom-down coords,
        respectively. No index check is performed, so
        this function may rise IndexError.

        +-----------------------------------------------+
        |                                               |
        |                                               |
        |                                               |
        |              (x1, y1) +--------------+        |
        |                       |              |        |
        |                       |              |        |
        |                       |              |        |
        |                       |              |        |
        |                       |              |        |
        |                       +--------------+        |
        |                                   (x2, y2)    |
        |                                               |
        |                                               |
        |                                               |
        |                                               |
        |                                               |
        +-----------------------------------------------+
    """

    h, w = cv2_mat.shape[:2]

    # these coords are pixels
    x1, y1, x2, y2 = coords

    if as_css:
        # compute pixel number
        x1 = int(round(x1/w * 100))
        x2 = int(round(x2/w * 100))
        y1 = int(round(y1/h * 100))
        y2 = int(round(y2/h * 100))

    return cv2_mat.copy()[y1:y2, x1:x2]

