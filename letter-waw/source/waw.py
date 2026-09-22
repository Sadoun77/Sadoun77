import re
src=open('ya.html').read()
CSS=src[src.index('<style>'):src.index('</style>')+8]
CSS+='<style>.steps svg .ghost,.steps svg .ink{font-size:190px}</style>'
def HEAD(student=True):
    meta=('<span>اسم الطالب: ...................................</span><span>الصف: <b>الأول (أ)</b></span>' if student else
          '<span>الصف: <b>الأول (أ)</b></span><span>المعلمة: <b>رجاء الحو</b></span><span>التاريخ: <b>19/9/2026</b></span>')
    return f'''  <div class="head">
    <img src="img0.jpeg" alt="">
    <div class="t"><div class="school">المدرسة الكردية في النرويج — قسم اللغة العربية</div>
      <div class="meta">{meta}</div></div>
    <div class="badge">و</div>
  </div>'''
FOOT='  <div class="foot"><span>حرف الواو ( و )</span><span>صفحة §</span></div>'

def row(items,h=132,W=1000):
    n=len(items);step=W/n
    o=[f'<svg class="wl" viewBox="0 0 {W} {h}">','<line x1="0" y1="12" x2="1000" y2="12" class="l-top"/>',
       '<line x1="0" y1="120" x2="1000" y2="120" class="l-mid"/>','<line x1="0" y1="64" x2="1000" y2="64" class="l-base"/>']
    for i,(t,k) in enumerate(items):
        if k!='blank': o.append(f'<text x="{W-step*(i+.5):.0f}" y="64" class="{k}">{t}</text>')
    return ''.join(o)+'</svg>'
lr=lambda t,m=2,tr=4,b=2: row([(t,'model')]*m+[(t,'trace')]*tr+[('','blank')]*b)
wr=lambda e,w: f'<div class="wordrow"><span class="emo">{e}</span>{row([(w,"model"),(w,"trace"),(w,"trace"),("","blank")])}</div>'

program=f'''<section class="page">
{HEAD(False).replace('<span>التاريخ: <b>19/9/2026</b></span>','')}
  <h1>برنامجُ الأسبوع</h1>
  <div class="prog-info">
    <div class="info"><div class="k">الأسبوع</div><div class="v">39</div></div>
    <div class="info"><div class="k">التاريخ</div><div class="v">19 / 9 / 2026</div></div>
    <div class="info"><div class="k">الصف</div><div class="v">الأول (أ)</div></div>
  </div>
  <div class="cols">
    <div class="col past"><div class="ch">الدرس الماضي</div><div class="body">
      <div class="lesson">الدرس: رامي و بابا</div><div class="big">ا</div>
      <div>حرف (ا) وأشكاله</div>
      <div class="chips"><span class="chip">رامي</span><span class="chip">ماما</span><span class="chip">بابا</span></div>
      <img src="w_past.jpeg" alt=""></div></div>
    <div class="col new"><div class="ch">الدرس الجديد</div><div class="body">
      <div class="lesson">الدرس: نور و ماما</div><div class="big">و</div>
      <div>حرف (و) وأشكاله</div>
      <div class="chips"><span class="chip">ورد</span><span class="chip">ولد</span><span class="chip">موز</span></div>
      <div>تدريب على قراءة الحرف والكلمات</div>
      <img src="w_new.jpeg" alt=""></div></div>
    <div class="col hw"><div class="ch">الواجبات المنزلية</div><div class="body">
      <div class="lesson">كتاب مدرسة الحروف</div><div class="big">و</div>
      <ul><li>كتابة حرف (و) وأشكاله</li><li>كلمات تحتوي حرف (و)</li></ul>
      <div class="chips"><span class="chip">لوز</span><span class="chip">ورد</span></div>
      <div>+ تمارين الكتابة المرفقة</div>
      <img src="w_hw.jpeg" alt=""></div></div>
  </div>
  <div class="teacher"><div class="box">المعلمة: <b>رجاء الحو</b></div><div class="link">https://www.facebook.com/KurdiskSkoleiNorg</div></div>
{FOOT}
</section>'''

