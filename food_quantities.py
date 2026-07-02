# ============================================================
# food_quantities.py
# كل حاجة خاصة بتصنيف food_quantities
# ============================================================
#
# المعادلات هنا مبنية على مصادر عالمية معتمدة:
# - البروتين:  ISSN Position Stand: Protein and Exercise (2017)
# - البروتين وقت الديفيسيت: ISSN Position Stand: Diets and Body Composition (2017)
# - الدهون:    Acceptable Macronutrient Distribution Range - IOM / Dietary Guidelines for Americans
# - الكارب:    ISSN / ACSM Guidelines for Carbohydrate Intake in Athletes
# - المياه:    EFSA Scientific Opinion on Water / IOM Dietary Reference Intakes (~35 مل لكل كيلو تقريبًا)
# - الألياف:   USDA Dietary Guidelines for Americans (14g لكل 1000 كالوري)
# - الكرياتين: ISSN Position Stand: Creatine Supplementation and Exercise
# - الكافيين:  FDA / EFSA safe daily intake (حتى 400 مجم لليوم للشخص السليم البالغ)
#
# ملحوظة: القيم دي متوسطات علمية عامة مش استشارة طبية، ولو فيه ملاحظات طبية
# (medicalNotes) لازم الشخص يرجع لدكتور/أخصائي تغذية قبل ما يطبق أي رقم فيها.
# ============================================================

FOOD_QUANTITIES_ENTITIES = {
    "calories": ["calories", "كالوري", "سعرات", "السعرات"],
    "protein": ["protein", "بروتين"],
    "carbs": ["carb", "carbohydrates", "كارب", "كربوهيدرات", "نشويات"],
    "fats": ["fats", "دهون"],
    "water": ["water", "مية", "مياه", "سوائل"],
    "fiber": ["fiber", "ألياف"],
    "creatine": ["creatine", "كرياتين"],
    "caffeine": ["caffeine", "كافيين", "قهوة"],
    "vitamins": ["vitamin", "فيتامين"],
}


def DESCRIPTION(entity="عنصر معين؟"):
    return f"عايزني احسبلك احتياجك اليومي من {entity}"


# ============================================================
# Helpers - قراءة بيانات اليوزر بأمان
# ============================================================

def _get(user_data, key, default=None):
    """بيرجع القيمة من user_data لو موجودة، أو الديفولت لو مش موجودة/None"""
    if not user_data:
        return default
    val = user_data.get(key, default)
    return default if val is None else val


def _norm(value):
    """توحيد شكل النص عشان نقارن الـ enums (gender, activityLevel, dietType, dietGoal)"""
    if not value:
        return ""
    return str(value).strip().lower().replace("-", "_").replace(" ", "_")


def _has_user_data(user_data):
    """بنتأكد إن فيه بيانات كفاية للحساب (لازم وزن على الأقل)"""
    return bool(user_data) and _get(user_data, "weightKg") is not None


# ============================================================
# الحسابات الأساسية
# ============================================================

def calculate_protein(user_data):
    """
    بروتين بناءً على هدف اليوزر (دايت جول) ووزنه/كتلته العضلية.
    المصدر: ISSN Position Stand - Protein and Exercise (2017)
    - بناء عضل/محافظة عليه: 1.6 - 2.0 g/kg من وزن الجسم
    - في فترة نزول وزن (ديفيسيت) لحماية الكتلة العضلية: 2.3 - 3.1 g/kg من الـ lean mass
    - نشاط خفيف/عادي (مش رياضي بشكل جدي): 1.2 - 1.6 g/kg كحد أدنى معقول
    """
    weight = _get(user_data, "weightKg", 70)
    lean_mass = _get(user_data, "leanMass")
    goal = _norm(_get(user_data, "dietGoal"))
    activity = _norm(_get(user_data, "activityLevel"))

    is_losing = any(k in goal for k in ["loss", "lose", "cut", "deficit", "نزول", "خساره", "خسارة"])
    is_gaining = any(k in goal for k in ["gain", "muscle", "bulk", "زياده", "زيادة", "تضخيم"])
    is_active = any(k in activity for k in ["active", "high", "athlete", "very"])

    if is_losing:
        # حماية الكتلة العضلية وقت الديفيسيت - نحسب على الـ lean mass لو متوفرة
        base = lean_mass if lean_mass else weight * 0.8  # تقدير تقريبي لو الـ lean mass مش موجودة
        low, high = 2.3, 2.8
        grams_low = round(base * low)
        grams_high = round(base * high)
        basis = "الكتلة الخالية من الدهون (Lean Mass)"
    elif is_gaining:
        low, high = 1.6, 2.2
        grams_low = round(weight * low)
        grams_high = round(weight * high)
        basis = "وزن الجسم الكلي"
    else:
        low, high = (1.4, 1.8) if is_active else (1.2, 1.6)
        grams_low = round(weight * low)
        grams_high = round(weight * high)
        basis = "وزن الجسم الكلي"

    target = round((grams_low + grams_high) / 2)
    calories = target * 4

    return {
        "low": grams_low,
        "high": grams_high,
        "target": target,
        "calories": calories,
        "basis": basis,
        "range_per_kg": (low, high),
    }


