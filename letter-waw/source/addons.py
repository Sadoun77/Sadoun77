import re, random, sys

CSS = '''<style>
/* ===== addons ===== */
.lad{display:flex;align-items:flex-end;gap:2.5mm;margin-bottom:9mm}
.lad .pic{border:none;padding:0;width:20mm;flex:none;text-align:center}
.lad .pic .emo{font-size:30pt}
.stp{flex:1;border-radius:3.5mm 3.5mm 0 0;display:flex;flex-direction:column;align-items:center;justify-content:center;position:relative;border-bottom:3px solid var(--ink)}
.stp .ar{font-weight:700;line-height:1.2}
.stp .k{position:absolute;top:1mm;right:2mm;font-size:8pt;font-weight:700;color:var(--muted)}
.s1{height:24mm;background:#EBF4FF;flex:.8}.s1 .ar{font-size:24pt}
.s2{height:32mm;background:#E6F4EA;flex:.9}.s2 .ar{font-size:24pt}
.s3{height:40mm;background:#FEF3C7;flex:1}.s3 .ar{font-size:25pt}
.s4{height:48mm;background:#FDECEC;flex:1.9}.s4 .ar{font-size:23pt}
.hl{color:var(--red)}
.story{display:grid;grid-template-columns:1fr 1fr;gap:4mm;margin-bottom:4mm}
.scene{border:2px solid var(--line);border-radius:5mm;padding:6mm 3mm;text-align:center;position:relative}
.scene .no{position:absolute;top:2mm;right:2mm;width:7mm;height:7mm;border-radius:50%;background:var(--gold);color:#fff;font-weight:900;font-size:10pt;display:flex;align-items:center;justify-content:center}
.scene .emo{font-size:54pt;line-height:1.4}
.scene .ar{font-weight:700;font-size:26pt;line-height:1.6}
.q{border:2px dashed var(--gold);border-radius:5mm;padding:3mm 5mm;margin-bottom:3mm}
.q .qt{font-weight:700;font-size:12.5pt;margin-bottom:1.5mm}
.q .opts{display:flex;gap:6mm;justify-content:center}
.q .opt{border:2px solid var(--line);border-radius:4mm;padding:1mm 5mm;text-align:center}
.q .opt .emo{font-size:26pt}
.q .opt .ar{font-weight:700;font-size:16pt}
.mz{flex:1;min-height:0;display:flex;align-items:center;justify-content:center}
.mz svg{max-width:100%;max-height:100%}
.hunt{display:grid;grid-template-columns:repeat(6,1fr);gap:3.5mm;margin:2mm 12mm 4mm}
.hunt div{aspect-ratio:1;border:2.5px solid var(--ink);border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:Amiri;font-weight:700;font-size:30pt;padding-bottom:2mm}
.count{display:flex;align-items:center;justify-content:center;gap:4mm;font-size:14pt;font-weight:700}
.count .box{width:20mm;height:13mm;border:2.5px dashed var(--red);border-radius:3mm}
.parent{font-size:9pt;color:var(--muted);text-align:center;margin-top:2mm}
.chart{width:100%;border-collapse:separate;border-spacing:0 1.6mm;margin-top:1mm}
.chart td{background:#F9FAFB;padding:.6mm 4mm;font-size:11.5pt;font-weight:700}
.chart td:first-child{border-radius:0 4mm 4mm 0;width:12mm;text-align:center;color:var(--gold);font-size:14pt}
.chart td:last-child{border-radius:4mm 0 0 4mm;width:26mm;text-align:center}
.chart svg{width:10mm;height:10mm;vertical-align:middle}
.sign{display:flex;justify-content:space-between;margin-top:auto;padding-top:4mm;font-size:12pt}
.cert{flex:1;border:5px double var(--gold);border-radius:6mm;margin-top:4mm;padding:8mm 10mm;display:flex;flex-direction:column;align-items:center;text-align:center;position:relative;
  background:radial-gradient(circle at 50% 35%,#FFFBEB 0,#fff 70%)}
.cert .corner{position:absolute;font-size:24pt}
.cert img{width:24mm}
.cert h1{font-size:30pt;color:var(--gold);margin:3mm 0 1mm}
.cert .medal{width:44mm;height:44mm;border-radius:50%;background:var(--gold);display:flex;align-items:center;justify-content:center;margin:5mm 0;box-shadow:0 0 0 3mm var(--gold-soft)}
.cert .medal span{font-family:Amiri;font-weight:700;font-size:84pt;color:#fff;line-height:1;margin-top:-6mm}
.cert .to{font-size:14pt;color:var(--muted)}
.cert .nm{width:120mm;border-bottom:2.5px dotted var(--ink);height:14mm;margin:2mm 0 6mm}
.cert ul{list-style:none;font-size:14pt;font-weight:700;line-height:2}
.cert .sig{display:flex;justify-content:space-between;width:100%;margin-top:auto;font-size:12pt}
.cert .sig div{border-top:1.5px solid var(--line);padding-top:2mm;width:60mm}
</style>'''

