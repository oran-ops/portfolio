import sys, glob, numpy as np
sys.stdout.reconfigure(encoding='utf-8',errors='replace')
from PIL import Image
def sil(path, box, tol=0.020, size=None):
    im=Image.open(path).convert('RGB')
    if size: im=im.resize(size, Image.LANCZOS)
    lum=(np.asarray(im,dtype=np.float64)/255.0).mean(axis=2)
    x0,y0,x1,y1=box; sub=lum[y0:y1,x0:x1]
    f=max(4,int(0.05*min(sub.shape)))
    ring=np.concatenate([sub[:f].ravel(),sub[-f:].ravel(),sub[:,:f].ravel(),sub[:,-f:].ravel()])
    return np.abs(sub-np.median(ring))>tol
def bbox(m):
    ys,xs=np.nonzero(m); return int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())
def norm(m,n=180):
    b=bbox(m); x0,y0,x1,y1=b
    im=Image.fromarray((m[y0:y1+1,x0:x1+1]*255).astype(np.uint8))
    return (np.asarray(im.resize((n,n),Image.BILINEAR),dtype=np.float64)/255.0>0.5), b
def score(pattern):
    R=sil('ref.png',(745,205,1265,715)); A,rb=norm(R)
    ra=(rb[2]-rb[0])/(rb[3]-rb[1])
    print('reference aspect %.4f'%ra)
    print('%-20s %-8s %-9s %s'%('file','aspect','d-aspect','IoU'))
    rows=[]
    for f in sorted(glob.glob(pattern)):
        M=sil(f,(20,20,1900,1060),size=(1920,1080)); B,mb=norm(M)
        ma=(mb[2]-mb[0])/(mb[3]-mb[1]); iou=(A&B).sum()/(A|B).sum()
        rows.append((iou,ma,f))
        print('%-20s %-8.4f %+-9.4f %.4f'%(f.replace('.png',''),ma,ma-ra,iou))
    rows.sort(reverse=True)
    print('\nbest IoU: %s  %.4f  (aspect %.4f)'%(rows[0][2],rows[0][0],rows[0][1]))
    return rows
if __name__=='__main__': score(sys.argv[1] if len(sys.argv)>1 else 'f_*.png')
