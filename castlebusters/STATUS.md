# Castle Busters — حالة المشروع

ملخص متابع للمشروع، محدَّث في هذا المستودع بدل ملف PDF منفصل، ليبقى تاريخ التقدم في الـ git log.

## 1. فكرة اللعبة

لعبة موبايل حقيقية **PvP 1v1 Real-time**، مستوحاة من إعلان TikTok بعنوان "Castle Busters".

**الآليات الأساسية:**
- تضاريس رملية قابلة للتدمير (destructible sand terrain)
- قصف بالصواريخ (rocket bombardment) يدمر التضاريس فعلياً
- صناديق مضاعِفة (multiplier crates) تظهر أثناء اللعب
- منافسة فعلية بزمن حقيقي بين لاعبين (playable ad حقيقي بين لاعبين شخصين، وليست مجرد إعلان تفاعلي)

**متطلبات إضافية:**
- لعبة موبايل أصلية حقيقية (Unity/Native)، وليست نموذج ويب أولي
- إطلاق فعلي عالمي: لاعبون حقيقيون من كل الدول يلعبون ضد بعض (اختبار محلي أولاً)
- تمثيل اللاعبين بعلم/لون دولتهم، مع خرائط تُظهر تمثيل الدول
- متجر داخل اللعبة: عناصر تجميلية (cosmetics)، رموز تقدّم (progression symbols)، صواريخ

**قرار تطوير:** يقوم Claude بتطوير المشروع بنفسه بمساعدة Unity، بدلاً من توظيف مطوّر — المستخدم اختار أن يتعلم لا أن يبرمج بنفسه.

## 2. بيئة العمل (على MacBook المستخدم)

- ✅ Unity Hub مثبّت
- ✅ Unity 6.3 LTS (6000.3.22f1) مثبّت
- ✅ دعم البناء لـ: Android, iOS, macOS مفعّل
- ✅ مشروع Unity باسم "castlebusters" في `/Users/kroren/castlebusters`، بقالب Universal 2D (URP 2D Renderer)

> ملاحظة مهمة: هذه الجلسة (Claude Code على الويب) تعمل داخل حاوية سحابية معزولة، **وليس لها وصول إلى MacBook للمستخدم أو إلى Unity Editor نفسه**. المستودع `sadoun77/sadoun77` هو المكان الوحيد المتاح هنا. لذلك تم كتابة نظام تدمير التضاريس كسكربتات C# حقيقية وقابلة للاستخدام مباشرة تحت `castlebusters/Assets/`، لينقلها المستخدم إلى مشروع Unity المحلي (أنظر قسم "كيفية الدمج" أدناه).

## 3. ما تم إنجازه في هذه الجلسة: نظام تدمير التضاريس

أول لبنة تقنية أساسية في اللعبة — **destructible terrain system** — تم بناؤها بالكامل:

### `Assets/Scripts/Terrain/DestructibleTerrain2D.cs`
المكوّن الرئيسي. يحمل التضاريس كـ `Texture2D` قابل للتعديل (القناة alpha تحدد صلب/فارغ)، ويعرض `SpriteRenderer` منها. عند استدعاء:

```csharp
terrain.DestroyCircle(worldPosition, radius);
```

يُصفّر alpha البكسلات ضمن دائرة التفجير، ثم يعيد بناء `PolygonCollider2D` تلقائياً (مُجمَّع على نفس الفريم لتفادي إعادة البناء عدة مرات عند انفجارات متزامنة) بحيث يطابق الفيزياء الشكل المرئي الجديد تماماً.

### `Assets/Scripts/Terrain/TerrainContourTracer.cs`
خوارزمية استخراج المضلعات (contours) من شبكة ثنائية صلب/فارغ: تجمع حواف كل خلية صلبة المواجهة لخلية فارغة، ثم تخيط هذه الحواف زاوية-إلى-زاوية لتكوّن حلقات مغلقة (جزيرة تضاريس منفصلة = مضلع منفصل). تدعم بذلك انفصال التضاريس لعدة قطع بعد التدمير المتكرر، وتبسّط النقاط المتراصفة (collinear) لتقليل عدد رؤوس الـ collider.

