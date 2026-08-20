# -*- coding: utf-8 -*-
"""The calibration for ref.png, and the conversion both ways.

SOLVED, NOT GUESSED. Two unknowns - the vertical scale and the horizontal foreshortening of
the three-quarter view - and two knowns to pin them: the case is 9.7 x 13.5 inches in
elevation, and it measures 273 x 482 px.

    PPI_V = 482 / 13.5 = 35.7 px per inch vertically
    PPI_H = 273 /  9.7 = 28.1 px per true inch horizontally
    FS    = 28.1 / 35.7 = 0.787          ->  the face is turned about 38 degrees

The check is a quantity that took no part in the fit: the CRT's active area is 512 x 342 at
72 dpi, so 7.11 x 4.75 inches. Measured on the image it is 199 x 170 px, which converts to

    199 / 28.1 = 7.08 in      170 / 35.7 = 4.76 in

against 7.11 and 4.75. Better than half a percent on both axes, from a fit that never saw
them. The calibration is right, and an earlier reading of 0.914 for FS was wrong because it
measured the screen's height as 157 px instead of 170.
"""
PPI_V = 35.70
FS = 0.787
PPI_H = PPI_V * FS          # 28.10 px per true inch across the face

# where the machine sits in ref.png
FACE_L, FACE_R = 772.0, 1045.0     # the front face, left and right, at mid height
TOP_FL = 218.0                     # top of the case at the front-left corner
BOTTOM = 700.0                     # the floor line under the case


def in_x(px):
    """a horizontal pixel distance, in true inches"""
    return px / PPI_H


def in_y(px):
    return px / PPI_V


def u_x(px):
    """...and in model units, where 1 unit = 10 inches"""
    return in_x(px) / 10.0


def u_y(px):
    return in_y(px) / 10.0


def face_u(x, y):
    """an image point on the FRONT FACE, as model units relative to the case centre.
    x runs +right, y runs +up, both from the centre of the case."""
    cx = (FACE_L + FACE_R) / 2.0
    cy = (TOP_FL + BOTTOM) / 2.0
    return (u_x(x - cx), -u_y(y - cy))
