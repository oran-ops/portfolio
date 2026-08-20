import sys
sys.stdout.reconfigure(encoding='utf-8',errors='replace')
from PIL import Image, ImageDraw
sys.path.insert(0,'.')
from cmp import sil, bbox
mine_f = sys.argv[1] if len(sys.argv)>1 else 'r_fit.png'
ref=Image.open('ref.png').convert('RGB')
mine=Image.open(mine_f).convert('RGB').resize((1920,1080), Image.LANCZOS)
R=sil('ref.png',(745,205,1265,715),tol=0.012); rb=bbox(R)
M=sil(mine_f,(20,20,1900,1060),tol=0.012,size=(1920,1080)); mb=bbox(M)
rc=ref.crop((745+rb[0]-25,205+rb[1]-25,745+rb[2]+25,205+rb[3]+25))
mc=mine.crop((20+mb[0]-25,20+mb[1]-25,20+mb[2]+25,20+mb[3]+25))
H=780
rc=rc.resize((int(rc.width*H/rc.height),H), Image.LANCZOS)
mc=mc.resize((int(mc.width*H/mc.height),H), Image.LANCZOS)
out=Image.new('RGB',(rc.width+mc.width+24,H+40),(200,196,188))
out.paste(rc,(0,40)); out.paste(mc,(rc.width+24,40))
d=ImageDraw.Draw(out)
d.text((8,14),'REFERENCE',fill=(30,30,30)); d.text((rc.width+32,14),'OURS',fill=(30,30,30))
out.save('side.png'); print('side.png', out.size)
