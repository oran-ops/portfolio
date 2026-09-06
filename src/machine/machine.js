

(function(){
  "use strict";
  var cv=document.getElementById('mach-gl');
  /* preserveDrawingBuffer so the frame can be read back and measured. It costs a copy per
     frame and is worth it: a render that cannot be measured can only be judged by looking,
     which is how three builds in a row came out not close. */
  var GLOPT={alpha:false,antialias:true,depth:true,preserveDrawingBuffer:true};
  var gl=cv.getContext('webgl',GLOPT)||cv.getContext('experimental-webgl',GLOPT);
  /* the lab's on-screen readout is not shipped; the assignments are kept because one of
     them is the no-WebGL message, and a page that cannot render should say so rather
     than throw on the way to saying so. */
  var read=document.getElementById('read')||{};
  if(!gl){read.textContent='no webgl';return}

/* ---------------------------------------------------------------- primitives
   Three of them, and every part of the machine is one of the three.

   All rounding is the Minkowski sum of a shape with a sphere: take any point on the
   un-rounded surface, clamp it into the inner shape, then push back out along the difference
   by the radius. Flat faces stay flat, edges become exact cylinders, corners exact spheres,
   and the normal is the same difference vector. It is a construction, not an approximation. */

function meshOut(P,Nm,I){
  return {pos:new Float32Array(P), nrm:new Float32Array(Nm), idx:new Uint16Array(I),
          n:I.length};
}

/* ---- 1. rounded box --------------------------------------------------- */
function roundedBox(a,b,c,r,N){
  var P=[],Nm=[],I=[],idx=0, ia=a-r, ib=b-r, ic=c-r;
  function cl(v,m){ return v<-m?-m:(v>m?m:v) }
  function emit(x,y,z){
    var cx=cl(x,ia), cy=cl(y,ib), cz=cl(z,ic);
    var dx=x-cx, dy=y-cy, dz=z-cz, L=Math.sqrt(dx*dx+dy*dy+dz*dz);
    if(L<1e-9){dx=0;dy=0;dz=1;L=1}
    dx/=L;dy/=L;dz/=L;
    P.push(cx+dx*r, cy+dy*r, cz+dz*r); Nm.push(dx,dy,dz); return idx++;
  }
  /* sin(t*pi/2) bunches samples toward the edges, where the curvature is. A uniform grid
     spends its vertices in the middle of flat faces, where they do nothing. */
  var S=function(t){ return Math.sin(t*Math.PI/2) }, ext=[a,b,c];
  var faces=[[0,1,2,1],[0,1,2,-1],[1,2,0,1],[1,2,0,-1],[2,0,1,1],[2,0,1,-1]];
  for(var f=0;f<6;f++){
    var au=faces[f][0], av=faces[f][1], aw=faces[f][2], s=faces[f][3], st=idx, i, j;
    for(i=0;i<=N;i++)for(j=0;j<=N;j++){
      var p=[0,0,0];
      p[au]=S(-1+2*i/N)*ext[au]; p[av]=S(-1+2*j/N)*ext[av]; p[aw]=s*ext[aw];
      emit(p[0],p[1],p[2]);
    }
    for(i=0;i<N;i++)for(j=0;j<N;j++){
      var A=st+i*(N+1)+j, B=A+1, C=A+(N+1), D=C+1;
      if(s>0) I.push(A,C,B, B,C,D); else I.push(A,B,C, B,D,C);
    }
  }
  return meshOut(P,Nm,I);
}

/* ---- 2. rounded profile extrusion ------------------------------------- */
function roundProfile(prof,R,SEG){
  var out=[], n=prof.length, i, k;
  for(i=0;i<n;i++){
    var p=prof[(i-1+n)%n], v=prof[i], q=prof[(i+1)%n];
    var d0=[v[0]-p[0], v[1]-p[1]], l0=Math.hypot(d0[0],d0[1]);
    var d1=[q[0]-v[0], q[1]-v[1]], l1=Math.hypot(d1[0],d1[1]);
    d0=[d0[0]/l0,d0[1]/l0]; d1=[d1[0]/l1,d1[1]/l1];
    var turn=Math.atan2(d0[0]*d1[1]-d0[1]*d1[0], d0[0]*d1[0]+d0[1]*d1[1]);
    if(Math.abs(turn)<0.02){ out.push([v[0],v[1]]); continue }
    var t=Math.min(R*Math.abs(Math.tan(turn/2)), 0.45*Math.min(l0,l1));
    var rr=t/Math.abs(Math.tan(turn/2)), s=turn>0?1:-1;
    var A=[v[0]-d0[0]*t, v[1]-d0[1]*t];
    var C=[A[0]-s*d0[1]*rr, A[1]+s*d0[0]*rr];
    var a0=Math.atan2(A[1]-C[1], A[0]-C[0]);
    for(k=0;k<=SEG;k++){
      var ang=a0+turn*(k/SEG);
      out.push([C[0]+rr*Math.cos(ang), C[1]+rr*Math.sin(ang)]);
    }
  }
  return out;
}
function extrudeRounded(profRaw,hw,r,NB,R2,SEG){
  var prof=roundProfile(profRaw,R2,SEG);
  var P=[],Nm=[],I=[],idx=0, n=prof.length, i, k, ix=hw-r;
  function push(x,y,z,nx,ny,nz){P.push(x,y,z);Nm.push(nx,ny,nz);return idx++}
  var en=[];
  for(i=0;i<n;i++){
    var a=prof[i], b=prof[(i+1)%n], dz=b[0]-a[0], dy=b[1]-a[1], L=Math.hypot(dz,dy);
    en.push(L<1e-9 ? (en.length?en[en.length-1]:[1,0]) : [dy/L,-dz/L]);
  }
  /* per-VERTEX normals: on a straight run the two edges are collinear so the average is
     exact, on a fillet it is the true arc normal, and sharing them closes every seam */
  var vn=[];
  for(i=0;i<n;i++){
    var e0=en[(i-1+n)%n], e1=en[i], nz=e0[0]+e1[0], ny=e0[1]+e1[1], L2=Math.hypot(nz,ny);
    vn.push(L2<1e-9?[e1[0],e1[1]]:[nz/L2, ny/L2]);
  }
  var bl=[], br=[];
  for(i=0;i<n;i++){
    var a2=prof[i], e2=vn[i];
    bl.push(push(-ix, a2[1]+r*e2[1], a2[0]+r*e2[0], 0, e2[1], e2[0]));
    br.push(push( ix, a2[1]+r*e2[1], a2[0]+r*e2[0], 0, e2[1], e2[0]));
  }
  for(i=0;i<n;i++){ var j=(i+1)%n; I.push(bl[i],br[i],bl[j], br[i],br[j],bl[j]) }
  for(var side=-1;side<=1;side+=2){
    var ring=[];
    for(i=0;i<n;i++){
      var a3=prof[i], e3=vn[i], col=[];
      for(k=0;k<=NB;k++){
        var be=(k/NB)*Math.PI/2, cb=Math.cos(be), sb=Math.sin(be);
        col.push(push(side*(ix+r*sb), a3[1]+r*cb*e3[1], a3[0]+r*cb*e3[0],
                      side*sb, cb*e3[1], cb*e3[0]));
      }
      ring.push(col);
    }
    for(i=0;i<n;i++){
      var j2=(i+1)%n;
      for(k=0;k<NB;k++){
        var A2=ring[i][k], B2=ring[i][k+1], C2=ring[j2][k], D2=ring[j2][k+1];
        if(side>0) I.push(A2,B2,C2, B2,D2,C2); else I.push(A2,C2,B2, B2,C2,D2);
      }
    }
    var cz=0, cy=0;
    for(i=0;i<n;i++){cz+=prof[i][0];cy+=prof[i][1]}
    cz/=n; cy/=n;
    var c0=push(side*hw, cy, cz, side, 0, 0), first=idx;
    for(i=0;i<n;i++) push(side*hw, prof[i][1], prof[i][0], side, 0, 0);
    for(i=0;i<n;i++){
      var p1=first+i, p2=first+((i+1)%n);
      if(side>0) I.push(c0,p2,p1); else I.push(c0,p1,p2);
    }
  }
  return meshOut(P,Nm,I);
}

/* ---- 3. the frame ----------------------------------------------------- */
/* A rounded-rectangular frame extruded along z with a DRAFTED inner wall - the piece that
   makes the front bezel a real moulding instead of a rectangle painted on a flat face. The
   opening's centre need not sit on the outer outline's centre, and on this machine it does
   not: the screen is high and the bezel runs to the floor.

   Both outlines are sampled by casting a ray from their own centre and bisecting on the
   rounded-rect distance field. That matches outer to inner sample for sample, needs no
   special case at the corners, and costs nothing at build time. */
function sdRR(x,y,hx,hy,r){
  var qx=Math.abs(x)-(hx-r), qy=Math.abs(y)-(hy-r);
  return Math.min(Math.max(qx,qy),0) + Math.hypot(Math.max(qx,0),Math.max(qy,0)) - r;
}
function rrRay(th,hx,hy,r){
  var dx=Math.cos(th), dy=Math.sin(th), lo=0, hi=Math.hypot(hx,hy)*1.6;
  for(var i=0;i<30;i++){
    var m=(lo+hi)*0.5;
    if(sdRR(dx*m,dy*m,hx,hy,r)<0) lo=m; else hi=m;
  }
  var t=(lo+hi)*0.5; return [dx*t, dy*t];
}
function frameXY(oH,oR,oC, iH,iR,iC, z0,z1, draft, edgeR, SEG){
  var P=[],Nm=[],I=[],idx=0, k;
  function push(x,y,z,nx,ny,nz){
    var L=Math.hypot(nx,ny,nz)||1;
    P.push(x,y,z); Nm.push(nx/L,ny/L,nz/L); return idx++;
  }
  var OUT=[], OUTE=[], IN=[], INU=[];
  for(k=0;k<=SEG;k++){
    var th=(k/SEG)*Math.PI*2;
    var o=rrRay(th,oH[0],oH[1],oR);
    var oe=rrRay(th,oH[0]-edgeR,oH[1]-edgeR,Math.max(oR-edgeR,0.001));
    var iv=rrRay(th,iH[0],iH[1],iR);
    OUT.push([o[0]+oC[0], o[1]+oC[1]]);
    OUTE.push([oe[0]+oC[0], oe[1]+oC[1]]);
    IN.push([iv[0]+iC[0], iv[1]+iC[1]]);
    var uL=Math.hypot(iv[0],iv[1])||1;
    INU.push([iv[0]/uL, iv[1]/uL]);            /* outward radial of the opening */
  }
  /* (a) the front face, between the opening and the start of the outer roll */
  var fa=[], fb=[];
  for(k=0;k<=SEG;k++){
    fa.push(push(IN[k][0],  IN[k][1],  z1, 0,0,1));
    fb.push(push(OUTE[k][0],OUTE[k][1],z1, 0,0,1));
  }
  for(k=0;k<SEG;k++) I.push(fa[k],fb[k],fa[k+1], fb[k],fb[k+1],fa[k+1]);

  /* (b) the inner wall, drafted: the opening is wider at the front, the way a moulded part
         must be to leave its tool. Its normal faces into the opening and tips forward. */
  var wa=[], wb=[];
  for(k=0;k<=SEG;k++){
    var u=INU[k], nx=-u[0]*(z1-z0), ny=-u[1]*(z1-z0), nz=draft;
    wa.push(push(IN[k][0], IN[k][1], z1, nx,ny,nz));
    wb.push(push(IN[k][0]-u[0]*draft, IN[k][1]-u[1]*draft, z0, nx,ny,nz));
  }
  for(k=0;k<SEG;k++) I.push(wa[k],wa[k+1],wb[k], wa[k+1],wb[k+1],wb[k]);

  /* (c) the outer edge: a quarter roll off the front face, then straight back */
  var NR=4, rings=[];
  for(var q=0;q<=NR;q++){
    var be=(q/NR)*Math.PI/2, cb=Math.cos(be), sb=Math.sin(be), row=[];
    for(k=0;k<=SEG;k++){
      var ox=OUTE[k][0], oy=OUTE[k][1];
      var dx=OUT[k][0]-ox, dy=OUT[k][1]-oy, dl=Math.hypot(dx,dy)||1;
      dx/=dl; dy/=dl;
      row.push(push(ox+dx*edgeR*sb, oy+dy*edgeR*sb, z1-edgeR*(1-cb),
                    dx*sb, dy*sb, cb));
    }
    rings.push(row);
  }
  for(q=0;q<NR;q++)for(k=0;k<SEG;k++){
    var A=rings[q][k], B=rings[q][k+1], C=rings[q+1][k], D=rings[q+1][k+1];
    I.push(A,C,B, B,C,D);
  }
  var sa=[], sb2=[];
  for(k=0;k<=SEG;k++){
    var ox2=OUT[k][0], oy2=OUT[k][1];
    var ux=ox2-oC[0], uy=oy2-oC[1], ul=Math.hypot(ux,uy)||1;
    sa.push(push(ox2,oy2,z1-edgeR, ux/ul,uy/ul,0));
    sb2.push(push(ox2,oy2,z0,      ux/ul,uy/ul,0));
  }
  for(k=0;k<SEG;k++) I.push(sa[k],sb2[k],sa[k+1], sb2[k],sb2[k+1],sa[k+1]);
  return meshOut(P,Nm,I);
}

/* ---- 4. merge ---------------------------------------------------------
   Sixty keys as sixty draw calls would be sixty state changes for nothing; they never move
   relative to each other, so they are one mesh. */
function mergeMeshes(list){
  var np=0, ni=0, i;
  for(i=0;i<list.length;i++){ np+=list[i].pos.length; ni+=list[i].idx.length }
  var P=new Float32Array(np), N=new Float32Array(np), I=new Uint16Array(ni);
  var po=0, io=0, base=0;
  for(i=0;i<list.length;i++){
    var m=list[i];
    P.set(m.pos,po); N.set(m.nrm,po);
    for(var k=0;k<m.idx.length;k++) I[io+k]=m.idx[k]+base;
    base+=m.pos.length/3; po+=m.pos.length; io+=m.idx.length;
  }
  return {pos:P,nrm:N,idx:I,n:I.length};
}
function translated(m,tx,ty,tz){
  var P=new Float32Array(m.pos);
  for(var i=0;i<P.length;i+=3){ P[i]+=tx; P[i+1]+=ty; P[i+2]+=tz }
  return {pos:P,nrm:m.nrm,idx:m.idx,n:m.n};
}

/* ---- 5. the keyboard's key field --------------------------------------
   The M0110's layout, in key units of 0.75 inch - the pitch every keyboard has used since.
   Rows are given as widths in units so the wide keys land where they really are: a 1.75u
   Caps Lock, a 2.25u Shift, a 7u space bar. Getting those wrong is the thing that makes a
   modelled keyboard look like a grid of squares rather than a keyboard. */
var KB_ROWS=[
  [1,1,1,1,1,1,1,1,1,1,1,1,1,1.5],                     /* ` 1..0 - = Backspace */
  [1.5,1,1,1,1,1,1,1,1,1,1,1,1,1],                     /* Tab Q..P [ ] \       */
  [1.75,1,1,1,1,1,1,1,1,1,1,1,1.75],                   /* Caps A..L ; ' Return */
  [2.25,1,1,1,1,1,1,1,1,1,1,2.25],                     /* Shift Z..M , . / Shift */
  [1.25,1.25,7.0,1.5,1.25]                             /* Option cmd Space Enter Option */
];
function keyField(pitch, gap, keyH, rowDepth, tilt){
  var parts=[], TOT=14.5, i, j;
  for(i=0;i<KB_ROWS.length;i++){
    var row=KB_ROWS[i], used=0, k;
    for(k=0;k<row.length;k++) used+=row[k];
    var x=-(used*pitch)/2, z=(i-(KB_ROWS.length-1)/2)*rowDepth;
    /* the deck rises toward the back, and each key sits on it */
    var y=-z*tilt;
    for(k=0;k<row.length;k++){
      var w=row[k]*pitch-gap;
      var box=roundedBox(w/2, keyH/2, (rowDepth-gap)/2, Math.min(0.006,keyH/2*0.9), 3);
      parts.push(translated(box, x+row[k]*pitch/2, y, z));
      x+=row[k]*pitch;
    }
  }
  return mergeMeshes(parts);
}

/* ---- 6. the sticky note -----------------------------------------------
   Adhered along its top edge and free at the bottom, which is the whole character of the
   thing: a flat rectangle lying on a disk reads as a printed label, and the lift is what
   makes it a note somebody stuck there.

   The curl is v-squared rather than linear because adhesive holds the top absolutely flat and
   then lets go progressively - a straight ramp looks like a bent card. A slight twist across
   the width keeps it off the symmetry that would give the geometry away. */
function stickyNote(hw, hl, lift, twist, NU, NV){
  var P=[],Nm=[],I=[],i,j;
  for(j=0;j<=NV;j++){
    var v=j/NV;                       /* 0 at the adhered edge, 1 at the free edge */
    var curl=lift*v*v;
    for(i=0;i<=NU;i++){
      var u=i/NU, x=(u-0.5)*2*hw, z=-hl + v*2*hl;
      var y=curl + twist*(u-0.5)*v*v;
      /* the surface normal from the analytic slope of the curl */
      var dydv=(2*lift*v + 2*twist*(u-0.5)*v)/(2*hl);
      var dydu=(twist*v*v)/(2*hw);
      var nx=-dydu, ny=1.0, nz=-dydv, L=Math.hypot(nx,ny,nz);
      P.push(x,y,z); Nm.push(nx/L,ny/L,nz/L);
    }
  }
  for(j=0;j<NV;j++)for(i=0;i<NU;i++){
    var a=j*(NU+1)+i, b=a+1, c=a+(NU+1), d=c+1;
    I.push(a,c,b, b,c,d);
  }
  return meshOut(P,Nm,I);
}

/* ---- 7. a 3.5 inch disk ------------------------------------------------
   90 x 94 x 3.3 mm, which is ISO 8630 and therefore exact, with the corner cut away at the
   top left the way every one of them is - that chamfer is the thing your fingers found in the
   dark, and leaving it off is the first thing anyone who used them would notice. */
function floppyBody(hw, ht, hl, r, chamfer){
  var prof=[
    [-hl+chamfer, -hw],            /* (z, x) walking the outline, top-left cut away */
    [-hl,         -hw+chamfer],
    [-hl,          hw],
    [ hl,          hw],
    [ hl,         -hw]
  ];
  /* extrudeRounded works in (z,y) extruded along x; the disk wants (z,x) extruded along y,
     so build it there and swap the axes afterwards. */
  var m=extrudeRounded(prof, ht, r, 6, r*1.6, 4);
  var P=new Float32Array(m.pos), N=new Float32Array(m.nrm);
  for(var i=0;i<P.length;i+=3){
    var X=P[i], Y=P[i+1], Z=P[i+2];      /* x was the thickness, y was across, z along */
    P[i]=Y; P[i+1]=X; P[i+2]=Z;
    var nx=N[i], ny=N[i+1], nz=N[i+2];
    N[i]=ny; N[i+1]=nx; N[i+2]=nz;
  }
  return {pos:P, nrm:N, idx:m.idx, n:m.n};
}

function crtFace(hw,hh,r,sag,NR,SEG){
  /* The CRT face, as a rounded-rect cap.

     Measured, and the measurement needed care: the reference part's bounding box is 1.027 in
     deep, which taken at face value gives a fishbowl. Binning its vertices by radius showed a
     flat mounting rim sitting at a constant depth behind the curve, and the CURVE is only
     0.327 in from rim to pole. The rim also lands within 0.009 in of the raked front face, so
     the tube bulges THROUGH the opening instead of hiding behind it - which is why the screen
     on this machine catches the light across its whole width rather than sitting in shadow.

     Polar grid over the rounded rect so the boundary is the opening's own shape, and the sag
     falls off as 1 - v^2, which tracks the measured profile to about 0.026 in. */
  var P=[],Nm=[],I=[],idx=0,i,k;
  function at(t,v){
    var e=rrRay(t*Math.PI*2, hw, hh, r);
    return [e[0]*v, e[1]*v, sag*(1.0-v*v)];
  }
  function emit(t,v){
    var p=at(t,v), d=1e-3;
    var a=at(t+d,v), b=at(t-d,v);
    var c=at(t, Math.min(v+d,1.0)), e=at(t, Math.max(v-d,0.0));
    var ux=a[0]-b[0], uy=a[1]-b[1], uz=a[2]-b[2];
    var wx=c[0]-e[0], wy=c[1]-e[1], wz=c[2]-e[2];
    var nx=uy*wz-uz*wy, ny=uz*wx-ux*wz, nz=ux*wy-uy*wx;
    if(nz<0){nx=-nx;ny=-ny;nz=-nz}            /* the glass looks out, always */
    var L=Math.hypot(nx,ny,nz)||1;
    P.push(p[0],p[1],p[2]); Nm.push(nx/L,ny/L,nz/L); return idx++;
  }
  var ring=[];
  for(i=0;i<=NR;i++){ var row=[]; for(k=0;k<SEG;k++) row.push(emit(k/SEG, i/NR)); ring.push(row) }
  for(i=0;i<NR;i++) for(k=0;k<SEG;k++){
    var k2=(k+1)%SEG;
    I.push(ring[i][k],ring[i+1][k],ring[i][k2], ring[i][k2],ring[i+1][k],ring[i+1][k2]);
  }
  return meshOut(P,Nm,I);
}

/* ---------------------------------------------------------------- the packed machine
   A browser has no .blend loader, so the mesh arrives as a binary blob: positions as 16-bit
   fixed point over each group's own box, normals octahedral in 16 bits. Eight bytes a vertex
   rather than twenty-four, and over a 10 inch box a 16-bit step is 0.00015 in - a hundred
   times finer than anything the object itself is toleranced to. */
function b64bytes(s){
  var bin=atob(s), n=bin.length, a=new Uint8Array(n), i;
  for(i=0;i<n;i++) a[i]=bin.charCodeAt(i);
  return a;
}
function octDec(a,b){
  /* a sphere has two degrees of freedom; storing three components spends a third of the bytes
     restating that. This is the inverse of the octahedral fold.

     Eight bits per component, not sixteen. Measured over every normal in this file the error
     is 0.29 degrees on average and 0.93 at worst, which on a matte cream case lit by three
     broad sources is below what the shading can express - and it bought back exactly what
     splitting the vertices at creases cost. */
  var x=a/255*2-1, y=b/255*2-1, z=1-Math.abs(x)-Math.abs(y), t;
  if(z<0){ t=x; x=(1-Math.abs(y))*(t>=0?1:-1); y=(1-Math.abs(t))*(y>=0?1:-1) }
  var L=Math.sqrt(x*x+y*y+z*z)||1;
  return [x/L,y/L,z/L];
}
function decodeMach(b64, xform){
  var by=b64bytes(b64), dv=new DataView(by.buffer), o=0;
  function u8(){ return dv.getUint8(o++) }
  function u16(){ var v=dv.getUint16(o,true); o+=2; return v }
  function u32(){ var v=dv.getUint32(o,true); o+=4; return v }
  function f32(){ var v=dv.getFloat32(o,true); o+=4; return v }
  if(String.fromCharCode(by[0],by[1],by[2],by[3])!=='MACH') throw new Error('bad blob');
  o=4;
  var ver=u16();
  if(ver!==2) throw new Error('blob version '+ver+', expected 2');
  var ng=u16(), out=[], gi, i, k;
  for(gi=0; gi<ng; gi++){
    var ln=u8(), nm='';
    for(i=0;i<ln;i++) nm+=String.fromCharCode(u8());
    var nv=u32(), wide=u8();
    var lo=[f32(),f32(),f32()], hi=[f32(),f32(),f32()];
    var T=xform(nm), S=T.s, P=new Float32Array(nv*3), N=new Float32Array(nv*3);
    for(i=0;i<nv;i++){
      var qx=u16(), qy=u16(), qz=u16();
      /* inches in the file's frame -> tenths of an inch in ours, with Z up becoming Y up and
         the front, which is -Y there, becoming +Z here */
      var mx=(lo[0]+qx/65535*(hi[0]-lo[0])), my=(lo[1]+qy/65535*(hi[1]-lo[1])),
          mz=(lo[2]+qz/65535*(hi[2]-lo[2]));
      P[i*3  ]=(mx-T.o[0])*0.1*S[0];
      P[i*3+1]=(mz-T.o[2])*0.1*S[1]+T.t[1];
      P[i*3+2]=-(my-T.o[1])*0.1*S[2]+T.t[2];
      P[i*3  ]+=T.t[0];
    }
    for(i=0;i<nv;i++){
      var n=octDec(u8(),u8());
      /* a non-uniform scale does not carry normals: they go through the inverse, which is why
         these are divided by the scale rather than multiplied by it */
      var nx=n[0]/S[0], ny=n[2]/S[1], nz=-n[1]/S[2];
      var L=Math.sqrt(nx*nx+ny*ny+nz*nz)||1;
      N[i*3]=nx/L; N[i*3+1]=ny/L; N[i*3+2]=nz/L;
    }
    var np=u16();
    for(k=0;k<np;k++){
      var mat=u8(), ni=u32(), idx=wide?new Uint32Array(ni):new Uint16Array(ni);
      for(i=0;i<ni;i++) idx[i]=wide?u32():u16();
      out.push({name:nm, mat:mat, m:{pos:P, nrm:N, idx:idx, n:ni}});
    }
  }
  return out;
}


  /* ================================================================ the machine
     Origin at the centre of the case. y up, z forward. 1 unit = 10 inches. */
  /* The face measures 10.02 in wide and 12.875 in tall on the reference, not the 9.7 x 13.5
     of the spec sheet - it is an artist's model and we are copying IT, not Apple's drawing.
     The face is centred at x=0 and the SCREEN is offset, because the screen is what sits off
     centre: 0.531 in to the right of the face's middle, and 1.996 in above it. */
  /* APPLE'S DIMENSIONS, not the reference model's. Checking every ratio against photographs
     of the real product turned up the same -3.2% on three unrelated quantities - the glass, the
     keyboard and the mouse were each that much small against the case - and one cause explains
     all three: the Sketchfab model's face measures 10.02 inches where Apple's is 9.7. It is an
     artist's model and it is 3% wide. Asked for a copy AND for realism, the product wins, so
     the case is now 9.7 x 13.5 x 11.2 and everything sized against it lands on the real ratio. */
  /* ================================================================ MEASURED, from a mesh
     Everything from here to the keyboard came off a 3D model of the machine rather than a
     photograph, so these are coordinates and not estimates. The derivations, the residuals
     and the three instrument failures are in docs/MACHINE_MEASURED.md.

     One unit is ten inches. X right, Y up, Z toward the viewer.

     The finding that mattered: THE CASE IS NOT A BOX. Its front face rakes back 6.76 degrees,
     its roof falls 6.40 degrees to the rear, and a brow pushes 1.32 inches forward of the chin
     beneath it. Three earlier builds tuned a flat-fronted, flat-topped box and every one was
     rejected on sight while each individual dimension looked defensible - because no setting
     of a flat front can produce this silhouette. */
  /* The mesh is Apple's machine to within 2%, but not exactly. Measured against Apple's own
     published 344 x 246 x 276 mm (the 1984 owner's guide, confirmed in a second scan and by
     BYTE's August 1984 review) it is 1.5% short and 1.7% narrow while its depth is right to
     0.2%. So: the SHAPE from the mesh, which is the only authority on angles no catalogue
     records, and the SIZE from Apple. Three numbers, one place. */
  var SX=1.016789, SY=1.014916, SZ=1.002305;
  var FLOOR=-0.675;
  var HW=0.4765*SX;           /* 9.69 in across, constant over the whole height - no taper */
  var ROLL=0.019*SX;          /* front-outline corners: 0.215 in at the top, 0.168 at the
                                 bottom, each fitted with a deviation of 0.0035 in */
  /* the rake is a RATIO, so it does not survive a non-uniform scale unchanged - 6.76 degrees
     on the mesh becomes 6.68 once height and depth scale by different amounts. Derived, not
     copied, so it cannot drift away from the profile it belongs to. */
  var RAKE=Math.atan(0.11858*SZ/SY);
  var RC=Math.cos(RAKE), RS=Math.sin(RAKE);
  var CASE_Y=FLOOR+0.6485*SY+ROLL;   /* drops the profile exactly onto the floor */
  var FACE_Z=0.4962*SZ;       /* the raked plane where it crosses the case centre height */

  /* THE PROFILE IS THE INNER OFFSET, NOT THE OUTLINE. extrudeRounded rounds by Minkowski sum
     with a sphere of radius ROLL, which pushes the whole profile OUTWARD by ROLL - so a
     profile drawn at the finished dimensions comes out 2*ROLL too big in every direction and
     its face lands in front of everything meant to sit in the well. That is what swallowed
     the screen once already.

     So this is the measured outline ERODED by ROLL. The erosion is a distance-transform
     threshold rather than a hand-offset polygon, which gets the awkward case right for free:
     a fillet tighter than ROLL cannot survive an ROLL-erosion and comes back as a corner of
     radius exactly ROLL, which is what the moulding actually does. Checked by dilating it
     back and comparing against the outline it started from: IoU 0.9987, worst boundary error
     0.030 in on a machine 13.3 in tall.

     [z toward the viewer, y up], relative to the case centre. Counter-clockwise: up the chin,
     over the brow, up the raked face, back along the roof, down the rear, along the floor. */
  var PROFILE=[
    [+0.3917,-0.4795],[+0.3962,-0.4675],[+0.3997,-0.4615],[+0.4087,-0.4530],
    [+0.4227,-0.4465],[+0.5012,-0.4375],[+0.5232,-0.3895],[+0.4077,+0.5860],
    [+0.4062,+0.5920],[+0.3722,+0.6455],[+0.3252,+0.6420],[-0.4388,+0.5555],
    [-0.5233,+0.3845],[-0.5228,-0.6485],[+0.3917,-0.6485]
  ].map(function(p){ return [p[0]*SZ, p[1]*SY] });

  /* One transform for everything that sits on the face. The face leans back as it rises, so a
     fitting's height and its depth are not independent quantities and keeping them in two
     separate constants is how they drift apart. Parts are built in face space - x across,
     s up the face from the case centre height, local z out along the face normal - and this
     puts them where they belong. */
  var FACE_R=[1,0,0, 0,RC,-RS, 0,RS,RC];
  var FACE_T=[0, CASE_Y, FACE_Z];

  /* the screen, measured. The opening is what a viewer sees; the glass behind it is larger in
     both directions and the bezel crops it. It is CENTRED - 0.004 in off the case centreline -
     where the homography fitted to a photograph had put it 0.53 in to the right. */
  var SCR_S=0.24762*SY;          /* 2.459 in above the case centre, taken up the face */
  var SCR_HW=0.3805*SX, SCR_HH=0.29203*SY;   /* 7.610 x 5.800 in, the second along the face */
  var SCR_R=0.026*SX;            /* opening corner radius 0.258 in, deviation 0.0041 */
  var SCR_DP=0.0154*SZ;          /* the opening chamfer, 0.154 in below the face */
  var GLS_HW=0.3849*SX, GLS_HH=0.30463*SY;   /* 7.698 x 6.049 in of tube face */
  var GLS_SAG=0.0327*SZ;         /* 0.327 in from rim to pole - and the rim sits flush with the
                                 face to within 0.009 in, so the tube bulges THROUGH the
                                 opening rather than sitting behind it */

  /* the disk slot. One opening cut clean through the face - the drive's own bezel sits behind
     it and carries the slot the disk actually goes into. */
  var SLOT_X=0.1696*SX, SLOT_S=-0.26161*SY;  /* 2.598 in below the case centre, 1.696 in right */
  var SLOT_HW=0.2180*SX, SLOT_HH=0.05094*SY; /* 4.360 x 1.012 in */
  var DISK_X=0.1651*SX, DISK_S=-0.27966*SY;  /* the slot in the drive bezel behind it */
  var DISK_HW=0.1629*SX, DISK_HH=0.01712*SY; /* 3.258 x 0.340 in */

  /* ---------------------------------------------------------------- the disks
     ISO 8630: 90 x 94 x 3.3 mm. Cream like the machine - the body colour is ours and only the
     form is copied - with a stainless shutter and a note in the project's own colour.

     Scattered, not arranged. The offsets are written out rather than generated so the pile is
     the same on every load: an arrangement that reshuffles on refresh reads as a screensaver.
     The lifts are one disk thickness apart, which is what lets a corner rest on the one below
     instead of intersecting it. */
  var MM=1.0/254.0;                        /* one unit is ten inches, so 254 mm */
  var DK_HW=45*MM, DK_HT=1.65*MM, DK_HL=47*MM;
  var NOTE_HW=30*MM, NOTE_HL=23*MM;
  var NOTE_CZ=13*MM;                       /* adhered at -10 mm, running back to +36 */
  var PILE=[
    {x:-0.95, z:0.30, rot:-0.34, lift:0.000, col:0},
    {x:-1.34, z:0.52, rot: 0.28, lift:0.014, col:1},
    {x:-0.88, z:0.80, rot: 0.55, lift:0.028, col:2},
    {x:-1.30, z:1.04, rot:-0.16, lift:0.042, col:3}
  ];
  /* XTIX emerald, OASIS brass, EVENTER ice, MEDCOIN paper - the page's own tokens */
  var NOTE_NAME=['XTIX','OASIS','EVENTER','MEDCOIN'];
  var NOTE_RGB=[[0.184,0.702,0.502],[0.878,0.643,0.345],
                [0.369,0.561,0.749],[0.914,0.906,0.874]];

  /* ---------------------------------------------------------------- keyboard and mouse
     Real Apple dimensions, in the same tenths of an inch as everything else. */
  /* Apple's own published figures, not the mesh's. The mesh's peripherals are the weakest
     part of it: its keyboard is 7% too wide and its mouse 28% too wide against Apple's
     numbers, which is the one place the artist clearly worked from photographs. The case is
     the other way round - the mesh knows its shape and no catalogue does. */
  var KBX=-0.0661, KBZ=0.9980;      /* 1.668 in in front of the brow, 0.661 in left of centre */
  var MSX= 0.8200, MSZ=0.9200;      /* just off the keyboard's right edge, level with it */
  var KB_TILT=0.1652;               /* 9.4 degrees; the mesh's keycap plane fitted 9.7 */
  /* M0110: 336 x 146 x 65 mm = 13.23 x 5.75 x 2.56 in. It is a WEDGE - 1.05 in at the front
     edge a wrist rests on, 2.0 in at the back - and a flat slab reads as a prop immediately. */
  var KB_PROFILE=[
    [ 0.2875, 0.105],   /* front top - the thin edge a wrist rests on */
    [-0.2875, 0.200],   /* back top                                   */
    [-0.2875, 0.000],
    [ 0.2875, 0.000]
  ];
  /* keys: 0.75 inch pitch, a 0.08 inch gap, 0.22 inch caps, sitting on the sloped deck */
  var KEYS=(function(){
    /* a 0.14 inch gap, not 0.08. Sixty caps with hairline gaps read as one textured slab
       because the gaps are narrower than the shading can resolve; a real keyboard's gaps
       are wide enough to hold a shadow, and that shadow is what makes them keys. */
    var f=keyField(0.075, 0.014, 0.026, 0.078, KB_TILT);
    /* 0.1525 is the deck's own surface at the key field, not a number of its own: the wedge
       runs 0.105 at the front to 0.200 at the back over 0.575, so the middle sits there.
       Raising the back of the deck without moving this is what buried the keys. */
    return translated(f, 0.0, 0.1525 + 0.013 + 0.006, -0.020);
  })();
  /* a thin plate under the caps, tilted with the deck, so every gap has something dark in it */
  var KEYWELL=(function(){
    var w=roundedBox(0.556, 0.006, 0.200, 0.010, 4), P=new Float32Array(w.pos);
    for(var i=0;i<P.length;i+=3) P[i+1]-=P[i+2]*KB_TILT;      /* lie along the slope */
    return translated({pos:P,nrm:w.nrm,idx:w.idx,n:w.n}, 0.0, 0.1525+0.006, -0.020);
  })();

  /* EVERYTHING IN THE WELL MUST SIT IN FRONT OF z = 0.500. The case shell is solid up to its
     own front plane, so the first attempt - which put the tube's surround at 0.462, behind it -
     drew a perfectly good part inside a solid box and the opening showed bare case instead.
     The bezel is 0.068 thick and that is the whole room there is. */
  /* ---------------------------------------------------------------- the mesh
     Sizes corrected per object rather than all together. The case is 1.5% small against
     Apple's 344 x 246 x 276 mm; the keyboard is 7% wide against the M0110's 336 x 146 mm;
     the mouse is 28% wide against the M0100's 97 x 62 x 37 mm. One scale factor would fit
     none of the three - the artist clearly worked from the product for the case and from
     photographs for the peripherals.

     The keyboard and mouse keep their measured HEIGHT: Apple's 65 mm for the M0110 is a
     max-rear-height on a wedge and single-sourced, and forcing it would stretch the keycaps
     by a quarter to satisfy a figure the machine itself contradicts. */
  var MESH_XF={
    machine:  {s:[1.016789, 1.014916, 1.002305], o:[0.042, -0.634, 0.221], t:[0, FLOOR, 0]},
    keyboard: {s:[0.935644, 1.000000, 0.979557], o:[-0.619, -10.660, 0.023],
               t:[KBX, FLOOR, KBZ]},
    cable:    {s:[1.000000, 1.000000, 1.000000], o:[0.042, -0.634, 0.009], t:[0, FLOOR, 0]},
    mouse:    {s:[0.847222, 1.168000, 0.989637], o:[10.111, -8.447, 0.023],
               t:[MSX, FLOOR, MSZ]}
  };
  function meshXform(name){ return MESH_XF[name] || MESH_XF.machine }

  /* The mesh is not shipped — see tools/extract_machine.py. 933 KB of baked geometry
     against a 520 KB budget, for the same object the code builds in 68 KB. This was a
     query flag; it is now a fact, so nothing can turn it back on and find no data. */
  var USE_MESH = false;
  var PARTS=[
    /* the case: one extrusion of the measured profile, and that is the whole body */
    {m:extrudeRounded(PROFILE,HW,ROLL,10,0.006,4), t:[0,CASE_Y,0],           mat:0},

    /* ---------------------------------------------------------------- on the raked face
       All four sit in face space and share one rotation. The bezel plate is a hair proud of
       the case rather than flush with it: coincident faces z-fight, and 0.008 in is invisible
       at this scale while a fight is not. */
    {m:frameXY([SCR_HW+0.030,SCR_HH+0.030],SCR_R+0.030,[0,SCR_S],
               [SCR_HW,SCR_HH],SCR_R,[0,SCR_S],
               -SCR_DP+0.0008, 0.0008, 0.003, 0.002, 128),
     R:FACE_R, t:FACE_T,                                                     mat:0},
    /* the tube, bulging through the opening. Placed just behind the bezel plate so its rim -
       which is wider than the opening in both directions - is cropped by the bezel, exactly
       as the reference has it. */
    {m:translated(crtFace(GLS_HW,GLS_HH,0.030,GLS_SAG,14,96), 0, SCR_S, -0.0009),
     R:FACE_R, t:FACE_T,                                                     mat:2},

    /* the disk slot: the opening in the face, then the drive bezel behind it, then the slot */
    {m:frameXY([SLOT_HW+0.030,SLOT_HH+0.030],0.028,[SLOT_X,SLOT_S],
               [SLOT_HW,SLOT_HH],0.012,[SLOT_X,SLOT_S],
               -0.030+0.0008, 0.0008, 0.002, 0.004, 96),
     R:FACE_R, t:FACE_T,                                                     mat:0},
    {m:translated(roundedBox(SLOT_HW-0.004,SLOT_HH-0.004,0.006,0.008,5),
                  SLOT_X, SLOT_S, -0.028),
     R:FACE_R, t:FACE_T,                                                     mat:0},
    {m:translated(roundedBox(DISK_HW,DISK_HH,0.005,0.005,4), DISK_X, DISK_S, -0.019),
     R:FACE_R, t:FACE_T,                                                     mat:1},

    /* ---------------------------------------------------------------- the keyboard
       Apple's M0110: 13.2 x 5.83 inches and about 1.4 inch tall at the back, tapering to
       0.75 at the front - it is a WEDGE, and a flat slab reads as a prop immediately. The
       key field is the real layout in 0.75-inch units, so the 1.75u Caps Lock, the 2.25u
       Shifts and the 7u space bar land where a hand expects them. A grid of equal squares is
       the other thing that gives a modelled keyboard away. */
    {m:extrudeRounded(KB_PROFILE,0.6615,0.022,8,0.045,6),      t:[KBX,FLOOR,KBZ], mat:0},
    /* the floor the keys stand in. Without it the caps and the deck are the same tone and the
       gaps between keys carry no shadow, so the field reads as a pattern printed on a slab
       rather than as sixty separate keys. */
    {m:KEYWELL,                                               t:[KBX,FLOOR,KBZ], mat:5},
    {m:KEYS,                                                  t:[KBX,FLOOR,KBZ], mat:4},

    /* ---------------------------------------------------------------- the mouse
       M0100: 2.24 wide, 3.62 long, 1.38 tall, and almost entirely square - one button
       filling the front of the top, and that is the whole object. */
    {m:roundedBox(0.122,0.073,0.191,0.016,8),  t:[MSX,FLOOR+0.073,MSZ],        mat:0},
    {m:roundedBox(0.092,0.009,0.062,0.006,5),  t:[MSX,FLOOR+0.142,MSZ-0.103],  mat:4},


    /* the Apple badge. The mesh cuts a 0.600 in recess for it and puts nothing inside - the
       original filled it with a texture that is missing from the file - so this is a plate for
       the shader to draw the six stripes on. */
    {m:translated(roundedBox(0.0305,0.0307,0.0020,0.004,3), -0.37011, -0.31988, -0.0008),
     R:FACE_R, t:FACE_T,                                                     mat:0},

    {m:(function(){ var s=9; return {pos:new Float32Array([-s,0,-s, s,0,-s, s,0,s, -s,0,s]),
        nrm:new Float32Array([0,1,0, 0,1,0, 0,1,0, 0,1,0]),
        idx:new Uint16Array([0,2,1, 0,3,2]), n:6}; })(), t:[0,-0.675,0], mat:3}
  ];

  /* the mesh replaces everything except the ground. If the blob will not decode we keep the
     procedural machine rather than showing an empty room - a page that renders nothing is
     worse than one that renders a good approximation. */
  /* the pile. One rotation about Y per disk carries its body, its shutter and its note, so the
     three can never drift apart. */
  var DISK=floppyBody(DK_HW, DK_HT, DK_HL, 0.0035, 5*MM);
  var SHUT=roundedBox(19.75*MM, 0.6*MM, 10.5*MM, 0.0016, 3);
  var NOTE=stickyNote(NOTE_HW, NOTE_HL, 8.0*MM, 2.4*MM, 14, 18);
  function addPile(list){
    PILE.forEach(function(d){
      var c=Math.cos(d.rot), sn=Math.sin(d.rot), R=[c,0,-sn, 0,1,0, sn,0,c];
      var y=FLOOR+d.lift;
      list.push({m:DISK, R:R, t:[d.x, y+DK_HT,          d.z], mat:0});
      list.push({m:SHUT, R:R, t:[d.x, y+DK_HT*2+0.6*MM, d.z], mat:6, off:[2*MM,0,-33*MM]});
      list.push({m:NOTE, R:R, t:[d.x, y+DK_HT*2+0.9*MM, d.z], mat:8, off:[0,0,NOTE_CZ],
                 note:d.col});
    });
  }

  var MESH_OK=false;
  if(USE_MESH){
    try{
      var loaded=decodeMach('==', meshXform);
      PARTS=loaded.concat(PARTS.slice(-2));   /* keep the badge and the ground */
      MESH_OK=true;
    }catch(err){
      if(window.console) console.warn('mesh blob failed, falling back to the built one:', err);
    }
  }

  /* ================================================================ program */
  var DERIV=!!gl.getExtension('OES_standard_derivatives');
  var PRE=DERIV?'#extension GL_OES_standard_derivatives : enable\n#define HAS_DERIV 1\n':'';
  function sh(t,src){
    var s=gl.createShader(t);gl.shaderSource(s,src);gl.compileShader(s);
    if(!gl.getShaderParameter(s,gl.COMPILE_STATUS)){read.textContent=gl.getShaderInfoLog(s);throw 0}
    return s;
  }
  var prog=gl.createProgram();
  gl.attachShader(prog,sh(gl.VERTEX_SHADER,'\nattribute vec3 aPos;\nattribute vec3 aNrm;\nuniform mat4 uProj, uView, uModel;\nuniform mat3 uNM;\nvarying vec3 vN;\nvarying vec3 vP;\nvarying vec3 vW;\nvoid main(){\n  vP = aPos;\n  vN = normalize(uNM * aNrm);\n  vec4 w = uModel * vec4(aPos, 1.0);\n  vW = w.xyz;\n  gl_Position = uProj * uView * w;\n}\n'));
  gl.attachShader(prog,sh(gl.FRAGMENT_SHADER,PRE+'precision highp float;\nvarying vec3 vN;\nvarying vec3 vP;\nvarying vec3 vW;\n\nuniform vec3  uCream;\nuniform vec3  uGround;\nuniform vec3  uCam;\nuniform float uMat;\nuniform float uDetail;\nuniform sampler2D uScreen;\nuniform vec4 uScreenRect;\nuniform sampler2D uNoteTex;\nuniform vec2 uNoteTile;\nuniform vec3 uNoteCol;\nuniform vec2 uNoteHalf;      /* 0 plastic, 1 dark moulding, 2 glass, 3 ground, 4 keycap */\n\nfloat box2(vec2 p, vec2 b){\n  vec2 d = abs(p) - b;\n  return min(max(d.x, d.y), 0.0) + length(max(d, 0.0));\n}\nfloat rrect(vec2 p, vec2 b, float r){ return box2(p, b - r) - r; }\n\n#ifdef HAS_DERIV\nfloat aaw(float d){ return max(fwidth(d), 1e-5); }\n#else\nfloat aaw(float d){ return 0.0024; }\n#endif\nfloat inside(float d){ float w = aaw(d); return 1.0 - smoothstep(-w, w, d); }\n\nfloat hash31(vec3 p){ return fract(sin(dot(p, vec3(127.1, 311.7, 74.7))) * 43758.5453); }\nfloat vnoise(vec3 p){\n  vec3 i = floor(p), f = fract(p);\n  f = f * f * (3.0 - 2.0 * f);\n  return mix(mix(mix(hash31(i + vec3(0.0,0.0,0.0)), hash31(i + vec3(1.0,0.0,0.0)), f.x),\n                 mix(hash31(i + vec3(0.0,1.0,0.0)), hash31(i + vec3(1.0,1.0,0.0)), f.x), f.y),\n             mix(mix(hash31(i + vec3(0.0,0.0,1.0)), hash31(i + vec3(1.0,0.0,1.0)), f.x),\n                 mix(hash31(i + vec3(0.0,1.0,1.0)), hash31(i + vec3(1.0,1.0,1.0)), f.x), f.y), f.z);\n}\n\nvoid main(){\n  vec3 N = normalize(vN);\n  vec3 V = normalize(uCam - vW);\n  vec3 albedo = uCream;\n  float ao = 1.0, gloss = 1.0;\n\n  /* ---------------------------------------------------------------- ground\n     BOUNDED at both ends. The keycap material is 4, and an open-ended `uMat > 2.5` swallowed\n     it into the ground branch - which returns early, so every key came out painted as floor. */\n  if(uMat > 2.5 && uMat < 3.5){\n    float lift = 1.0 - smoothstep(0.0, 3.2, length(vW.xz - vec2(0.10, 0.05)));\n    vec3 g = uGround * (1.0 + 0.26 * lift);\n    vec2 q = vW.xz - vec2(0.02, 0.06);\n    float core = 1.0 - smoothstep(0.30, 0.92, length(q / vec2(0.62, 0.60)));\n    float halo = 1.0 - smoothstep(0.35, 1.30, length(q / vec2(1.10, 1.05)));\n    g *= 1.0 - 0.78 * core - 0.26 * halo;\n    gl_FragColor = vec4(g, 1.0);\n    return;\n  }\n\n  /* ---------------------------------------------------------------- glass\n     Bounded, for the same reason the ground branch is: these are early RETURNS, so any\n     material id above the threshold is swallowed by whichever open-ended test comes first.\n     Adding a fifth material at 4 sent every keycap through the glass branch and then, once\n     that was fixed, through the ground branch. An unbounded test in a chain of early returns\n     is a trap that only springs when the next id is added. */\n  if(uMat > 1.5 && uMat < 2.5){\n    /* The page\'s own charcoal, as specified. But a dark rectangle with nothing happening in\n       it reads as a HOLE, not as a screen, and the one thing that separates glass from a hole\n       is that glass returns something. So: the vignette a curved tube has at its corners, a\n       soft band of sky down the upper third the way a CRT catches the room, and a grazing\n       lift at the edges - all of it far too weak to fight the charcoal, and enough to make\n       the surface read as a surface. */\n    /* the screen\'s own rectangle, passed in. This used to be vP.xy divided by a pair of\n       constants, which assumed the tube was centred on the origin - it sits 2.46 in above the\n       case centre, so the vignette was a quarter of a tube out of place. */\n    vec2 s = (vP.xy - uScreenRect.xy) / uScreenRect.zw;\n    float r2 = dot(s, s);\n    vec3 c = uGround * 1.10 * (1.0 - 0.075 * r2);\n\n    float band = pow(max(0.0, 0.5 + 0.5 * s.y), 3.0);         /* the room, high on the tube */\n    c += vec3(0.052, 0.055, 0.062) * band * (1.0 - 0.35 * abs(s.x));\n\n    float edge = smoothstep(0.55, 1.0, sqrt(r2));             /* the curve turning away */\n    c += vec3(0.022, 0.023, 0.027) * edge;\n\n    /* what the machine is showing. A CRT emits rather than reflects, so the raster is ADDED\n       over the glass instead of replacing it - the vignette and the room band still ride on\n       top, which is what keeps a lit screen looking like glass and not like a decal. */\n    /* 342 of the texture\'s 512 rows carry the raster; the rest is padding that exists\n       only so the texture can be mipmapped. */\n    vec2 uv = vec2(s.x * 0.5 + 0.5, 0.5 - s.y * 0.5);\n    float inside_r = step(0.0, uv.x) * step(uv.x, 1.0) * step(0.0, uv.y) * step(uv.y, 1.0);\n    float lit = texture2D(uScreen, vec2(clamp(uv.x,0.0,1.0),\n                                        clamp(uv.y,0.0,1.0) * 0.66797)).r * inside_r;\n    /* P4 phosphor was not white - it ran cool and a little green */\n    c += vec3(0.735, 0.790, 0.755) * lit * (1.0 - 0.18 * r2);\n\n    gl_FragColor = vec4(c, 1.0);\n    return;\n  }\n\n  /* ---------------------------------------------------------------- keycaps\n     The M0110\'s caps are a cooler, slightly darker grey than the case, and a touch glossier -\n     they were moulded in a different plastic and handled every day. */\n  /* ---------------------------------------------------------------- the sticky note\n     Its own colour, and the name written on it. vP is OBJECT space, which is what makes this\n     work at all: every note is a separate part with its own rotation, so a world-space lookup\n     would need the rotation undone first, while the object-space grid already runs -hw..hw\n     across and -hl..hl along. */\n  if(uMat > 7.5 && uMat < 8.5){\n    vec2 nuv = vec2(vP.x / (2.0 * uNoteHalf.x) + 0.5, vP.z / (2.0 * uNoteHalf.y) + 0.5);\n    float ink = 1.0 - texture2D(uNoteTex, uNoteTile + clamp(nuv, 0.0, 1.0) * 0.5).r;\n    albedo = uNoteCol * mix(1.0, 0.22, ink);\n    /* paper, and paper that has been handled: the fibre is coarser than moulded plastic */\n    albedo *= mix(0.955, 1.045, vnoise(vP * 210.0));\n    gloss = 0.10;\n  } else\n  /* ---------------------------------------------------------------- the shutter\n     Stainless, and the only thing on this desk that is not matte. Brushed along its length,\n     so what it returns is a streak rather than a point. */\n  if(uMat > 5.5 && uMat < 6.5){\n    albedo = vec3(0.560, 0.578, 0.600);\n    albedo *= mix(0.86, 1.14, vnoise(vec3(vP.x * 40.0, vP.y * 6.0, vP.z * 300.0)));\n    gloss = 2.6; ao *= 0.92;\n  } else\n  /* BOUNDED AT BOTH ENDS. `uMat > 4.5` alone also claims 6, 7 and 8, and an early return in a\n     chain of else-ifs swallows every material added after it without a word. */\n  if(uMat > 4.5 && uMat < 5.5){         /* the well the keys stand in */\n    albedo = uCream * vec3(0.185, 0.188, 0.190);\n    gloss = 0.3; ao *= 0.55;\n  } else\n  if(uMat > 3.5 && uMat < 4.5){         /* keycaps */\n    albedo = uCream * vec3(0.735, 0.744, 0.738);\n    gloss = 0.9;\n    albedo *= mix(0.975, 1.025, vnoise(vP * 90.0));\n  } else\n  /* ---------------------------------------------------------------- dark moulding */\n  if(uMat > 0.5 && uMat < 2.5){\n    /* On the reference this moulding is near black, and with the screen dark too the whole\n       upper face reads as one dark mass - which is exactly what a switched-off Macintosh\n       looks like and therefore what to copy. 0.520 was chosen to keep the glass legible\n       against it and made the frame a mid brown that appears nowhere on the reference. */\n    albedo = uCream * vec3(0.255, 0.248, 0.238);\n    gloss = 0.55;\n    albedo *= mix(0.96, 1.04, vnoise(vP * 60.0));\n  } else {\n    /* Aged ABS, in three scales. Two octaves of fine mould texture as before, plus a very\n       broad, very shallow one: real thirty-year-old plastic is not evenly coloured across a\n       whole panel, and the reference\'s paint carries that unevenness clearly. A perfectly\n       uniform surface is most of what makes a render look untouched. */\n    float fine = vnoise(vP * 46.0) * 0.55 + vnoise(vP * 15.0) * 0.45;\n    float wide = vnoise(vP * 2.6);\n    albedo *= mix(0.952, 1.038, fine);\n    albedo *= mix(0.975, 1.022, wide);\n\n    /* the logo, six stripes, low and left on the face. Measured off the mesh as a 0.600 in\n       square recess whose centre is 3.640 in left of the case centreline and 3.130 in below\n       it - the previous position was 0.37 in out sideways and 0.52 in low.\n\n       The face test is on the NORMAL now. It used to be step(0.52, vP.z), which asked whether\n       a point was far enough forward; that question only has an answer while the face is a\n       plane at a constant depth, and it is not one any more. */\n    /* world, not object: the badge sits on a rotated plate of its own, so its\n       object space is the face plane and not the machine. */\n    vec2 lp = vW.xy - vec2(-0.37011, -0.31518);\n    float mL = inside(box2(lp, vec2(0.03050, 0.03065))) * step(0.90, N.z);\n    if(mL > 0.001){\n      float band = floor((lp.y + 0.03065) / 0.01022);\n      vec3 lc = band < 1.0 ? vec3(0.24,0.55,0.80)\n              : band < 2.0 ? vec3(0.45,0.30,0.60)\n              : band < 3.0 ? vec3(0.80,0.22,0.30)\n              : band < 4.0 ? vec3(0.90,0.44,0.14)\n              : band < 5.0 ? vec3(0.95,0.77,0.16)\n                           : vec3(0.42,0.66,0.29);\n      albedo = mix(albedo, lc, mL * 0.88);\n    }\n\n    /* THE BACK. The reader can orbit, so it cannot be a blank slab: two vent grids flanking\n       the carry-handle well up top, the badge panel below them, and the port row along the\n       bottom. All surface markings with normals that tip, which is what a moulded grille and\n       a recess actually do to light. */\n    if(uDetail > 0.5 && N.z < -0.55){   /* the rear plane is now at z = -0.402 */\n      vec2 b = vP.xy;\n      float grid = smoothstep(0.30, 0.62, abs(fract((b.y - 0.30) / 0.0165) - 0.5) * 2.0);\n      float gl = inside(rrect(b - vec2(-0.300, 0.300), vec2(0.115, 0.070), 0.012));\n      float gr = inside(rrect(b - vec2( 0.300, 0.300), vec2(0.115, 0.070), 0.012));\n      float gm = max(gl, gr);\n      albedo *= mix(1.0, mix(0.66, 1.0, grid), gm);\n      ao     *= mix(1.0, mix(0.74, 1.0, grid), gm);\n      N = normalize(N + vec3(0.0, 0.22 * (fract((b.y - 0.30) / 0.0165) - 0.5) * 2.0 * gm, 0.0));\n\n      /* the handle well between them */\n      float hw2 = inside(rrect(b - vec2(0.0, 0.315), vec2(0.150, 0.062), 0.020));\n      albedo *= mix(1.0, 0.80, hw2);\n      ao     *= mix(1.0, 0.66, hw2);\n\n      /* the badge panel */\n      float bd = inside(rrect(b - vec2(-0.230, 0.115), vec2(0.145, 0.030), 0.006));\n      albedo = mix(albedo, albedo * 0.86, bd);\n\n      /* the port row */\n      for(int k = 0; k < 4; k++){\n        float px = -0.240 + float(k) * 0.160;\n        float pd = inside(rrect(b - vec2(px, -0.455), vec2(0.052, 0.021), 0.008));\n        albedo = mix(albedo, uCream * 0.24, pd);\n        ao *= mix(1.0, 0.42, pd);\n      }\n    }\n\n    /* THE ROOF. The reference still is shot almost level with the machine so its top never\n       appears in it, and three builds left the roof blank because of that - a real Macintosh\n       has two big vent grilles up there flanking a recessed carry channel, and the moment the\n       reader orbits above the machine a blank roof is the first thing they see. Confirmed\n       against the product itself, not only against the model.\n\n       The slits run ACROSS the machine and stack front to back. */\n    if(uDetail > 0.5 && N.y > 0.80 && vP.y > 0.40){\n      vec2 rp = vec2(vP.x, vP.z);\n      /* measured: a pair 1.741 in across and 7.748 in front to back, centred 3.31 in either\n         side of the middle. The old pair was twice that wide and sat too far forward. */\n      float grille = max(inside(rrect(rp - vec2(-0.33656, 0.03949), vec2(0.08856, 0.38829), 0.020)),\n                         inside(rrect(rp - vec2( 0.33656, 0.03949), vec2(0.08856, 0.38829), 0.020)));\n      float sl = abs(fract((vP.z + 0.44) / 0.0265) - 0.5) * 2.0;\n      float slit = smoothstep(0.26, 0.58, sl);\n      albedo *= mix(1.0, mix(0.62, 1.0, slit), grille);\n      ao     *= mix(1.0, mix(0.70, 1.0, slit), grille);\n      N = normalize(N + vec3(0.0, 0.0, 0.26 * (fract((vP.z + 0.44) / 0.0265) - 0.5) * 2.0 * grille));\n\n      /* the carry channel down the middle, open at the back */\n      /* 4.111 x 1.291 in, and it runs ACROSS the machine - the old one was turned 90 degrees\n         and read as a trench down the middle rather than a handle to lift by. */\n      float ch = inside(rrect(rp - vec2(0.00702, -0.09321), vec2(0.20905, 0.06475), 0.030));\n      albedo *= mix(1.0, 0.78, ch);\n      ao     *= mix(1.0, 0.62, ch);\n    }\n\n    /* vents, low on the flanks. A surface marking with no wall worth modelling, but they are\n       grooves, so the normal tips as well as the colour darkening. */\n    if(uDetail > 0.5 && abs(N.x) > 0.6 && vP.y < -0.47192 && vP.y > -0.66711 && vP.z < 0.31581 && vP.z > -0.54474){\n      /* measured: 7.588 in front to back, 0.938 in tall, low on the flank and set back a\n         little over an inch from the case centre. */\n      float band2 = (vP.y - -0.61711) / 0.0125;\n      float g2 = abs(fract(band2) - 0.5) * 2.0;\n      float ends = inside(box2(vec2(vP.z - -0.11446, vP.y - -0.56951), vec2(0.38027, 0.04760)));\n      float slit = smoothstep(0.28, 0.60, g2);\n      albedo *= mix(1.0, mix(0.70, 1.0, slit), ends);\n      ao     *= mix(1.0, mix(0.78, 1.0, slit), ends);\n      N = normalize(N + vec3(0.0, 0.20 * (fract(band2) - 0.5) * 2.0 * ends, 0.0));\n    }\n  }\n\n  /* ---------------------------------------------------------------- light\n     A broad key from the upper left, a weak fill from the right so the dark flank keeps its\n     form, a hemisphere for the room and a narrow rim for the top edges. The key is WRAPPED,\n     lit = (dot + k)/(1 + k), which is what a large soft source does and a point light cannot:\n     the terminator runs past ninety degrees instead of stopping dead at it. */\n  vec3 key  = normalize(vec3(-0.62, 0.74, 0.58));\n  vec3 fill = normalize(vec3( 0.88, 0.16, 0.30));\n  vec3 rim  = normalize(vec3( 0.10, 0.55,-0.82));\n  float kw = 0.26;\n  float kd = max((dot(N, key) + kw) / (1.0 + kw), 0.0);\n  float fd = max(dot(N, fill), 0.0);\n  float rd = max(dot(N, rim), 0.0);\n  float hemi = 0.155 + 0.150 * (N.y * 0.5 + 0.5);\n  vec3  amb  = vec3(1.02, 1.00, 0.955);      /* the room is warm, and so is what it returns */\n\n  /* the face is not one flat value on the reference: it falls away gently toward the floor,\n     which is what a large source above and in front does to a matte upright plane */\n  float base = smoothstep(-0.70, -0.26, vP.y);\n  ao *= mix(0.62, 1.0, base);\n  ao *= mix(0.90, 1.02, smoothstep(-0.60, 0.55, vP.y));\n\n  /* the well swallows light: the deeper behind the bezel\'s own face a fragment sits, the\n     less of the room reaches it. The first version added a normal-derived quantity to a z\n     coordinate, which is not a depth and never fired. */\n  ao *= mix(0.78, 1.0, smoothstep(0.455, 0.556, vP.z));\n\n  /* the rim carries the whole back now that the reader can orbit to it. It only touches\n     faces pointing away from the viewer\'s usual side, so the front is unaffected. */\n  /* THE FLANK. On the reference the side of the case reads about 0.65 of the face; ours was\n     nearer 0.25, which is the single loudest difference between the two pictures and is\n     lighting, not geometry. The fill from the right carries the flank, so it goes from a\n     token 0.155 to 0.34 - a big soft source on that side, which is what the reference\'s\n     lighting evidently is. */\n  float diff = hemi + kd * 0.80 + fd * 0.340 + rd * 0.165;\n  /* the roof is the one plane facing the room\'s brightest direction and on the reference it\n     is clearly the lightest surface on the machine; without this the object has no \'up\' */\n  float sky  = pow(max(N.y, 0.0), 1.9) * 0.115;\n\n  vec3  H = normalize(key + V);\n  /* the reference\'s plastic has a broad, weak sheen and no hard highlight anywhere; a\n     tighter lobe put a bright line along the well\'s top lip that belongs to nothing */\n  float spec = pow(max(dot(N, H), 0.0), 16.0) * 0.055 * gloss;\n  float fres = pow(1.0 - max(dot(N, V), 0.0), 3.6) * 0.055 * gloss;\n\n  gl_FragColor = vec4(albedo * amb * (diff + sky) * ao + vec3(spec + fres) * ao, 1.0);\n}\n'));
  gl.linkProgram(prog);
  if(!gl.getProgramParameter(prog,gl.LINK_STATUS)){read.textContent=gl.getProgramInfoLog(prog);return}
  gl.useProgram(prog);
  gl.activeTexture(gl.TEXTURE0);
  var A={pos:gl.getAttribLocation(prog,'aPos'), nrm:gl.getAttribLocation(prog,'aNrm')};
  /* ---------------------------------------------------------------- the raster
     512 x 342, which is not a round number chosen for convenience: it is the machine's real
     active area, 7.111 x 4.750 inches at 72 dpi. Drawn at runtime, so it adds no bytes to the
     file and makes no request.

     Everything is thresholded to pure black and white at the end. That one step is what makes
     a modern font read as 1984: the Macintosh had one bit per pixel and no antialiasing, and
     grey edges are the first thing that gives a fake screen away. */
  function screenTexture(){
    var W=512, H=342, cv2=document.createElement('canvas');
    cv2.width=W; cv2.height=512;      /* padded to a power of two, see below */
    var x=cv2.getContext('2d');

    /* the desktop: the 50% stipple the Finder actually showed, built as pixels rather than as
       175,000 fill calls */
    var img=x.createImageData(W,H), d=img.data, i, j, o;
    for(j=0;j<H;j++) for(i=0;i<W;i++){
      o=(j*W+i)*4; var on=((i+j)&1)===0?0:255;
      d[o]=d[o+1]=d[o+2]=on; d[o+3]=255;
    }
    x.putImageData(img,0,0);

    /* the menu bar */
    x.fillStyle='#fff'; x.fillRect(0,0,W,20);
    x.fillStyle='#000'; x.fillRect(0,20,W,1);
    x.font='13px Geneva, Chicago, "Lucida Grande", Verdana, sans-serif';
    x.textBaseline='middle';
    x.fillText('⌘', 12, 10);
    var menus=['File','Edit','View','Special'], mx=40;
    for(i=0;i<menus.length;i++){ x.fillText(menus[i], mx, 10); mx+=x.measureText(menus[i]).width+22 }

    /* the folder, white and matte, drawn the way the Finder drew one: a tab, a body, and a
       one-pixel black rule round the outside */
    var fw=104, fh=80, fx=(W-fw)/2, fy=104;
    x.fillStyle='#fff';
    x.beginPath();
    x.moveTo(fx, fy+10); x.lineTo(fx+34, fy+10); x.lineTo(fx+42, fy+2); x.lineTo(fx+fw, fy+2);
    x.lineTo(fx+fw, fy+fh); x.lineTo(fx, fy+fh); x.closePath();
    x.fill();
    x.strokeStyle='#000'; x.lineWidth=2; x.stroke();
    x.beginPath(); x.moveTo(fx+2, fy+18); x.lineTo(fx+fw-2, fy+18); x.stroke();

    /* the name, on a white slip the way a selected icon carries its label */
    x.font='16px Geneva, Chicago, "Lucida Grande", Verdana, sans-serif';
    x.textAlign='center';
    var label='Oran Carmon — Master File';
    var tw=x.measureText(label).width;
    x.fillStyle='#fff'; x.fillRect(W/2-tw/2-8, fy+fh+12, tw+16, 24);
    x.fillStyle='#000'; x.fillText(label, W/2, fy+fh+24);

    /* one bit per pixel, no antialiasing */
    var px=x.getImageData(0,0,W,H), q=px.data;
    for(i=0;i<q.length;i+=4){
      var v=(q[i]*0.299+q[i+1]*0.587+q[i+2]*0.114)>=128?255:0;
      q[i]=q[i+1]=q[i+2]=v;
    }
    x.putImageData(px,0,0);

    var tex=gl.createTexture();
    gl.bindTexture(gl.TEXTURE_2D,tex);
    gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL,false);
    gl.texImage2D(gl.TEXTURE_2D,0,gl.RGBA,gl.RGBA,gl.UNSIGNED_BYTE,cv2);
    /* 512x342 is not a power of two, so clamp and no mipmaps - WebGL1 allows that combination
       and nothing else */
    /* a one-pixel checkerboard is the worst case for aliasing and it crawled badly without
       these. WebGL1 allows mipmaps only on power-of-two textures, which is the whole reason
       the canvas is 512x512 with the raster in its top 342 rows. */
    gl.generateMipmap(gl.TEXTURE_2D);
    gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_S,gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_T,gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MIN_FILTER,gl.LINEAR_MIPMAP_LINEAR);
    gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MAG_FILTER,gl.LINEAR);
    return tex;
  }

  var U={};['uProj','uView','uModel','uNM','uCream','uGround','uCam','uMat','uDetail','uScreen','uScreenRect','uNoteTex','uNoteTile','uNoteCol','uNoteHalf']
    .forEach(function(k){U[k]=gl.getUniformLocation(prog,k)});

  /* read where it is used, not from the query block further down: that block runs AFTER this
     loop, and a var declaration hoists without its value, so the flag was reliably undefined. */
  var KEEPGEO=/[?&]dbg=1/.test(location.search);
  /* the raster's rectangle in world units: the ACTIVE area, 7.111 x 4.750 in, centred in the
     opening 2.459 in above the case centre. Not the opening itself - the bezel is wider than
     the picture on every Macintosh ever made. */
  addPile(PARTS);

  var SCR_TEX=screenTexture();
  var SCR_RECT=[ -0.0004, 0.0019+0.24762*SY, 0.35560*SX, 0.23750*SY ];

  /* ---------------------------------------------------------------- the handwriting
     Four names on one atlas. Caveat is inlined as a data URI so the page still makes no
     request, and because a font arrives asynchronously the atlas is drawn twice: once now in
     whatever face is available, and again when Caveat reports itself ready. */
  var NOTE_TEX=gl.createTexture();
  function drawNotes(){
    var TW=256, TH=160, cvN=document.createElement('canvas');
    cvN.width=TW*2; cvN.height=TH*2;
    var x=cvN.getContext('2d');
    x.fillStyle='#fff'; x.fillRect(0,0,cvN.width,cvN.height);
    x.fillStyle='#1b1b1e'; x.textAlign='center'; x.textBaseline='middle';
    for(var i=0;i<4;i++){
      var ox=(i%2)*TW, oy=Math.floor(i/2)*TH, nm=NOTE_NAME[i];
      /* one size does not fit MEDCOIN and XTIX both, so the size follows the width */
      var fs=74;
      do { x.font=fs+'px Caveat, "Segoe Script", cursive'; fs-=2 }
      while(x.measureText(nm).width > TW*0.78 && fs > 20);
      x.save();
      x.translate(ox+TW/2, oy+TH*0.52);
      x.rotate((i%2 ? -1 : 1) * 0.035);     /* nobody writes perfectly level */
      x.fillText(nm, 0, 0);
      x.restore();
    }
    gl.activeTexture(gl.TEXTURE1);
    gl.bindTexture(gl.TEXTURE_2D,NOTE_TEX);
    gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL,false);
    gl.texImage2D(gl.TEXTURE_2D,0,gl.RGBA,gl.RGBA,gl.UNSIGNED_BYTE,cvN);
    gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_S,gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_T,gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MIN_FILTER,gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MAG_FILTER,gl.LINEAR);
    gl.activeTexture(gl.TEXTURE0);
  }
  drawNotes();
  if(document.fonts && document.fonts.load){
    document.fonts.load('64px Caveat').then(function(){ drawNotes(); kick() })
      .catch(function(){});
  }

  var TRIS=0;
  PARTS.forEach(function(P){
    P.p=gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER,P.p);
    gl.bufferData(gl.ARRAY_BUFFER,P.m.pos,gl.STATIC_DRAW);
    P.nb=gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER,P.nb);
    gl.bufferData(gl.ARRAY_BUFFER,P.m.nrm,gl.STATIC_DRAW);
    P.i=gl.createBuffer(); gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER,P.i);
    gl.bufferData(gl.ELEMENT_ARRAY_BUFFER,P.m.idx,gl.STATIC_DRAW);
    P.count=P.m.idx.length; TRIS+=P.count/3;
    var R=P.R||[1,0,0, 0,1,0, 0,0,1], T=(P.t||[0,0,0]).slice();
    if(P.off){                            /* an offset in the part's OWN frame, not the world's */
      var f=P.off;
      T[0]+=R[0]*f[0]+R[3]*f[1]+R[6]*f[2];
      T[1]+=R[1]*f[0]+R[4]*f[1]+R[7]*f[2];
      T[2]+=R[2]*f[0]+R[5]*f[1]+R[8]*f[2];
    }
    P.M=new Float32Array([R[0],R[1],R[2],0, R[3],R[4],R[5],0, R[6],R[7],R[8],0, T[0],T[1],T[2],1]);
    P.NM=new Float32Array(R);
    if(KEEPGEO) P.raw=P.m;                      /* ?dbg=1 keeps it, so the built geometry
                                                   can be measured instead of screenshotted */
    P.m=null;                                   /* the CPU copy has done its job */
  });

  /* ================================================================ maths */
  function persp(fovDeg,asp,n,f){var t=1/Math.tan(fovDeg*Math.PI/360),d=1/(n-f);
    return new Float32Array([t/asp,0,0,0, 0,t,0,0, 0,0,(f+n)*d,-1, 0,0,2*f*n*d,0])}
  function lookAt(e,c,u){
    var zx=e[0]-c[0],zy=e[1]-c[1],zz=e[2]-c[2],zl=Math.hypot(zx,zy,zz);zx/=zl;zy/=zl;zz/=zl;
    var xx=u[1]*zz-u[2]*zy, xy=u[2]*zx-u[0]*zz, xz=u[0]*zy-u[1]*zx;
    var xl=Math.hypot(xx,xy,xz);xx/=xl;xy/=xl;xz/=xl;
    var yx=zy*xz-zz*xy, yy=zz*xx-zx*xz, yz=zx*xy-zy*xx;
    return new Float32Array([xx,yx,zx,0, xy,yy,zy,0, xz,yz,zz,0,
      -(xx*e[0]+xy*e[1]+xz*e[2]), -(yx*e[0]+yy*e[1]+yz*e[2]), -(zx*e[0]+zy*e[1]+zz*e[2]), 1]);
  }
  var NM=new Float32Array([1,0,0, 0,1,0, 0,0,1]);   /* nothing is rotated in model space */

  /* ================================================================ camera + orbit
     The reader gets to walk round it, so the orbit has weight: a drag hands the camera its
     velocity and the camera keeps it, shedding it over about a second. Snapping to a stop the
     instant a finger lifts is the thing that makes a viewer feel like a widget. */
  var W=0,H=0,DPR=1,PROJ=null;
  /* the camera is settable from the query string so the render can be put at the reference
     photograph's exact viewpoint and the two compared pixel for pixel. Comparing a model to a
     reference from a different angle compares the angles, not the models. */
  var Q=new URLSearchParams(location.search);
  function qn(k,d){ var v=parseFloat(Q.get(k)); return isNaN(v)?d:v }
  var yaw=qn('yaw',-0.46), pitch=qn('pitch',0.20), dist=qn('dist',5.6);
  var FOV=qn('fov',21), BGF=qn('bg',0);
  var vYaw=0, vPitch=0, drag=false, lx=0, ly=0, lt=0, raf=null;

  function size(){
    /* Supersample. MSAA resolves GEOMETRY edges, and the panel markings are drawn INSIDE
       triangles by the shader where MSAA never looks; only rendering above the display
       resolution and filtering down touches those. */
    DPR=Math.min((window.devicePixelRatio||1)*1.75, 2.6);
    W=cv.clientWidth;H=cv.clientHeight;
    cv.width=Math.round(W*DPR);cv.height=Math.round(H*DPR);
    gl.viewport(0,0,cv.width,cv.height);
    PROJ=persp(FOV,W/H,0.05,60);
  }

  function frame(){
    /* bg=1 paints the reference's own grey so a silhouette lifts identically from both */
    if(BGF>0.5) gl.clearColor(0.793,0.784,0.757,1); else gl.clearColor(0.098,0.102,0.122,1);
    gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT);
    gl.enable(gl.DEPTH_TEST); gl.enable(gl.CULL_FACE); gl.cullFace(gl.BACK);

    var ex=Math.sin(yaw)*Math.cos(pitch)*dist,
        ey=Math.sin(pitch)*dist+0.16,
        ez=Math.cos(yaw)*Math.cos(pitch)*dist;
    gl.uniformMatrix4fv(U.uProj,false,PROJ);
    gl.uniformMatrix4fv(U.uView,false,lookAt([ex,ey,ez],[0,0.02,0],[0,1,0]));
    gl.uniform3f(U.uCam,ex,ey,ez);
    gl.uniform3f(U.uCream,0.874,0.845,0.768);
    gl.uniform3f(U.uGround,0.098,0.102,0.122);

    for(var i=0;i<PARTS.length;i++){
      var P=PARTS[i];
      if(BGF>0.5 && P.mat===3) continue;      /* no floor while measuring a silhouette */
      gl.uniform1f(U.uMat,P.mat);
      gl.uniform1f(U.uDetail,MESH_OK?0.0:1.0);
      gl.uniform1i(U.uScreen,0);
      gl.uniform1i(U.uNoteTex,1);
      gl.uniform2f(U.uNoteHalf,NOTE_HW,NOTE_HL);
      if(P.note!==undefined){
        gl.uniform2f(U.uNoteTile,(P.note%2)*0.5,Math.floor(P.note/2)*0.5);
        gl.uniform3f(U.uNoteCol,NOTE_RGB[P.note][0],NOTE_RGB[P.note][1],
                                NOTE_RGB[P.note][2]);
      }
      gl.uniform4f(U.uScreenRect,SCR_RECT[0],SCR_RECT[1],SCR_RECT[2],SCR_RECT[3]);
      gl.uniformMatrix4fv(U.uModel,false,P.M);
      gl.uniformMatrix3fv(U.uNM,false,P.NM);
      gl.bindBuffer(gl.ARRAY_BUFFER,P.p);  gl.enableVertexAttribArray(A.pos); gl.vertexAttribPointer(A.pos,3,gl.FLOAT,false,0,0);
      gl.bindBuffer(gl.ARRAY_BUFFER,P.nb); gl.enableVertexAttribArray(A.nrm); gl.vertexAttribPointer(A.nrm,3,gl.FLOAT,false,0,0);
      gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER,P.i);
      gl.drawElements(gl.TRIANGLES,P.count,gl.UNSIGNED_SHORT,0);
    }
    read.textContent =
      'macintosh 128k + M0110 + M0100   246 x 344 x 276 mm, measured   ' + PARTS.length + ' parts, ' +
      TRIS.toLocaleString() + ' triangles\n' +
      'yaw ' + yaw.toFixed(2) + '  pitch ' + pitch.toFixed(2) + '  dist ' + dist.toFixed(2);
  }

  function glide(){
    raf=null;
    if(drag) return;
    if(Math.abs(vYaw)<1e-4 && Math.abs(vPitch)<1e-4){ vYaw=0; vPitch=0; return }
    yaw+=vYaw; pitch+=clampPitch(pitch+vPitch)-pitch;
    vYaw*=0.92; vPitch*=0.92;
    frame();
    raf=requestAnimationFrame(glide);
  }
  function clampPitch(p){ return p>1.15?1.15:(p<-0.40?-0.40:p) }
  function kick(){ if(!raf) raf=requestAnimationFrame(glide) }

  addEventListener('resize',function(){size();frame()});
  cv.style.touchAction='none';
  cv.addEventListener('pointerdown',function(e){
    drag=true; lx=e.clientX; ly=e.clientY; lt=e.timeStamp; vYaw=0; vPitch=0;
    cv.setPointerCapture(e.pointerId);
  });
  cv.addEventListener('pointermove',function(e){
    if(!drag)return;
    var dx=(e.clientX-lx)*0.0062, dy=(e.clientY-ly)*0.0052;
    yaw-=dx; pitch=clampPitch(pitch+dy);
    vYaw=-dx*0.55; vPitch=dy*0.55;
    lx=e.clientX; ly=e.clientY; lt=e.timeStamp;
    frame();
  });
  function release(){ if(drag){ drag=false; kick() } }
  cv.addEventListener('pointerup',release);
  cv.addEventListener('pointercancel',release);
  cv.addEventListener('wheel',function(e){
    e.preventDefault();
    dist*=(1+Math.sign(e.deltaY)*0.06);
    if(dist<2.6)dist=2.6; if(dist>11)dist=11;
    frame();
  },{passive:false});

  size(); frame();

  /* hand the frame back to the harness so the same measurement code runs over it and over
     the reference photograph */
  /* the built geometry, so it can be measured rather than admired. Every previous check on
     this object went through a camera, and a camera turns a shape question into a shape-plus-
     lens-plus-threshold question - which is how a silhouette score sat at 0.86 for five builds
     while measuring the reference's contact shadow. */
  window.__parts=PARTS;
  window.__shot=function(name){
    frame();
    return fetch('/save/'+name,{method:'POST',body:cv.toDataURL('image/png')})
             .then(function(r){return r.text()});
  };
  window.__cam=function(y,p,d,f){
    if(y!=null)yaw=y; if(p!=null)pitch=p; if(d!=null)dist=d;
    if(f!=null){FOV=f; size();}
    frame();
    return [yaw,pitch,dist,FOV];
  };
  window.__sweep=function(list){
    /* capture a whole grid in one round trip: the browser is the slow part, not the GPU */
    var i=0;
    function step(){
      if(i>=list.length) return Promise.resolve('done '+list.length);
      var c=list[i++];
      window.__cam(c[0],c[1],c[2],c[3]);
      return window.__shot(c[4]).then(step);
    }
    return step();
  };
})();