NONLEFT=set('اأإآدذرزوؤةىء')
DIAC=re.compile('[\u064B-\u0652]')
def hl(text, L):
    """colour every L in red while keeping Arabic joining (ZWJ at span edges)"""
    out=[];i=0;n=len(text);Z='\u200d'
    while i<n:
        ch=text[i]
        if ch!=L: out.append(ch);i+=1;continue
        j=i+1
        while j<n and DIAC.match(text[j]): j+=1
        k=i-1
        while k>=0 and DIAC.match(text[k]): k-=1
        prev=text[k] if k>=0 else ' '
        nxt=text[j] if j<n else ' '
        joins_prev=('\u0621'<=prev<='\u064A') and prev not in NONLEFT
        joins_next=L not in NONLEFT and ('\u0621'<=nxt<='\u064A')
        out.append((Z if joins_prev else '')+'<span class="hl">'+(Z if joins_prev else '')+text[i:j]+(Z if joins_next else '')+'</span>'+(Z if joins_next else ''))
        i=j
    return ''.join(out)

def maze_svg(L, goal_emo, cols=8, rows=10, seed=7):
    seed=ord(L)
    random.seed(seed); c=60; pad=70
    W=cols*c+2*pad; H=rows*c+2*pad
    walls={(x,y,d) for x in range(cols) for y in range(rows) for d in 'NESW'}
    seen={(cols-1,0)}; st=[(cols-1,0)]
    D={'N':(0,-1,'S'),'S':(0,1,'N'),'E':(1,0,'W'),'W':(-1,0,'E')}
    while st:
        x,y=st[-1]; nb=[(d,x+dx,y+dy,o) for d,(dx,dy,o) in D.items() if 0<=x+dx<cols and 0<=y+dy<rows and (x+dx,y+dy) not in seen]
        if not nb: st.pop(); continue
        d,nx,ny,o=random.choice(nb); walls.discard((x,y,d)); walls.discard((nx,ny,o)); seen.add((nx,ny)); st.append((nx,ny))
    walls.discard((cols-1,0,'N')); walls.discard((0,rows-1,'S'))
    segs=set()
    for x,y,d in walls:
        X=pad+x*c; Y=pad+y*c
        s={'N':(X,Y,X+c,Y),'S':(X,Y+c,X+c,Y+c),'W':(X,Y,X,Y+c),'E':(X+c,Y,X+c,Y+c)}[d]; segs.add(s)
    lines=''.join(f'<line x1="{a}" y1="{b}" x2="{e}" y2="{f}"/>' for a,b,e,f in segs)
    sx=pad+(cols-.5)*c; ex=pad+.5*c
    return (f'<svg viewBox="0 0 {W} {H}"><rect x="{pad-8}" y="{pad-8}" width="{cols*c+16}" height="{rows*c+16}" rx="18" fill="#FFFBEB"/>'
            f'<g stroke="#1F2A37" stroke-width="7" stroke-linecap="round">{lines}</g>'
            f'<circle cx="{sx}" cy="{pad-38}" r="30" fill="#C53030"/><text x="{sx}" y="{pad-24}" text-anchor="middle" fill="#fff" style="font-family:Amiri;font-weight:700;font-size:44px">{L}</text>'
            f'<text x="{sx-42}" y="{pad-28}" style="font-family:Cairo;font-weight:700;font-size:24px" fill="#2F855A" text-anchor="start" direction="rtl">ابدأ من هنا</text>'
            f'<text x="{ex}" y="{H-10}" text-anchor="middle" style="font-family:Noto Color Emoji;font-size:50px">{goal_emo}</text></svg>')

STAR='<svg viewBox="0 0 24 24"><path d="M12 2l2.9 6.3 6.9.7-5.2 4.6 1.5 6.8L12 17l-6.1 3.4 1.5-6.8L2.2 9l6.9-.7z" fill="none" stroke="#C9A13B" stroke-width="1.6" stroke-linejoin="round"/></svg>'