explain=f'''<section class="page">
{HEAD(False)}
  <h1>حَرْفُ الواوِ <span class="ar" style="color:var(--red)">( و )</span></h1>
  <p class="sub">الدرس: نور و ماما — شرح الحرف وتمارين الكتابة</p>
  <div class="sec"><div class="sec-title"><span class="num">1</span>أشكالُ الحرف حسب موضعه في الكلمة</div>
    <div class="shapes" style="grid-template-columns:repeat(3,1fr)">
      <div class="shape"><div class="lbl">في أول الكلمة (منفصل)</div><div class="ch">و</div><div class="w"><em>و</em>َرْد</div></div>
      <div class="shape"><div class="lbl">في وسط الكلمة (متصل)</div><div class="ch">ـو</div><div class="w">مـ<em>ـو</em>ز</div></div>
      <div class="shape"><div class="lbl">في آخر الكلمة (متصل)</div><div class="ch">ـو</div><div class="w">دَلـ<em>ـو</em></div></div>
    </div>
    <div class="hint" style="margin:3mm 0 0">💡 <b>قاعدة مهمة:</b> حرف الواو يتّصل بالحرف الذي <b>قبله</b> فقط، ولا يتّصل أبدًا بالحرف الذي <b>بعده</b> — لذلك نترك مسافة بعده، مثل: <span class="ar" style="font-size:14pt">نور، موز، لوز</span>.</div>
  </div>
  <div class="sec"><div class="sec-title"><span class="num">2</span>أصواتُ الحرف القصيرة والطويلة</div>
    <div class="sounds">
      <div class="sbox short"><h3>الأصوات القصيرة (الحركات)</h3>
        <div class="row"><div><div class="s">وَ</div><div class="r">فتحة</div></div><div><div class="s">وُ</div><div class="r">ضمة</div></div><div><div class="s">وِ</div><div class="r">كسرة</div></div></div></div>
      <div class="sbox long"><h3>الأصوات الطويلة (المدود)</h3>
        <div class="row"><div><div class="s">وا</div><div class="r">مد بالألف</div></div><div><div class="s">وو</div><div class="r">مد بالواو</div></div><div><div class="s">وي</div><div class="r">مد بالياء</div></div></div></div>
    </div></div>
  <div class="sec"><div class="sec-title"><span class="num">3</span>كلماتٌ تحتوي حرف الواو</div>
    <div class="words">
      <div class="word"><div class="ar"><em>وَ</em>رْد</div><div class="pos">في الأول</div></div>
      <div class="word"><div class="ar"><em>وَ</em>لَد</div><div class="pos">في الأول</div></div>
      <div class="word"><div class="ar">مَـ<em>ـو</em>ْز</div><div class="pos">في الوسط</div></div>
      <div class="word"><div class="ar">نـ<em>ـو</em>ر</div><div class="pos">في الوسط</div></div>
      <div class="word"><div class="ar">لَـ<em>ـو</em>ْز</div><div class="pos">في الوسط</div></div>
      <div class="word"><div class="ar">دَلْـ<em>ـو</em></div><div class="pos">في الآخر</div></div>
      <div class="word"><div class="ar">خَـ<em>ـو</em>خ</div><div class="pos">في الوسط</div></div>
      <div class="word"><div class="ar"><em>وَ</em>جْه</div><div class="pos">في الأول</div></div>
    </div></div>
  <div class="sec"><div class="sec-title"><span class="num">4</span>ملاحظات لولي الأمر</div>
    <div class="plan" style="grid-template-columns:1fr">
      <div class="card"><ul style="columns:2">
        <li>ساعِد طفلك على نطق الحرف بصوت واضح.</li><li>الواو ليس لها نقاط.</li>
        <li>الواو لا تتصل بالحرف الذي بعدها.</li><li>اقرأ الكلمات معه وابحث عن الواو فيها.</li></ul></div>
    </div></div>
{FOOT.replace('<div class="foot">','<div class="foot" style="margin-top:auto">')}
</section>'''

