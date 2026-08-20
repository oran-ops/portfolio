# -*- coding: utf-8 -*-
"""Draw the MODEL's front-face layout onto the reference photograph, through the homography.

This is the check that cannot be argued with. The homography is the exact map from the face
plane to the image, fitted on a rectangle whose true size is known. Push the model's own
numbers through it and the rectangles either land on the reference's features or they do not -
no camera to solve, no silhouette to confound with lens choice, no eyeballing.

Model units are tenths of an inch and the origin is the centre of the CASE; the homography's
origin is the centre of the GLASS, so the two differ by the glass's height above the case
centre, which is the only constant that has to be carried.
"""
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, '.')
from homog import to_px

# --- the model, exactly as lab/machine.html builds it ------------------------
SCR_Y = 0.2309          # centre of the well and everything in it, in case-centre units
SCR_X = 0.0531
PARTS = [
    ('glass',          SCR_X,   SCR_Y,  0.3555, 0.2375, (0, 255, 255)),
    ('tube surround',  SCR_X,   SCR_Y,  0.395,  0.2920, (255, 210, 0)),
    ('well opening',   0.0,     0.2289, 0.431,  0.3256, (255, 60, 60)),
    ('bezel outline',  0.0,     0.0313, 0.5008, 0.6437, (60, 255, 60)),
    ('slot opening',   0.100,  -0.2809, 0.2573, 0.0348, (255, 120, 255)),
    ('logo',          -0.4007, -0.3654, 0.025,  0.032,  (255, 255, 255)),
]


def px(u_units, v_units):
    """model units (case centre) -> image pixels, via inches from the GLASS centre"""
    return to_px((u_units - SCR_X) * 10.0, (v_units - SCR_Y) * 10.0)


def rect(d, cx, cy, hx, hy, col, w=2):
    pts = [px(cx - hx, cy + hy), px(cx + hx, cy + hy),
           px(cx + hx, cy - hy), px(cx - hx, cy - hy)]
    d.line(pts + [pts[0]], fill=col, width=w)


if __name__ == '__main__':
    im = Image.open('ref.png').convert('RGB')
    d = ImageDraw.Draw(im)
    for name, cx, cy, hx, hy, col in PARTS:
        rect(d, cx, cy, hx, hy, col)
    im.save('overlay.png')
    print('overlay.png written')
    for name, cx, cy, hx, hy, col in PARTS:
        a = px(cx - hx, cy + hy)
        b = px(cx + hx, cy - hy)
        print('  %-15s px  x %7.1f .. %7.1f    y %7.1f .. %7.1f' % (name, a[0], b[0], a[1], b[1]))
