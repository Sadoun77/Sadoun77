import re
HEAD='''  <div class="head">
    <img src="img0.jpeg" alt="">
    <div class="t"><div class="school">المدرسة الكردية في النرويج — قسم اللغة العربية</div>
      <div class="meta"><span>اسم الطالب: ...................................</span><span>الصف: <b>الأول (ب)</b></span></div></div>
    <div class="badge">ي</div>
  </div>'''
FOOT='  <div class="foot"><span>حرف الياء ( ي )</span><span>صفحة X من Y</span></div>'

def row(items, h=132, W=1000):
    """items: list of (text, kind) placed right-to-left; kind: model|trace|blank"""
    n=len(items); step=W/n; out=[f'<svg class="wl" viewBox="0 0 {W} {h}" ">',
      f'<line x1="0" y1="12" x2="{W}" y2="12" class="l-top"/>',
      f'<line x1="0" y1="120" x2="{W}" y2="120" class="l-mid"/>',
      f'<line x1="0" y1="64" x2="{W}" y2="64" class="l-base"/>']
    for i,(t,k) in enumerate(items):
        x=W-step*(i+.5)
        if k=='blank': continue
        out.append(f'<text x="{x:.0f}" y="64" class="{k}">{t}</text>')
    out.append('</svg>'); return ''.join(out)

def letterrow(t, models=2, traces=4, blanks=2):
    return row([(t,'model')]*models+[(t,'trace')]*traces+[('', 'blank')]*blanks)

