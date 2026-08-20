# -*- coding: utf-8 -*-
"""Build lab/compare.html - the evidence, so the match can be judged rather than asserted.

Three things, in the order that settles the question:

  1. the two machines side by side at the same camera and the same size
  2. the model's own numbers pushed through the homography and drawn on the reference - the
     check with no camera to solve and no lens to argue about
  3. the measurements themselves, and what each one corrected

Self-contained: the images are inlined, so the page makes no request.
"""
import base64
import io
import os
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = r'C:\Users\Alex\Desktop\Oran_Personal_Brand\portfolio-repo\lab\compare.html'


def b64(name, maxw=1500):
    from PIL import Image
    im = Image.open(os.path.join(HERE, name)).convert('RGB')
    if im.width > maxw:
        im = im.resize((maxw, int(im.height * maxw / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, 'JPEG', quality=88, optimize=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()


ROWS = [
    ('well opening, half', '0.402 x 0.284', '0.455 x 0.326', '13% narrow, 15% short'),
    ('tube surround, half', '0.378 x 0.258', '0.395 x 0.292', '12% short'),
    ('screen centre', '0, +0.245', '+0.0531, +0.2309', 'it is not centred on the face'),
    ('face height', '1.253', '1.2875', ''),
    ('face bottom', '-0.398', '-0.578', 'the base was a storey, not a foot'),
    ('slot width, half', '0.186', '0.2573', '38% narrow'),
    ('rear height', '79% of front', '94.8%', 'the roof was a cliff'),
    ('case depth', '1.12', '1.05', ''),
    ('well depth', '0.06', '0.11', 'the screen is deeply sunk'),
    ('flank brightness', '0.25 of the face', '0.65', 'the loudest error, and it was light'),
]
trs = ''.join('<tr><td>%s</td><td class=old>%s</td><td class=new>%s</td><td class=note>%s</td></tr>'
              % r for r in ROWS)

HTML = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="dark">
<title>The machine &mdash; measured against the reference</title>
<style>
 :root{--bg:#191A1F;--card:#22242A;--hair:#31333A;--ink:#F2F1ED;--dim:#8A8C92;--em:#2FB380}
 *{box-sizing:border-box}
 html,body{margin:0;background:var(--bg);color:var(--ink);
   font:14px/1.65 ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif}
 .w{max-width:1180px;margin:0 auto;padding:46px 22px 90px}
 h1{font:600 21px/1.3 ui-sans-serif,system-ui,sans-serif;margin:0 0 6px}
 h2{font:600 15px/1.3 ui-sans-serif,system-ui,sans-serif;margin:44px 0 6px}
 p{color:var(--dim);margin:0 0 16px;max-width:74ch}
 img{width:100%;display:block;border-radius:3px;border:1px solid var(--hair)}
 code{font:12.5px ui-monospace,Menlo,Consolas,monospace;color:#C8CBD2}
 table{border-collapse:collapse;width:100%;margin-top:12px;font-size:13px}
 th,td{text-align:left;padding:7px 10px;border-bottom:1px solid var(--hair)}
 th{color:var(--dim);font-weight:600;font-size:12px;letter-spacing:.04em;text-transform:uppercase}
 td.old{color:#9A6B6B} td.new{color:var(--em)} td.note{color:var(--dim)}
 .k{color:var(--em)}
</style></head><body><div class="w">

<h1>The machine, measured against the reference</h1>
<p>Three builds were adjusted by eye and none of them was close. This one measures one quantity
at a time, checks the model against it, and only then moves on. What follows is the evidence
rather than the claim.</p>

<h2>1 &nbsp; The two, at the same camera and the same size</h2>
<p>Ours is rendered at the viewpoint solved from the reference itself: turned 38&deg;, almost
level with the machine, through a long lens.</p>
<img src="__SIDE__" alt="reference and ours side by side">

<h2>2 &nbsp; The model's own numbers, drawn on the reference</h2>
<p>This is the check that cannot be argued with. A homography is the exact map from the face
plane to the photograph, fitted on the CRT's active area &mdash; the one rectangle whose true
size is known to the millimetre, <code>512 &times; 342 at 72 dpi = 7.111 &times; 4.750 in</code>.
Push the model's parameters through it and the rectangles either land on the reference's
features or they do not. No camera to solve, no silhouette to confound with lens choice.</p>
<p><span class="k">cyan</span> glass &middot; <span class="k">yellow</span> tube surround &middot;
<span class="k">red</span> well opening &middot; <span class="k">green</span> face outline &middot;
<span class="k">magenta</span> slot &middot; <span class="k">white</span> logo</p>
<img src="__OVER__" alt="model layout drawn on the reference">

<h2>3 &nbsp; What the measurements corrected</h2>
<p>Model units; one unit is ten inches.</p>
<table><tr><th>parameter</th><th>build 3</th><th>measured</th><th></th></tr>__ROWS__</table>

<h2>Two that were solved rather than tried</h2>
<p>The silhouette's aspect is <code>(W cos t + D sin t) / H</code>, whose maximum over every
possible viewing angle is <code>sqrt(W&sup2; + D&sup2;) / H</code>. With build 3's numbers that
ceiling was <span class="k">1.029</span> &mdash; below the reference's measured
<span class="k">1.044</span> &mdash; so no camera could ever have matched it, and sweeping the
camera to find one was wasted effort.</p>
<p>A recess of depth <code>d</code> drafted inward by <code>s</code> shows a wall about
<code>d&nbsp;sin&nbsp;38 + s&nbsp;cos&nbsp;38</code> wide. The reference's measures 0.906&nbsp;in,
which lands on <code>d&nbsp;=&nbsp;0.11, s&nbsp;=&nbsp;0.030</code> &mdash; after guessing twice
and getting first a wall too narrow to see, then a funnel.</p>

<h2>And one instrument that lied</h2>
<p>Silhouette overlap sat at 0.85&ndash;0.87 across five builds and would not move, which read as
a stubborn shape error. Sweeping the threshold showed the score depends almost entirely on how
the <em>reference</em> is thresholded &mdash; 0.872 at 0.012, 0.775 at 0.045 &mdash; because the
reference carries a soft contact shadow that a low threshold swallows. The uniform band the
difference map kept showing was that shadow being clipped, not our model being fat. Before
optimising a number, check that it measures the thing you think it measures.</p>

</div></body></html>
"""

html = (HTML.replace('__SIDE__', b64('side.png'))
            .replace('__OVER__', b64('overlay.png', 1400))
            .replace('__ROWS__', trs))
io.open(OUT, 'w', encoding='utf-8', newline='').write(html)
print('wrote %s  (%d KB)' % (OUT, len(html.encode('utf-8')) // 1024))