def build(html, cfg):
    L=cfg['L']
    head=re.search(r'<section class="page">\s*(<div class="head">.*?</div>\s*</div>\s*<div class="badge">.*?</div>\s*</div>)', html, re.S)
    # use the student header (the one with اسم الطالب)
    heads=re.findall(r'(  <div class="head">(?:(?!</section>).)*?<div class="badge">[^<]*</div>\n  </div>)', html, re.S)
    H=[h for h in heads if 'اسم الطالب' in h][0]
    F=f'  <div class="foot"><span>{cfg["title"]}</span><span>صفحة 0 من 0</span></div>'
    def page(inner, style=''): return f'<section class="page"{style}>\n{H}\n{inner}\n{F}\n</section>\n'
    top=lambda e,t,p: f'<div class="ws-top"><div class="n emo" style="font-size:18pt">{e}</div><div><h2>{t}</h2><p>{p}</p></div></div>'

    lad=''.join(f'''<div class="lad"><div class="pic"><div class="emo">{e}</div></div>
      <div class="stp s1"><span class="k">1</span><div class="ar">{hl(a,L)}</div></div>
      <div class="stp s2"><span class="k">2</span><div class="ar">{hl(b,L)}</div></div>
      <div class="stp s3"><span class="k">3</span><div class="ar">{hl(c,L)}</div></div>
      <div class="stp s4"><span class="k">4</span><div class="ar">{hl(d,L)}</div></div></div>''' for e,a,b,c,d in cfg['ladders'])
    p_lad=page(top('🪜','سُلَّمُ القراءة','أقرأ الدرجة، ثم أصعد إلى التي بعدها ⬅️')+
      '<div class="hint">👣 ابدأ من الدرجة الصغيرة: <b>صوت</b> ← <b>مقطع</b> ← <b>كلمة</b> ← <b>جملة</b>. ضع ✓ عند كل سُلَّم تصعده حتى آخره.</div>'+lad+
      '<div class="star"><span class="emo">🏆</span> وصلتَ إلى القمة! أنت قارئٌ ماهر <span class="emo">🏆</span></div>')

    sc=''.join(f'<div class="scene"><span class="no">{i+1}</span><div class="emo">{e}</div><div class="ar">{hl(t,L)}</div></div>' for i,(e,t) in enumerate(cfg['story']))
    qq=cfg['question']
    opts=''.join(f'<div class="opt"><div class="emo">{e}</div><div class="ar">{w}</div></div>' for e,w in qq[1])
    p_story=page(top('📖',cfg['story_title'],'قصةٌ قصيرة — أقرؤها مع ماما أو بابا')+
      f'<div class="story">{sc}</div>'+
      f'<div class="q"><div class="qt">❓ {qq[0]} <span style="font-weight:400;color:var(--muted)">(ضع دائرة حول الجواب)</span></div><div class="opts">{opts}</div></div>'+
      f'<div class="q"><div class="qt">🔴 ضع دائرةً حول كلِّ حرف <span class="ar" style="font-size:16pt">( {L} )</span> في القصة. كم حرفًا وجدت؟ <span style="display:inline-block;width:16mm;border-bottom:2.5px dotted var(--ink)"></span></div></div>')

    p_maze=page(top('🧭',cfg['maze_title'],'أرسمُ الطريقَ بالقلم من البداية إلى النهاية')+
      '<div class="hint">✏️ ابدأ من الدائرة الحمراء، وامشِ بين الجدران بدون أن تلمسها، حتى تصل إلى الصورة.</div>'+
      f'<div class="mz">{maze_svg(L,cfg["maze_goal"])}</div>')

    random.seed(3); pool=cfg['decoys']; n=36; k=cfg['hunt_count']
    cells=[L]*k+[random.choice(pool) for _ in range(n-k)]; random.shuffle(cells)
    grid=''.join(f'<div>{x}</div>' for x in cells)
    p_hunt=page(top('🔍',f'صيدُ حرفِ {cfg["name"]}',f'أبحثُ عن حرف ( {L} ) بين أصدقائه')+
      f'<div class="hint">🖍️ لوِّن كلَّ دائرةٍ فيها حرف <b class="ar" style="font-size:14pt">( {L} )</b> باللون الأحمر. انتبه! بعض الحروف تشبهه.</div>'+
      f'<div class="hunt">{grid}</div>'+
      f'<div class="count">كم دائرةً لوّنت؟ <span class="box"></span></div>'+
      f'<div class="parent">لولي الأمر: عدد الحروف الصحيحة {k}</div>')
    return p_lad+p_story+p_maze+p_hunt, H, page

