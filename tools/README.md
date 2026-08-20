# The measuring kit

Built while getting page 4's machine to match its reference. Every element after it — the
floppy, the sticky note, the scene — needs the same instruments, so they live here rather than
in a scratch directory.

The reason they exist: three builds of the machine were made by constructing the whole object
and adjusting it by eye, and all three were rejected. The fourth measured one quantity at a
time and found errors of 13 to 38 per cent that eye-adjustment never had.

| file | what it does |
| --- | --- |
| `measure.py` | loading, silhouettes against a smooth background, edge finding by gradient |
| `homog.py` | the homography from the machine's front-face plane to `ref/ref.jpg`, and back |
| `cal.py` | the linear calibration, kept for the record — superseded by the homography |
| `cmp.py` | silhouette comparison: bounding boxes, normalised overlap, aspect |
| `overlay.py` | draws the model's own parameters onto the reference through the homography |
| `side.py` | the two machines side by side at matched size |
| `compare.py` | builds `lab/compare.html` from the images above |
| `serve.py` | serves the repo AND accepts a rendered frame back by POST |

## The two rules that made the difference

**Fit a homography, not a scale factor.** A plane seen in perspective does not have one
pixels-per-inch. A single foreshortening factor kept contradicting itself — the case measured
9.6 inches wide from one pair of landmarks and 10.3 from another. The homography is exactly the
map perspective applies, so it dissolves the contradiction instead of averaging it. Anchor it on
something whose true size is known exactly, then check it against a quantity that took no part
in the fit.

**Run the same code over both pictures.** `serve.py` exists so the render can come back as a
file and go through the identical measurement path as the reference. A metric computed one way
for one image and another way for the other is not a comparison.

And one warning, learned the hard way: before optimising a number, check that it measures what
you think. Silhouette overlap here sat at 0.85 across five builds and looked like a stubborn
shape error; it turned out to depend almost entirely on how the *reference* was thresholded,
because the reference carries a soft contact shadow.

## Running them

`serve.py` on port 8732, open `lab/machine.html` from it, then from the page console:

    await window.__cam(yaw, pitch, dist, fov)
    await window.__shot('mine.png')
    await window.__sweep([[yaw, pitch, dist, fov, 'name.png'], ...])
