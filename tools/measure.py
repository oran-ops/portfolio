# -*- coding: utf-8 -*-
"""Measure landmarks on an image of the machine, in pixels, with no eyeballing anywhere.

Every previous pass read the reference by looking at it, and every reading was wrong by enough
to matter - two readings of the screen's aspect off the same picture disagreed by 30%. This
finds edges by looking at where the image actually changes.

The routines are deliberately generic so the SAME code measures the reference and our render.
A metric that is computed differently for the two things it compares is not a comparison.
"""
import sys

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8', errors='replace')


def load(path):
    a = np.asarray(Image.open(path).convert('RGB'), dtype=np.float64) / 255.0
    return a, a.mean(axis=2)


def dark_blob(lum, thresh, box=None):
    """Bounding box of the darkest connected mass - the CRT is far darker than anything else."""
    m = lum < thresh
    if box:
        x0, y0, x1, y1 = box
        keep = np.zeros_like(m)
        keep[y0:y1, x0:x1] = True
        m = m & keep
    ys, xs = np.nonzero(m)
    if len(xs) == 0:
        return None
    # the largest run, not scattered noise: keep the rows/cols that carry most of the mass
    colsum = m.sum(axis=0)
    rowsum = m.sum(axis=1)
    cx = np.nonzero(colsum > colsum.max() * 0.25)[0]
    cy = np.nonzero(rowsum > rowsum.max() * 0.25)[0]
    return int(cx[0]), int(cy[0]), int(cx[-1]), int(cy[-1])


def edge_in_row(lum, y, x_from, x_to, step, grad_min=0.012):
    """First strong horizontal change along a row, walking from x_from toward x_to."""
    row = lum[y]
    x = x_from
    while (x_to - x) * step > 0:
        if abs(row[x + step] - row[x]) > grad_min:
            return x + (step > 0)
        x += step
    return None


def edge_in_col(lum, x, y_from, y_to, step, grad_min=0.012):
    col = lum[:, x]
    y = y_from
    while (y_to - y) * step > 0:
        if abs(col[y + step] - col[y]) > grad_min:
            return y + (step > 0)
        y += step
    return None


def silhouette(lum, box, bg_tol=0.010):
    """Outline against a smooth background: a pixel belongs to the object when it differs from
    the local background estimate, which is taken from the image's own margins so it works on
    the reference's grey gradient and on our flat charcoal alike."""
    x0, y0, x1, y1 = box
    sub = lum[y0:y1, x0:x1]
    # background model: median of the outer 6% frame of the crop
    f = max(4, int(0.06 * min(sub.shape)))
    ring = np.concatenate([sub[:f].ravel(), sub[-f:].ravel(),
                           sub[:, :f].ravel(), sub[:, -f:].ravel()])
    bg = np.median(ring)
    mask = np.abs(sub - bg) > bg_tol
    return mask, bg


def span_row(mask, y):
    xs = np.nonzero(mask[y])[0]
    return (int(xs[0]), int(xs[-1])) if len(xs) else None


def span_col(mask, x):
    ys = np.nonzero(mask[:, x])[0]
    return (int(ys[0]), int(ys[-1])) if len(ys) else None