### `Assets/Scripts/Weapons/RocketProjectile2D.cs`
صاروخ بسيط بـ `Rigidbody2D`: يُطلق باتجاه ما (`Launch(direction)`)، وعند الاصطدام يستدعي `DestroyCircle` على أي `DestructibleTerrain2D` أصابه، ثم يُدمَّر نفسه (مع إمكانية تفعيل تأثير انفجار بصري).

### `Assets/Editor/GenerateTestTerrainTexture.cs`
أداة Editor (قائمة `Tools > Castle Busters > Generate Test Terrain Texture`) تولّد تكستشر رملية بسيطة للاختبار فوراً، دون الحاجة لأصول فنية جاهزة.

## 4. كيفية الدمج في مشروع Unity المحلي

1. انسخ مجلد `castlebusters/Assets/Scripts` و `castlebusters/Assets/Editor` بالكامل إلى `/Users/kroren/castlebusters/Assets/` (استبدال/دمج).
2. افتح Unity Editor، اسمح له بإعادة الترجمة (compile) — لا توجد أخطاء متوقعة.
3. من القائمة: `Tools > Castle Busters > Generate Test Terrain Texture` لتوليد تكستشر رملية تجريبية في `Assets/Textures/TestSandTerrain.png`.
4. أنشئ GameObject فارغ باسم "Terrain"، أضف إليه:
   - `SpriteRenderer` (يُضاف تلقائياً كمتطلب)
   - `PolygonCollider2D` (يُضاف تلقائياً كمتطلب)
   - `DestructibleTerrain2D`، واسحب `TestSandTerrain` في حقل `Source Texture`
5. أنشئ prefab صاروخ: GameObject به `Rigidbody2D` (Gravity Scale = 0 إن أردت خطاً مستقيماً)، `Collider2D` (isTrigger أو صلب)، وسكربت `RocketProjectile2D`.
6. عند التشغيل، أطلق الصاروخ باتجاه التضاريس (`rocket.Launch(direction)`) وراقب ظهور حفرة انفجار حقيقية مع فيزياء متطابقة معها.

**ملاحظة على الأداء:** `colliderGridStep` في `DestructibleTerrain2D` يتحكم بدقة الـ collider مقابل التكلفة (القيمة الافتراضية 2 تعني أخذ عيّنة كل بكسلين). ارفعها إذا كانت التضاريس كبيرة والتحديث بطيئاً.

**قيود معروفة في هذه النسخة الأولى:**
- لا يوجد دعم رسمي لـ "ثقوب داخلية" منفصلة بصرياً عن الفراغ الخارجي عند PolygonCollider2D (كل مضلع يُعامل ككتلة صلبة مستقلة) — حالة نادرة الحدوث مع انفجارات دائرية عادية.
- التدمير حالياً محلي (client-side) فقط؛ لا مزامنة شبكة بعد — ذلك يأتي مع نظام الـ multiplayer العالمي المذكور في المتطلبات الإضافية.

## 5. الخطوة القادمة (لم تبدأ بعد)

بعد التأكد من أن نظام التدمير يعمل داخل Unity على الجهاز المحلي:
- ربط صندوق مضاعِف (`multiplier crates`) بسيط يظهر عشوائياً فوق التضاريس.
- بنية اللاعبين الأساسية (PlayerController) لإطلاق الصواريخ يدوياً بزمن حقيقي.
- التخطيط لطبقة الشبكة (multiplayer عالمي حقيقي) — قرار التقنية (Netcode for GameObjects / Photon / خادم مخصص) لم يُتخذ بعد ويحتاج نقاشاً منفصلاً.

## 6. كيف تُكمل العمل في جلسة جديدة

هذا المستودع (`sadoun77/sadoun77`, فرع `claude/project-start-ffho87`) يحتفظ بتاريخ التقدّم عبر git — لا حاجة لنسخ ولصق وثيقة PDF يدوياً في كل مرة. فقط أشر إلى هذا الملف (`castlebusters/STATUS.md`) في بداية أي محادثة جديدة مع Claude ليكمل من حيث توقف.