def finish(html, cfg, insert_before, H, page):
    # star chart + certificate appended at end
    secs=re.findall(r'<section class="page".*?</section>', html, re.S)
    titles=[]
    for s in secs:
        if 'kid-hero' in s: titles.append(f'أتعرّفُ على حرف {cfg["name"]}'); continue
        m=re.search(r'<h2>(.*?)</h2>',s) or re.search(r'<h1>(.*?)</h1>',s)
        titles.append(re.sub('<[^>]+>','',m.group(1)).strip() if m else '')
    titles+= ['جدولُ نجومي']
    rows=''.join(f'<tr><td>{i+1}</td><td>{t}</td><td>{STAR}</td></tr>' for i,t in enumerate(titles[:-1]) if i>0)
    chart=page('<div class="ws-top"><div class="n emo" style="font-size:18pt">⭐</div><div><h2>جدولُ نجومي</h2><p>ألوّنُ نجمةً كلّما أنهيتُ صفحة</p></div></div>'+
      f'<table class="chart">{rows}</table>'+
      '<div class="sign"><span>توقيع ولي الأمر: ...........................</span><span>توقيع المعلمة: ...........................</span></div>')
    cert=f'''<section class="page">
  <div class="cert">
    <span class="corner emo" style="top:4mm;right:5mm">⭐</span><span class="corner emo" style="top:4mm;left:5mm">⭐</span>
    <span class="corner emo" style="bottom:4mm;right:5mm">🌟</span><span class="corner emo" style="bottom:4mm;left:5mm">🌟</span>
    <img src="img0.jpeg" alt="">
    <div style="font-size:11pt;color:var(--muted);margin-top:2mm">المدرسة الكردية في النرويج — قسم اللغة العربية</div>
    <h1>شهادةُ إتقان</h1>
    <div style="font-size:16pt;font-weight:700">حرف {cfg["name"]}</div>
    <div class="medal"><span>{cfg["L"]}</span></div>
    <div class="to">تُمنَحُ هذه الشهادة للبطل / للبطلة</div>
    <div class="nm"></div>
    <ul><li>✅ أقرأُ حرفَ {cfg["name"]}</li><li>✅ أكتبُ حرفَ {cfg["name"]} بأشكاله</li><li>✅ أجدُ حرفَ {cfg["name"]} في الكلمات</li></ul>
    <div style="font-size:15pt;font-weight:900;color:var(--red);margin-top:3mm">أحسنت! <span class="emo">👏</span></div>
    <div class="sig"><div>المعلمة: <b>رجاء الحو</b></div><div>التاريخ: {cfg["date"]}</div></div>
  </div>
</section>
'''
    html=html.replace('</body>', chart+cert+'</body>')
    total=len(re.findall(r'صفحة \d+ من \d+',html)); k=iter(range(1,total+1))
    html=re.sub(r'صفحة \d+ من \d+',lambda m:f'صفحة {next(k)} من {total}',html)
    return html

def run(src, dst, cfg, marker):
    html=open(src).read()
    if '/* ===== addons' not in html: html=html.replace('</head>',CSS+'</head>')
    pages,H,page=build(html,cfg)
    i=html.index(marker) if marker else html.index('</body>')
    html=html[:i]+pages+html[i:]
    html=finish(html,cfg,None,H,page)
    open(dst,'w').write(html)

YA=dict(L='ي',name='الياء',title='حرف الياء ( ي )',date='27/9/2025',
  ladders=[('✋','يَ','يَدْ','يَدي','هذه يَدي'),('🏠','بَـ','بَيْـ','بَيْت','هذا بَيْتي'),('☀️','يَـ','يَوْ','يَوْم','اليَوْمُ جَميلٌ')],
  story_title='قصة: يدي و قدمي',
  story=[('✋','هذه يَدي.'),('🦶','هذه قَدَمي.'),('🏠','أنا في البَيْتِ.'),('☀️','اليَوْمُ جَميلٌ.')],
  question=('أين أنا؟',[('🏠','البيت'),('🌳','الحديقة'),('🏫','المدرسة')]),
  maze_title='ساعِدِ الياءَ لتصلَ إلى البيت',maze_goal='🏠',
  decoys=['ب','ت','ن','ث','ى','ر'],hunt_count=12)
WAW=dict(L='و',name='الواو',title='حرف الواو ( و )',date='19/9/2026',
  ladders=[('🌹','وَ','وَرْ','وَرْد','هذا وَرْدٌ'),('🍌','مَـ','مَوْ','مَوْز','أُحِبُّ المَوْزَ'),('💡','نُـ','نُو','نُور','هذه نُور')],
  story_title='قصة: نور و ماما',
  story=[('👧','هذه نُورُ.'),('🌹','نُورُ تُحِبُّ الوَرْدَ.'),('👩','ماما تُعْطي نُورَ مَوْزًا.'),('🍌','نُورُ تَأْكُلُ المَوْزَ.')],
  question=('ماذا تُحِبُّ نُور؟',[('🌹','الورد'),('🚗','السيارة'),('⚽','الكرة')]),
  maze_title='ساعِدِ الواوَ لتصلَ إلى الوردة',maze_goal='🌹',
  decoys=['ر','ز','د','ذ','ف','ق'],hunt_count=12)

if __name__=='__main__':
    run('ya.html','ya_full.html',YA,'<!-- ============ ورقة عمل 1')
    run('waw.html','waw_full.html',WAW,None)