css='''
/* ===== kids pages ===== */
.kid-hero{display:flex;align-items:center;gap:6mm;margin:5mm 0 4mm}
.kid-hero .L{width:48mm;height:48mm;border-radius:50%;background:var(--red-soft);display:flex;align-items:center;justify-content:center;flex:none;border:3px solid var(--red)}
.kid-hero .L span{font-family:Amiri;font-weight:700;font-size:92pt;color:var(--red);line-height:1;margin-top:-8mm}
.bubble{position:relative;background:var(--gold-soft);border-radius:6mm;padding:4mm 6mm;font-size:15pt;font-weight:700;line-height:1.8}
.bubble:before{content:"";position:absolute;right:-5mm;top:50%;margin-top:-4mm;border:4mm solid transparent;border-left-color:var(--gold-soft);border-right:0}
.bubble .ar{font-size:22pt;color:var(--red)}
.emo{font-family:"Noto Color Emoji";font-weight:400}
.kid-sec{font-size:14pt;font-weight:900;margin:3mm 0 2.5mm;display:flex;gap:2mm;align-items:center}
.pics{display:grid;grid-template-columns:repeat(4,1fr);gap:3mm}
.pic{border:2px solid var(--line);border-radius:5mm;text-align:center;padding:2mm 0 1mm}
.pic .emo{font-size:30pt;line-height:1.3}
.pic .ar{font-weight:700;font-size:22pt;line-height:1.3}
.pic em{color:var(--red);font-style:normal}
.hide{display:grid;grid-template-columns:repeat(3,1fr);gap:3mm}
.hbox{border-radius:5mm;padding:2.5mm;text-align:center}
.hbox.a{background:var(--blue-soft)} .hbox.b{background:var(--green-soft)} .hbox.c{background:var(--red-soft)}
.hbox .t1{font-size:11pt;font-weight:900}
.hbox .emo{font-size:24pt;line-height:1.2}
.hbox .ar{font-weight:700;font-size:26pt;line-height:1.3}
.hbox em{color:var(--red);font-style:normal}
.dots{display:flex;justify-content:center;gap:4mm;margin-top:1mm}
.dots i{width:4mm;height:4mm;border-radius:50%;background:#CBD5E0;display:block}
.dots i.on{background:var(--red)}
.snd{display:grid;grid-template-columns:repeat(3,1fr);gap:3mm}
.sn{border:2px dashed var(--line);border-radius:5mm;text-align:center;padding:1mm}
.sn .ar{font-weight:700;font-size:34pt;line-height:1.4;color:var(--blue)}
.sn .x{font-size:10pt;color:var(--muted)}
/* steps */
.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:4mm;margin:2mm 0 4mm}
.st{border:2px solid var(--line);border-radius:5mm;text-align:center;padding:2mm 2mm 3mm}
.st .no{display:inline-flex;width:9mm;height:9mm;border-radius:50%;background:var(--gold);color:#fff;font-weight:900;align-items:center;justify-content:center;font-size:13pt}
.st svg{width:100%;height:40mm;display:block}
.st .cap{font-size:11.5pt;font-weight:700;line-height:1.5}
.ghost{font-family:Amiri;font-weight:700;font-size:150px;fill:#E2E8F0;text-anchor:middle}
.ink{font-family:Amiri;font-weight:700;font-size:150px;fill:var(--red);text-anchor:middle}
/* writing lines */
.wl{width:100%;height:24mm;display:block;margin-bottom:2.5mm}
.wl .l-top,.wl .l-mid{stroke:#CBD5E0;stroke-width:1.5;stroke-dasharray:8 6}
.wl .l-base{stroke:var(--blue);stroke-width:2.5}
.wl text{font-family:Amiri;font-weight:700;font-size:96px;text-anchor:middle;direction:rtl}
.wl .model{fill:var(--ink)}
.wl .trace{fill:none;stroke:#94A3B8;stroke-width:2;stroke-dasharray:5 4}
.rowlbl{display:flex;align-items:center;gap:2mm;font-size:11pt;font-weight:700;margin:1.5mm 0 .5mm}
.rowlbl .tag{background:var(--gold-soft);border-radius:3mm;padding:0 3mm;font-family:Amiri;font-size:17pt}
.legend{display:flex;gap:6mm;font-size:10pt;color:var(--muted);margin-bottom:3mm}
.legend b{color:var(--ink)}
.wordrow{display:flex;align-items:center;gap:3mm;margin-bottom:2mm}
.wordrow .emo{font-size:30pt;width:17mm;text-align:center;flex:none}
.wordrow svg{flex:1}
.fill{display:grid;grid-template-columns:repeat(3,1fr);gap:4mm}
.fb{border:2px solid var(--line);border-radius:5mm;text-align:center;padding:2mm}
.fb .emo{font-size:34pt;line-height:1.3}
.fb .ar{font-weight:700;font-size:28pt;line-height:1.5}
.fb .gap{display:inline-block;width:12mm;border-bottom:3px dotted var(--red);height:9mm;vertical-align:middle}
.star{margin-top:auto;display:flex;align-items:center;justify-content:center;gap:4mm;font-size:13pt;font-weight:700;color:var(--muted)}
.star .emo{font-size:22pt}
'''