def calculate_fats(user_data):
    """
    الدهون كنسبة من السعرات اليومية.
    المصدر: Acceptable Macronutrient Distribution Range (IOM) / Dietary Guidelines for Americans
    - نظام متوازن: 20% - 35% من السعرات
    - كيتو / لو كارب: نسبة أعلى بكتير (65% - 75%) عشان الجسم يعتمد عليها كمصدر طاقة أساسي
    - حد أدنى بيولوجي مهم للهرمونات: تقريبًا 0.5 - 1 g/kg من وزن الجسم مهما كان النظام
    """
    weight = _get(user_data, "weightKg", 70)
    tdee = _get(user_data, "tdee") or _get(user_data, "dailyCalorieTarget", 2200)
    diet_type = _norm(_get(user_data, "dietType"))

    is_keto = "keto" in diet_type or "كيتو" in diet_type
    is_low_carb = "low_carb" in diet_type or "لوكارب" in diet_type or "لو_كارب" in diet_type

    if is_keto:
        pct_low, pct_high = 0.65, 0.75
    elif is_low_carb:
        pct_low, pct_high = 0.35, 0.45
    else:
        pct_low, pct_high = 0.20, 0.35

    cal_low = tdee * pct_low
    cal_high = tdee * pct_high
    grams_low = round(cal_low / 9)
    grams_high = round(cal_high / 9)

    # حد أدنى بيولوجي - متنزلش تحته حتى لو النظام قليل دهون جدًا
    min_biological = round(weight * 0.5)
    if grams_low < min_biological:
        grams_low = min_biological
        if grams_high < grams_low:
            grams_high = grams_low + 10

    target = round((grams_low + grams_high) / 2)

    return {
        "low": grams_low,
        "high": grams_high,
        "target": target,
        "calories": target * 9,
        "pct_range": (pct_low, pct_high),
    }


def calculate_carbs(user_data, protein_result=None, fats_result=None):
    """
    الكارب = باقي السعرات بعد البروتين والدهون.
    المصدر: ISSN / ACSM Carbohydrate Guidelines for Athletes
    بنتأكد كمان إن القيمة منطقية حسب مستوى النشاط:
    - نشاط خفيف: 3-5 g/kg
    - نشاط متوسط/رياضة منتظمة: 5-7 g/kg
    - نشاط عالي/تمرين مكثف: 6-10 g/kg
    """
    weight = _get(user_data, "weightKg", 70)
    tdee = _get(user_data, "tdee") or _get(user_data, "dailyCalorieTarget", 2200)
    activity = _norm(_get(user_data, "activityLevel"))
    diet_type = _norm(_get(user_data, "dietType"))

    protein_result = protein_result or calculate_protein(user_data)
    fats_result = fats_result or calculate_fats(user_data)

    if "high" in activity or "active" in activity or "very" in activity:
        low_gkg, high_gkg = 6, 10
    elif "moderate" in activity or "medium" in activity:
        low_gkg, high_gkg = 5, 7
    else:
        low_gkg, high_gkg = 3, 5

    is_keto = "keto" in diet_type or "كيتو" in diet_type
    if is_keto:
        # الكيتو بيكسر قاعدة النشاط عمدًا - الكارب بيفضل منخفض جدًا مهما كان مستوى التمرين
        grams_low = round(weight * 0.5)
        grams_high = round(weight * 1.0)
    else:
        # الكارب = باقي السعرات بعد أعلى وأقل حد من البروتين والدهون - كده المدى بيكون واقعي وضيق
        remaining_cal_min = tdee - protein_result["high"] * 4 - fats_result["high"] * 9
        remaining_cal_max = tdee - protein_result["low"] * 4 - fats_result["low"] * 9
        grams_low = max(round(remaining_cal_min / 4), 0)
        grams_high = max(round(remaining_cal_max / 4), grams_low)

    target = round((grams_low + grams_high) / 2)

    return {
        "low": grams_low,
        "high": grams_high,
        "target": target,
        "activity_range_per_kg": (low_gkg, high_gkg),
    }


