# -*- coding: utf-8 -*-
# Site sync: Medcoin section -> dark (white-file), matching the PDF polish pass
import io
s=io.open("site.html",encoding="utf-8").read()

# 1. replace the paper override CSS block with dark white-file styling
start="/* ============ MEDCOIN PAPER ============ */"
end="#medcoin .insight .who{color:rgba(12,13,16,.5)}"
i0=s.index(start); i1=s.index(end)+len(end)
newcss="""/* ============ MEDCOIN — DARK, WHITE FILE ============ */
#medcoin .outs{position:relative;border:1px solid var(--grid);border-radius:0 12px 12px 12px;background:var(--card2);padding:6px 20px 8px}
#medcoin .outs table{width:100%;border-collapse:collapse}
#medcoin .outs td{border-top:1px solid var(--grid);padding:10px 0;vertical-align:middle}
#medcoin .outs tr:first-child td{border-top:none}
#medcoin .outs .k{font-family:'JetBrains Mono',monospace;font-size:8.5px;letter-spacing:.16em;color:var(--dim)}
#medcoin .outs .v{text-align:right;font-weight:700;font-size:13.5px;color:var(--ink)}
#medcoin .outs .v.em{color:var(--emb)}
#medcoin .stamp{position:absolute;top:-16px;right:16px;transform:rotate(-7deg);border:2px solid var(--emb);border-radius:6px;
padding:6px 13px;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:12px;letter-spacing:.3em;color:var(--emb);background:var(--bg)}
#medcoin .lessq .qx b{color:var(--emb)}"""
s=s[:i0]+newcss+s[i1:]

# 2. section accent: white file
s=s.replace('<section class="sec case" id="medcoin" style="--fc:#F4603E">',
            '<section class="sec case" id="medcoin" style="--fc:var(--ink)">',1)

# 3. timeline svg colors -> dark theme (scoped to medcoin slice)
a=s.index('id="medcoin"'); b=s.index('<section class="sec" id="leadership"')
seg=s[a:b]
seg=seg.replace('stroke="#0C0D10" stroke-width="1.6"','stroke="#F2F1ED" stroke-width="1.6"')
seg=seg.replace('x2="930" y2="26" stroke="#0C0D10" stroke-width="1.5"','x2="930" y2="26" stroke="#F2F1ED" stroke-width="1.5"')
seg=seg.replace('r="5" fill="#F2F1ED"','r="5" fill="#0C0D10"')
seg=seg.replace('fill="rgba(12,13,16,.6)"','fill="#8E8E93"')
s=s[:a]+seg+s[b:]

io.open("site.html","w",encoding="utf-8").write(s)
print("site medcoin -> dark, synced")