kid=f'''<section class="page">
{HEAD()}
  <div class="kid-hero">
    <div class="L"><span>و</span></div>
    <div class="bubble">مرحبًا! <span class="emo">👋</span> أنا حرفُ <span class="ar">الواو</span><br>
      لي رأسٌ صغيرٌ مدوّر <span class="emo">⚪</span> وذيلٌ طويل <span class="emo">🐒</span><br>
      وليس عندي نقاط!</div>
  </div>
  <div class="kid-sec"><span class="emo">🔊</span> أسمعُ صوتي في هذه الكلمات</div>
  <div class="pics">
    <div class="pic"><div class="emo">🌹</div><div class="ar"><em>وَ</em>رْد</div></div>
    <div class="pic"><div class="emo">👦</div><div class="ar"><em>وَ</em>لَد</div></div>
    <div class="pic"><div class="emo">🍌</div><div class="ar">مَـ<em>ـو</em>ْز</div></div>
    <div class="pic"><div class="emo">💡</div><div class="ar">نـ<em>ـو</em>ر</div></div>
  </div>
  <div class="kid-sec"><span class="emo">🔍</span> أين أختبئُ في الكلمة؟</div>
  <div class="hide">
    <div class="hbox a"><div class="t1">في الأوّل</div><div class="emo">🌹</div><div class="ar"><em>و</em>رد</div><div class="dots"><i class="on"></i><i></i><i></i></div></div>
    <div class="hbox b"><div class="t1">في الوسط</div><div class="emo">🍌</div><div class="ar">مـ<em>ـو</em>ز</div><div class="dots"><i></i><i class="on"></i><i></i></div></div>
    <div class="hbox c"><div class="t1">في الآخر</div><div class="emo">🪣</div><div class="ar">دلـ<em>ـو</em></div><div class="dots"><i></i><i></i><i class="on"></i></div></div>
  </div>
  <div class="kid-sec"><span class="emo">🤝</span> أمسكُ يدَ الحرفِ الذي قبلي فقط</div>
  <div class="hint" style="font-size:12pt;text-align:center">أنا أمسكُ يدَ صديقي الذي <b>قبلي</b> <span class="emo">🤝</span> ولا أمسكُ يدَ الذي <b>بعدي</b> <span class="emo">✋</span>
    <div class="ar" style="font-size:26pt;line-height:1.5">نـ<span style="color:var(--red)">ـو</span> ر &nbsp;&nbsp; مـ<span style="color:var(--red)">ـو</span> ز</div></div>
  <div class="kid-sec"><span class="emo">🎵</span> أغيّرُ صوتي مع الحركات</div>
  <div class="snd">
    <div class="sn"><div class="ar">وَ</div><div class="x">فتحة ← «وَ» كما في وَرْد</div></div>
    <div class="sn"><div class="ar">وُ</div><div class="x">ضمة ← «وُ»</div></div>
    <div class="sn"><div class="ar">وِ</div><div class="x">كسرة ← «وِ»</div></div>
  </div>
  <div class="star"><span class="emo">⭐</span> قُلْ معي: وَ — وُ — وِ ... وَرْد! <span class="emo">⭐</span></div>
{FOOT}
</section>'''