def calculate_water(user_data):
    """
    المياه اليومية.
    المصدر: EFSA / IOM Dietary Reference Intakes - تقريبًا 30-35 مل لكل كيلو من وزن الجسم
    بنزود كمية إضافية لو النشاط عالي (تعويض العرق).
    """
    weight = _get(user_data, "weightKg", 70)
    activity = _norm(_get(user_data, "activityLevel"))

    base_ml = weight * 35

    if "high" in activity or "active" in activity or "very" in activity:
        extra_ml = 750
    elif "moderate" in activity or "medium" in activity:
        extra_ml = 400
    else:
        extra_ml = 0

    total_ml = base_ml + extra_ml
    liters = round(total_ml / 1000, 1)

    return {
        "ml": round(total_ml),
        "liters": liters,
        "extra_for_activity_ml": extra_ml,
    }


def calculate_fiber(user_data):
    """
    الألياف اليومية.
    المصدر: USDA Dietary Guidelines for Americans - 14 جم ألياف لكل 1000 كالوري
    مع حد أدنى تقريبي حسب الجندر (Adequate Intake - IOM): رجالة ~38g / ستات ~25g
    """
    tdee = _get(user_data, "tdee") or _get(user_data, "dailyCalorieTarget", 2200)
    gender = _norm(_get(user_data, "gender"))

    from_calories = round((tdee / 1000) * 14)
    floor = 38 if gender.startswith("m") else 25

    target = max(from_calories, floor - 5)  # مانخليش الرقم يبعد جدًا عن الحد الأدنى المعروف

    return {
        "target": target,
        "floor_reference": floor,
    }


def calculate_creatine(user_data):
    """
    الكرياتين مونوهيدرات.
    المصدر: ISSN Position Stand: Creatine Supplementation and Exercise (2017)
    - جرعة محافظة يومية: 3-5 جم لمعظم الناس (مش لازم تتحسب على الوزن أصلاً)
    - جرعة محسوبة أدق: تقريبًا 0.03 جم/كجم يوميًا
    - مرحلة تحميل اختيارية: 0.3 جم/كجم لمدة 5-7 أيام (مش ضرورية)
    """
    weight = _get(user_data, "weightKg", 70)
    calculated = round(weight * 0.03, 1)
    maintenance = min(max(calculated, 3), 5)
    loading = round(weight * 0.3)

    return {
        "maintenance_g": maintenance,
        "loading_g_per_day": loading,
    }


def calculate_caffeine(user_data):
    """
    الكافيين - الحد اليومي الآمن.
    المصدر: FDA / EFSA - حتى 400 مجم يوميًا للشخص البالغ السليم (تقريبًا 3-6 مجم/كجم)
    لو فيه ملاحظات طبية تخص القلب أو الحمل، بننزل الرقم وبننصح بمراجعة دكتور.
    """
    weight = _get(user_data, "weightKg", 70)
    medical_notes = _norm(_get(user_data, "medicalNotes", ""))

    safe_upper = min(round(weight * 6), 400)

    has_caution_flag = any(
        k in medical_notes for k in ["heart", "قلب", "pregnan", "حمل", "anxiety", "قلق", "ضغط"]
    )
    if has_caution_flag:
        safe_upper = min(safe_upper, 200)

    return {
        "safe_upper_mg": safe_upper,
        "capped_by_medical_notes": has_caution_flag,
    }


# ============================================================
# Formatters - تحويل الأرقام لرسالة عربية مفهومة
# ============================================================