kid=f'''<!-- ============ شرح بصري للطفل ============ -->
<section class="page">
{HEAD}
  <div class="kid-hero">
    <div class="L"><span>ي</span></div>
    <div class="bubble">مرحبًا! <span class="emo">👋</span> أنا حرفُ <span class="ar">الياء</span><br>
      بطني كبيرٌ مثلَ القارب <span class="emo">⛵</span><br>
      وتحتي نقطتان <span class="emo">••</span> لا تنسَهما!</div>
  </div>

  <div class="kid-sec"><span class="emo">🔊</span> أسمعُ صوتي في هذه الكلمات</div>
  <div class="pics">
    <div class="pic"><div class="emo">✋</div><div class="ar"><em>يَـ</em>ـد</div></div>
    <div class="pic"><div class="emo">🏠</div><div class="ar">بَـ<em>ـيْـ</em>ـت</div></div>
    <div class="pic"><div class="emo">☀️</div><div class="ar"><em>يَـ</em>ـوْم</div></div>
    <div class="pic"><div class="emo">🕊️</div><div class="ar"><em>يَـ</em>ـمامة</div></div>
  </div>

  <div class="kid-sec"><span class="emo">🔍</span> أين أختبئُ في الكلمة؟</div>
  <div class="hide">
    <div class="hbox a"><div class="t1">في الأوّل</div><div class="emo">✋</div><div class="ar"><em>يـ</em>ـد</div><div class="dots"><i></i><i class="on"></i></div></div>
    <div class="hbox b"><div class="t1">في الوسط</div><div class="emo">🏠</div><div class="ar">بـ<em>ـيـ</em>ـت</div><div class="dots"><i></i><i class="on"></i><i></i></div></div>
    <div class="hbox c"><div class="t1">في الآخر</div><div class="emo">🪑</div><div class="ar">كرسـ<em>ـي</em></div><div class="dots"><i class="on"></i><i></i><i></i><i></i></div></div>
  </div>

  <div class="kid-sec"><span class="emo">🎵</span> أغيّرُ صوتي مع الحركات</div>
  <div class="snd">
    <div class="sn"><div class="ar">يَ</div><div class="x">فتحة ← «يَـ» كما في يَد</div></div>
    <div class="sn"><div class="ar">يُ</div><div class="x">ضمة ← «يُـ»</div></div>
    <div class="sn"><div class="ar">يِ</div><div class="x">كسرة ← «يِـ»</div></div>
  </div>

  <div class="star"><span class="emo">⭐</span> قُلْ معي: يَ — يُ — يِ ... يَد! <span class="emo">⭐</span></div>
{FOOT}
</section>
'''

step_svg=lambda inner:f'<svg viewBox="0 0 200 200">{inner}</svg>'
steps=f'''<!-- ============ كيف أكتب الياء + تتبّع ============ -->
<section class="page">
{HEAD}
  <div class="ws-top"><div class="n emo" style="font-size:18pt">✍️</div><div><h2>كيفَ أكتبُ حرفَ الياء؟</h2><p>ثلاثُ خطواتٍ سهلة</p></div></div>
  <div class="steps">
    <div class="st"><span class="no">1</span>
      {step_svg('<defs><clipPath id="c1"><rect x="96" y="0" width="104" height="100"/></clipPath></defs><text x="100" y="96" class="ghost">ى</text><text x="100" y="96" class="ink" clip-path="url(#c1)">ى</text><circle cx="147" cy="40" r="8" fill="#2F855A"/>')}
      <div class="cap">أبدأ من فوق <span class="emo">🟢</span><br>وأنزلُ قليلًا</div></div>
    <div class="st"><span class="no">2</span>
      {step_svg('<text x="100" y="96" class="ink">ى</text>')}
      <div class="cap">أرسمُ بطنًا كبيرًا<br>مثلَ القارب <span class="emo">⛵</span></div></div>
    <div class="st"><span class="no">3</span>
      {step_svg('<defs><clipPath id="c3"><rect x="0" y="137" width="200" height="63"/></clipPath></defs><text x="100" y="96" class="ghost" style="fill:#1F2A37">ي</text><text x="100" y="96" class="ink" clip-path="url(#c3)">ي</text>')}
      <div class="cap">أضعُ نقطتين<br>تحتَ البطن <span class="emo">••</span></div></div>
  </div>
  <div class="legend"><span><b>الحرف الأسود:</b> انظر إليه</span><span><b>الحرف المنقّط:</b> مرِّر القلم فوقه</span><span><b>المكان الفارغ:</b> اكتب وحدك</span></div>
  {''.join(letterrow('ي') for _ in range(6))}
  <div class="star"><span class="emo">⭐</span> أحسنت! تذكّر النقطتين تحت الحرف <span class="emo">⭐</span></div>
{FOOT}
</section>
'''

