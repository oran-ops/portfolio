import io,re,subprocess,fitz
SRC='cv_ops.html'
BASE=io.open(SRC,encoding='utf-8').read()
D=r'C:\Users\Alex\AppData\Local\Temp\claude\C--Users-Alex-Desktop\e3c36f0f-f1cf-432c-9d0d-0ceb4892074a\scratchpad\portfolio'
DU='file:///C:/Users/Alex/AppData/Local/Temp/claude/C--Users-Alex-Desktop/e3c36f0f-f1cf-432c-9d0d-0ceb4892074a/scratchpad/portfolio'
CHROME=r'C:\Program Files\Google\Chrome\Application\chrome.exe'
UDD=r'C:\Users\Alex\AppData\Local\Temp\claude\C--Users-Alex-Desktop\75c46525-df9e-4ec4-95b8-e051c77aaff6\scratchpad\chromeprof'
PT=72/96.0

def variant(fs,lh,measure=False):
    s=re.sub(r'--fs:[\d.]+px;', f'--fs:{fs}px;', BASE)
    s=re.sub(r'--lh:[\d.]+;',  f'--lh:{lh};',   s)
    if measure:
        s=s.replace('@page{size:794px 1123px;margin:0}','@page{size:794px 2600px;margin:0}')
        s=s.replace('width:794px;height:1123px;overflow:hidden','width:794px;height:2600px;overflow:visible')
    return s

def render(html,tag):
    io.open(f'_{tag}.html','w',encoding='utf-8').write(html)
    subprocess.run([CHROME,'--headless=new','--disable-gpu','--no-first-run',f'--user-data-dir={UDD}',
        '--no-pdf-header-footer','--virtual-time-budget=6000',
        f'--print-to-pdf={D}\_{tag}.pdf',f'{DU}/_{tag}.html'],capture_output=True)
    return fitz.open(f'_{tag}.pdf')[0]

def span(fs,lh):
    p=render(variant(fs,lh,measure=True),'mo')
    bs=p.get_text('blocks')
    return min(b[1] for b in bs)/PT, max(b[3] for b in bs)/PT