def _format_calories(user_data):
    tdee = _get(user_data, "tdee")
    target = _get(user_data, "dailyCalorieTarget")
    goal = _get(user_data, "dietGoal", "")

    if not tdee and not target:
        return "محتاج بيانات وزن/طول/نشاط أدق عشان أحسبلك السعرات، ابعتلي بروفايلك الصحي كامل."

    lines = []
    if tdee:
        lines.append(f"معدل حرقك اليومي (TDEE) تقريبًا: {round(tdee)} سعرة")
    if target:
        lines.append(f"احتياجك اليومي المستهدف بناءً على هدفك ({goal or 'الحفاظ على الوزن'}): {round(target)} سعرة")

    return (
        "دي حسبة السعرات بتاعتك:\n- " + "\n- ".join(lines) +
        "\n\nالرقم ده متوسط، لو حسيت إنك بتزود أو بتنزل بسرعة غير متوقعة كلمني نعدله."
    )


def _format_protein(user_data):
    p = calculate_protein(user_data)
    low, high = p["range_per_kg"]
    return (
        f"احتياجك اليومي من البروتين تقريبًا بين {p['low']} و {p['high']} جم "
        f"(يعني حوالي {p['target']} جم في المتوسط)، محسوبة على أساس {low}-{high} جم لكل كيلو من {p['basis']}.\n\n"
        f"ده معتمد على توصيات الجمعية الدولية لتغذية الرياضة (ISSN).\n"
        f"حاول توزعهم على 3-4 وجبات كل وحدة فيها 20-40 جم بروتين عشان الجسم يستفيد بيهم بشكل أفضل."
    )


def _format_fats(user_data):
    f = calculate_fats(user_data)
    pct_low, pct_high = f["pct_range"]
    return (
        f"احتياجك اليومي من الدهون الصحية تقريبًا بين {f['low']} و {f['high']} جم "
        f"(حوالي {int(pct_low*100)}%-{int(pct_high*100)}% من سعراتك اليومية).\n\n"
        f"ركز على مصادر الدهون الصحية زي زيت الزيتون، الأفوكادو، المكسرات، والأسماك الدهنية، "
        f"وابعد قدر الإمكان عن الدهون المتحولة (المقليات الجاهزة والسمن الصناعي)."
    )


def _format_carbs(user_data):
    p = calculate_protein(user_data)
    f = calculate_fats(user_data)
    c = calculate_carbs(user_data, p, f)
    low_gkg, high_gkg = c["activity_range_per_kg"]
    return (
        f"احتياجك اليومي من الكاربوهيدرات تقريبًا بين {c['low']} و {c['high']} جم، "
        f"ده بيغطي احتياجك للطاقة بعد ما حسبنا البروتين والدهون.\n\n"
        f"بناءً على مستوى نشاطك، المعدل الرياضي العام بيكون في حدود {low_gkg}-{high_gkg} جم لكل كيلو من وزنك. "
        f"فضّل المصادر المعقدة زي الشوفان، الأرز البني، البطاطا، والخضار النشوية."
    )


def _format_water(user_data):
    w = calculate_water(user_data)
    extra_note = ""
    if w["extra_for_activity_ml"]:
        extra_note = f" (زودنا {w['extra_for_activity_ml']} مل إضافية عشان مستوى نشاطك)"
    return (
        f"احتياجك اليومي من المية تقريبًا {w['liters']} لتر (حوالي {w['ml']} مل){extra_note}.\n\n"
        f"القيمة دي بتزيد في الجو الحر أو لو بتتعرق كتير في التمرين، وبتقل شوية لو بتاكل خضار وفاكهة كتير "
        f"(لأنها بتديك سوائل من غير ما تشرب)."
    )


def _format_fiber(user_data):
    f = calculate_fiber(user_data)
    return (
        f"احتياجك اليومي من الألياف تقريبًا {f['target']} جم.\n\n"
        f"أهم مصادرها: الخضار الورقي، البقوليات (عدس، فول، حمص)، الشوفان، والفواكه بقشرها. "
        f"الألياف بتساعد في الشبع، وصحة الجهاز الهضمي، والتحكم في نسبة السكر في الدم."
    )