sv=lambda inner:f'<svg viewBox="0 0 200 200">{inner}</svg>'
steps=f'''<section class="page">
{HEAD()}
  <div class="ws-top"><div class="n emo" style="font-size:18pt">✍️</div><div><h2>كيفَ أكتبُ حرفَ الواو؟</h2><p>ثلاثُ خطواتٍ سهلة</p></div></div>
  <div class="steps">
    <div class="st"><span class="no">1</span>
      {sv('<defs><clipPath id="c1"><rect x="100" y="0" width="100" height="103"/></clipPath></defs><text x="113" y="106" class="ghost">و</text><text x="113" y="106" class="ink" clip-path="url(#c1)">و</text><circle cx="124" cy="46" r="8" fill="#2F855A"/>')}
      <div class="cap">أبدأ من فوق <span class="emo">🟢</span><br>وأرسمُ رأسًا صغيرًا مدوّرًا</div></div>
    <div class="st"><span class="no">2</span>
      {sv('<text x="113" y="106" class="ink">و</text>')}
      <div class="cap">أنزلُ وأرسمُ ذيلًا<br>تحتَ السطر <span class="emo">↙️</span></div></div>
    <div class="st"><span class="no">3</span>
      {sv('<text x="113" y="106" class="ghost" style="fill:#1F2A37">و</text><text x="165" y="60" style="font-family:Noto Color Emoji;font-size:34px">✅</text>')}
      <div class="cap">انتهيت! <br>الواو ليس لها نقاط</div></div>
  </div>
  <div class="legend"><span><b>الحرف الأسود:</b> انظر إليه</span><span><b>الحرف المنقّط:</b> مرِّر القلم فوقه</span><span><b>المكان الفارغ:</b> اكتب وحدك</span></div>
  {''.join(lr('و') for _ in range(6))}
  <div class="star"><span class="emo">⭐</span> أحسنت! الرأس صغير والذيل تحت السطر <span class="emo">⭐</span></div>
{FOOT}
</section>'''

shapes=f'''<section class="page">
{HEAD()}
  <div class="ws-top"><div class="n emo" style="font-size:18pt">✏️</div><div><h2>أكتبُ أشكالَ حرفِ الواو</h2><p>منفصلة — متصلة</p></div></div>
  <div class="hint">✏️ تتبّع الحرف المنقّط، ثم اكتبه وحدك في آخر السطر. ابدأ دائمًا من اليمين <span class="emo">⬅️</span></div>
  <div class="rowlbl"><span class="tag">و</span> منفصلة — مثل <span class="ar" style="font-size:15pt">وَرْد 🌹</span></div>
  {lr('و',2,4,2)}{lr('و',1,4,3)}{lr('و',1,3,4)}
  <div class="rowlbl"><span class="tag">ـو</span> متصلة بما قبلها — مثل <span class="ar" style="font-size:15pt">مَوْز 🍌</span></div>
  {lr('ـو',2,4,2)}{lr('ـو',1,4,3)}{lr('ـو',1,3,4)}
{FOOT}
</section>'''

words=f'''<section class="page">
{HEAD()}
  <div class="ws-top"><div class="n emo" style="font-size:18pt">🖍️</div><div><h2>أكتبُ كلماتٍ فيها حرفُ الواو</h2><p>أنظرُ إلى الصورة، أقرأ الكلمة، ثم أكتبها</p></div></div>
  {wr('🌹','ورد')}{wr('👦','ولد')}{wr('🍌','موز')}{wr('💡','نور')}{wr('🪣','دلو')}
  <div class="kid-sec" style="margin-top:4mm"><span class="emo">🧩</span> أكملُ الكلمةَ بحرفِ الواو المناسب <span class="ar" style="font-size:15pt">( و / ـو )</span></div>
  <div class="fill">
    <div class="fb"><div class="emo">👦</div><div class="ar"><span class="gap"></span>لد</div></div>
    <div class="fb"><div class="emo">🍌</div><div class="ar">مـ<span class="gap"></span>ز</div></div>
    <div class="fb"><div class="emo">💡</div><div class="ar">نـ<span class="gap"></span>ر</div></div>
  </div>
  <div class="star"><span class="emo">🌟</span> رائع! أنت الآن تعرف حرف الواو <span class="emo">🌟</span></div>
{FOOT}
</section>'''

pages=[program,explain,kid,steps,shapes,words]
body='\n'.join(pages); n=body.count('صفحة §'); k=iter(range(1,n+1))
body=re.sub('صفحة §',lambda m:f'صفحة {next(k)} من {n}',body)
open('waw.html','w').write(f'<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>حرف الواو</title>{CSS}</head><body>{body}</body></html>')
