# -*- coding: utf-8 -*-
"""A homography from the machine's FRONT-FACE PLANE to ref.png, and back.

Why a homography and not a scale factor. The face is turned about 36 degrees and photographed
with a real lens, so pixels-per-inch is not constant across it: the left edge is nearer the
camera than the right and is magnified accordingly. Every earlier reading assumed a single
foreshortening factor, and it kept producing contradictions - the case measured 9.6 inches
wide from one pair of landmarks and 10.3 from another. A homography is exactly the map a plane
undergoes under perspective, so it removes the contradiction instead of averaging it.

It is anchored on the CRT's active area, which is the one rectangle on the machine whose true
size is known to the millimetre: 512 x 342 pixels at 72 dpi is 7.111 x 4.750 inches.

Face coordinates are inches, x right and y UP, origin at the centre of the glass.
"""
import numpy as np

# Glass edges, each fitted from many samples rather than read at a corner (see measure.py).
#   top    y = 300 + 0.0667 (x - 880)
#   bottom y = 469 - 0.1417 (x - 880)
#   left   x = 826 - 0.0500 (y - 340)
#   right  x = 1030 - 0.0500 (y - 340)
GLASS_W, GLASS_H = 7.1111, 4.7500


def _isect(a, b):
    """intersect y = a0 + a1(x - a2)  with  x = b0 + b1(y - b2)"""
    a0, a1, a2 = a
    b0, b1, b2 = b
    y = (a0 + a1 * (b0 - b1 * b2 - a2)) / (1.0 - a1 * b1)
    x = b0 + b1 * (y - b2)
    return x, y


# Refit sub-pixel from the midpoint crossing between the surround's 0.19 and the content's
# 0.58, over 23-26 samples per edge. Residuals: top 0.08 px, bottom 0.09, right 0.30, left
# 3.02 (the left edge carries MacPaint's tool palette, which is not a clean step).
#   left   x = -0.01089 y +  820.74
#   right  x = -0.05868 y + 1048.99
#   top    y = +0.05459 x +  252.15
#   bottom y = +0.10478 x +  375.55
# The right edge of the glass is the TALLER one, which places the camera to the right of the
# face's normal - the same side the case recedes towards, and the reason the well's right-hand
# wall is not visible in the image at all.
CORNERS = np.array([[819.28, 296.87], [1030.89, 308.43],
                    [1020.68, 482.50], [ 813.52, 460.79]], dtype=float)

FACE = np.array([[-GLASS_W / 2,  GLASS_H / 2],
                 [ GLASS_W / 2,  GLASS_H / 2],
                 [ GLASS_W / 2, -GLASS_H / 2],
                 [-GLASS_W / 2, -GLASS_H / 2]], dtype=float)


def solve(src, dst):
    """the 3x3 taking src (N x 2) to dst (N x 2), up to scale"""
    A = []
    for (u, v), (x, y) in zip(src, dst):
        A.append([u, v, 1, 0, 0, 0, -x * u, -x * v, -x])
        A.append([0, 0, 0, u, v, 1, -y * u, -y * v, -y])
    _, _, Vt = np.linalg.svd(np.asarray(A, dtype=float))
    return (Vt[-1] / Vt[-1][-1]).reshape(3, 3)


H = solve(FACE, CORNERS)        # inches -> pixels
Hinv = np.linalg.inv(H)


def to_px(u, v):
    p = H @ np.array([u, v, 1.0])
    return p[0] / p[2], p[1] / p[2]


def to_in(x, y):
    p = Hinv @ np.array([x, y, 1.0])
    return p[0] / p[2], p[1] / p[2]