def _format_creatine(user_data):
    c = calculate_creatine(user_data)
    return (
        f"الجرعة اليومية الموصى بيها من الكرياتين مونوهيدرات: {c['maintenance_g']} جم يوميًا، "
        f"وده رقم ثابت تقريبًا معظم الوقت مهما كان وزنك (لأن الجرعة الفعالة علميًا بتتشبع عند حد معين).\n\n"
        f"لو حابب تستعجل النتيجة، ممكن تعمل مرحلة تحميل اختيارية بجرعة أعلى (~{c['loading_g_per_day']} جم) "
        f"مقسمة على اليوم لمدة 5-7 أيام بس، لكنها مش ضرورية أبدًا وممكن تستغنى عنها وتاخد الجرعة العادية على طول."
    )


def _format_caffeine(user_data):
    c = calculate_caffeine(user_data)
    caution = ""
    if c["capped_by_medical_notes"]:
        caution = "\n\nلاحظنا إن عندك ملاحظات طبية ممكن تتأثر بالكافيين، فالرقم ده اتحسب بحذر أكتر - يفضل تتأكد من دكتورك."
    return (
        f"الحد الآمن يوميًا من الكافيين بالنسبالك تقريبًا {c['safe_upper_mg']} مجم "
        f"(يعني حوالي {round(c['safe_upper_mg']/95)} كوباية قهوة تقريبًا، بافتراض إن الكوباية فيها ~95 مجم).{caution}\n\n"
        f"حاول متاخدش كافيين قريب من موعد نومك بـ 6 ساعات عشان مايأثرش على جودة نومك."
    )


def _format_vitamins(user_data):
    gender = _norm(_get(user_data, "gender"))
    is_female = gender.startswith("f")
    extra = "خصوصًا الحديد وفيتامين د وحمض الفوليك، دول بيكونوا مهمين أكتر للستات." if is_female else "فيتامين د وB12 مهمين خصوصًا لو نشاطك عالي أو نظامك الغذائي فيه قيود."
    return (
        "الفيتامينات صعب تتحسب برقم دقيق من غير تحليل دم، لكن في نقط عامة مهمة ليك:\n"
        "- فيتامين D: مهم للعظام والهرمونات، وأغلب الناس عندها نقص فيه خصوصًا لو التعرض للشمس قليل.\n"
        "- فيتامين B12: مهم للطاقة، وبيكون ناقص أكتر عند اللي بياكلوا نباتي بالكامل.\n"
        "- فيتامين C: مهم للمناعة والتعافي بعد التمرين.\n\n"
        f"{extra}\n\n"
        "لو حابب رقم دقيق، الأفضل تعمل تحليل دم شامل وتشوف نتيجته مع دكتور أو أخصائي تغذية."
    )


_FORMATTERS = {
    "calories": _format_calories,
    "protein": _format_protein,
    "fats": _format_fats,
    "carbs": _format_carbs,
    "water": _format_water,
    "fiber": _format_fiber,
    "creatine": _format_creatine,
    "caffeine": _format_caffeine,
    "vitamins": _format_vitamins,
}


# ============================================================
# Handler
# ============================================================

def handle(user_input, entity, is_short_func, user_data=None):
    """الـ handler الخاص بـ food_quantities - بيحسب بناءً على HealthProfileData بتاع اليوزر"""
    user_data = user_data or {}

    if not entity:
        return "بتسأل عن إيه بالظبط؟ بروتين؟ كارب؟ دهون صحية؟ سعرات؟"

    if is_short_func(user_input):
        return f"هل عايز تعرف احتياجك من {entity}؟"

    formatter = _FORMATTERS.get(entity)
    if not formatter:
        return f"[food_quantities | entity: {entity}] - البيانات مش موجودة"

    # كافيين وفيتامينات مش محتاجين وزن بالضرورة، لكن باقي الحسابات محتاجة weightKg على الأقل
    if entity not in ("vitamins","creatine") and not _has_user_data(user_data):
        return (
            f"عشان أحسبلك احتياجك الدقيق من {entity} محتاج بيانات صحية عنك الأول "
            f"(الوزن، الطول، الجندر، مستوى النشاط، وهدفك)، تقدر تكمل بيانات البروفايل الصحي بتاعك وارجعلي؟"
        )

    return formatter(user_data)