shapes=f'''<!-- ============ كتابة أشكال الحرف ============ -->
<section class="page">
{HEAD}
  <div class="ws-top"><div class="n emo" style="font-size:18pt">✏️</div><div><h2>أكتبُ أشكالَ حرفِ الياء</h2><p>في الأوّل — في الوسط — في الآخر</p></div></div>
  <div class="hint">✏️ تتبّع الحرف المنقّط، ثم اكتبه وحدك في آخر السطر. ابدأ دائمًا من اليمين <span class="emo">⬅️</span></div>
  <div class="rowlbl"><span class="tag">يـ</span> في أوّل الكلمة — مثل <span class="ar" style="font-size:15pt">يَد ✋</span></div>
  {letterrow('يـ',2,4,2)}{letterrow('يـ',1,4,3)}
  <div class="rowlbl"><span class="tag">ـيـ</span> في وسط الكلمة — مثل <span class="ar" style="font-size:15pt">بَيْت 🏠</span></div>
  {letterrow('ـيـ',2,4,2)}{letterrow('ـيـ',1,4,3)}
  <div class="rowlbl"><span class="tag">ـي</span> في آخر الكلمة — مثل <span class="ar" style="font-size:15pt">كُرْسي 🪑</span></div>
  {letterrow('ـي',2,4,2)}{letterrow('ـي',1,4,3)}
{FOOT}
</section>
'''

def wordrow(emo,w):
    return f'<div class="wordrow"><span class="emo">{emo}</span>{row([(w,"model"),(w,"trace"),(w,"trace"),("","blank")])}</div>'
words=f'''<!-- ============ كتابة الكلمات ============ -->
<section class="page">
{HEAD}
  <div class="ws-top"><div class="n emo" style="font-size:18pt">🖍️</div><div><h2>أكتبُ كلماتٍ فيها حرفُ الياء</h2><p>أنظرُ إلى الصورة، أقرأ الكلمة، ثم أكتبها</p></div></div>
  {wordrow('✋','يد')}{wordrow('🏠','بيت')}{wordrow('☀️','يوم')}{wordrow('🪑','كرسي')}{wordrow('🕊️','يمامة')}
  <div class="kid-sec" style="margin-top:4mm"><span class="emo">🧩</span> أكملُ الكلمةَ بحرفِ الياء المناسب</div>
  <div class="fill">
    <div class="fb"><div class="emo">✋</div><div class="ar"><span class="gap"></span>ـد</div></div>
    <div class="fb"><div class="emo">🏠</div><div class="ar">بـ<span class="gap"></span>ـت</div></div>
    <div class="fb"><div class="emo">🪑</div><div class="ar">كرسـ<span class="gap"></span></div></div>
  </div>
  <div class="star"><span class="emo">🌟</span> رائع! أنت الآن تعرف حرف الياء <span class="emo">🌟</span></div>
{FOOT}
</section>
'''

s=open('ya.html').read()
if '/* ===== kids pages' not in s:
    s=s.replace('</style>',css+'</style>')
    s=s.replace('<!-- ============ ورقة عمل 1 ============ -->', kid+steps+shapes+words+'\n<!-- ============ ورقة عمل 1 ============ -->',1)
s=s.replace('+ أوراق العمل المرفقة (الصفحات 3–6)','+ تمارين الكتابة وأوراق العمل المرفقة')
# renumber worksheets 1..4 -> 5..8
for a,b in [(4,8),(3,7),(2,6),(1,5)]:
    s=s.replace(f'<div class="ws-top"><div class="n">{a}</div>',f'<div class="ws-top"><div class="n">{b}</div>')
s=s.replace('<li>تتبّع حرف الياء (تين)</li>','<li>شرح مصوّر للطفل + كيف أكتب الياء</li><li>كتابة أشكال الحرف والكلمات</li><li>تتبّع حرف الياء (تين)</li>')
s=s.replace('<li>كتابة الياء على النقاط','<li>كتابة الياء على النقاط').replace('<div class="card"><h3>أوراق العمل</h3>\n        <ol>','<div class="card"><h3>أوراق العمل</h3>\n        <ol style="font-size:10pt;line-height:1.6">')
# page numbers
s=re.sub(r'صفحة (\d+|X) من (\d+|Y)','صفحة §',s)
total=s.count('صفحة §'); i=0
def rep(m):
    global i; i+=1; return f'صفحة {i} من {total}'
s=re.sub('صفحة §',rep,s)
open('ya.html','w').write(s)
print(total)
