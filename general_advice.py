# ============================================================
# general_advice.py
# ============================================================
import random
from thefuzz import fuzz

def DESCRIPTION (entity="الأكل أو الجيم"): 
   if entity is None or entity == "":
        entity = "الأكل أو الجيم"
   return f"عايز نصيحة عامة تفيدك في {entity}؟ 💡"
GENERAL_ADVICE_ENTITIES = {
    "الأكل": [
        "اكل", "تغذية", "وجبة", "نظام", "دايت", "diet", "nutrition",
        "food", "meal", "سعرات", "calories", "بروتين", "protein", "غذاء","اخس","weight","وزن"
    ],
    "التمارين": [
        "تمرين", "رياضة", "جيم", "workout", "exercise", "training",
        "تدريب", "كارديو", "cardio", "سيشن", "session", "تمارين","عضل","muscles"
    ],
    "الالتزام بجدولك": [
        "التزم", "داوم", "استمر", "اكمل", "بدأت وبطلت", "مش قادر",
        "اكمل", "استمر", "تحفيز", "motivation", "consistent","اواظب",
        "بطلت", "فضلت", "صعب", "مش بلتزم", "تكاسلت", "كسل" ,"continue" ,"tied" ,"go on","keep going"
    ],
}

GENERAL_ADVICE_DATA = {

    "food_general": [
        "البروتين أهم عنصر في تغذية الرياضي، احرص على 1.6-2.2 جرام لكل كيلو من وزنك",
        "المية مهمة جداً، اشرب على الأقل 8 أكواب يومياً وزود لو بتتعرق كتير",
        "الكارب مش عدوك، هو مصدر طاقة جسمك الأساسي للتمرين",
        "الدهون الصحية (زيت زيتون، افوكادو، مكسرات) مهمة لصحة الهرمونات",
        "الخضار والفواكه مش بس فيتامينات، فيها ألياف بتحسن الهضم وبتخليك تشبع",
        "قلل من الأكل المصنع والمعلب قدر الإمكان",
        "الوجبة قبل التمرين بساعتين: كارب معتدل + بروتين خفيف + دهون قليلة",
        "الوجبة بعد التمرين: بروتين + كارب عشان تعوض الطاقة وتبني العضل",
        "السكر الزيادة عدوك الأول في الدايت، حتى عصاير الفاكهة فيها سكر كتير",
        "الأكل البطيء بيساعدك تاكل أقل وتشبع أسرع",
        "الطبخ في البيت أصح وأرخص وأكتر تحكم من الأكل بره",
        "المكملات الغذائية مش سحر، هي بس تكملة للأكل الصح مش بديل عنه",
        "حساب السعرات لفترة بيعلمك تقدر الكميات حتى لو مش هتعمله طول عمرك",
        "الجوع الشديد عدوك، خلي وجبات منتظمة عشان متاكلش أكتر من اللازم",
        "البروتين من مصادر طبيعية (فراخ، بيض، لبن) أفضل من البروتين البودر لو بتاكل كويس",
    ],

    "food_commitment": [
        "جهز أكلك من أول الأسبوع (Meal Prep) عشان متلاقيش نفسك بتاكل أي حاجة",
        "متحرمش نفسك من كل حاجة بتحبها، خلي 80% صح و20% مرونة",
        "لو وقعت في أكل وحش يوم، مش ده نهاية الدنيا، ارجع لنظامك في الوجبة الجاية",
        "التغيير التدريجي أفضل من التغيير المفاجئ، ابدأ بتغيير حاجة واحدة في الأسبوع",
        "اتعلم تقرأ الملصقات الغذائية عشان تعرف إيه اللي بتاكله بالظبط",
        "الصور قبل وبعد ومتابعة الأرقام بتحفزك تكمل",
        "وجود شخص تاني معاك على نفس النظام بيساعدك تلتزم أكتر",
        "لو بتاكل بره كتير، اتعلم تختار من القايمة بذكاء مش لازم تكسر نظامك",
        "الملل من الأكل الصح غالباً بيجي من تكرار نفس الأكل، جرب وصفات جديدة",
        "ذكّر نفسك بهدفك كل يوم، إيه اللي خلاك تبدأ النظام ده؟",
    ],

    "exercise_general": [
        "الإحماء قبل التمرين مش اختياري، 5-10 دقايق بيحموك من الإصابات",
        "النوم الكافي (7-9 ساعات) مهم زي التمرين نفسه، العضل بيتبني في النوم",
        "الراحة بين السيشنز مهمة، العضلة محتاجة 48 ساعة على الأقل",
        "التدرج في الوزن أساسي، زود 5-10% بس كل أسبوعين",
        "ركز على الفورم الصح قبل ما تزود الوزن",
        "التمرين المركب (سكوات، ديدليفت، بنش) أهم من الـ isolation في بناء العضل",
        "التنفس الصح في التمرين مهم، زفير في أصعب جزء من الحركة",
        "الهيدريشن أثناء التمرين مهم، اشرب كل 15-20 دقيقة",
        "تمارين الكور بتحمي ضهرك في كل التمارين التانية",
        "سجل تمارينك عشان تعرف إنت بتتقدم ولا لأ",
        "لو حاسس بألم حاد أثناء التمرين، وقف فوراً",
        "الإستريتش بعد التمرين بيحسن المرونة وبيقلل صلابة العضل",
        "التبريد بعد التمرين بيساعد على تسريع الاستشفاء"
    ],

    "exercise_commitment": [
        "الاتساق أهم من الشدة، 3 أيام منتظمين أفضل من 6 أيام ومتقطعين",
        "لو مش حاسس بتقدم، مش معناه إنك مش بتتقدم، التغيير بيبان على المدى البعيد",
        "ابدأ بأهداف صغيرة وقابلة للتحقيق، مش هدف ضخم بيخليك تحبط",
        "التمرين في نفس الوقت كل يوم بيساعدك تلتزم أكتر ويبقى عادة",
        "لو مش مدفعك التمرين، جرب نوع تاني من الرياضة، مش لازم الجيم",
        "وجود تريننج باتنر بيخليك تروح حتى لو مش نفسك",
        "لو فاتك يوم أو اتنين، ارجع من غير ما تحس بذنب وكمل",
        "تتبع جسمك بالصور والمقاسات كل شهر بيحفزك تكمل",
        "الموسيقى المفضلة ليك أثناء التمرين بتحسن الأداء والاستمتاع",
        "فكر في التمرين كوقت ليك إنت بس، مش كواجب",
        "احتفل بالإنجازات الصغيرة، وزنت أكتر في تمرين؟ ده إنجاز يستاهل",
        "لو شايل تقل في حياتك، التمرين المعتدل هو اللي هيساعدك مش التوقف",
    ],
}

# ============================================================
# Fuzzy search على الكيوردز
# ============================================================
def detect_categories(user_input, threshold=80):
    """بيدور على food/exercise/commitment بـ fuzzy"""
    words = user_input.lower().split()
    candidates = words.copy()
    for i in range(len(words) - 1):
        candidates.append(words[i] + " " + words[i+1])

    has_food = False
    has_exercise = False
    has_commitment = False

    for candidate in candidates:
        for kw in GENERAL_ADVICE_ENTITIES["الأكل"]:
            if fuzz.ratio(candidate, kw) >= threshold or kw in candidate:
                has_food = True
                break
        for kw in GENERAL_ADVICE_ENTITIES["التمارين"]:
            if fuzz.ratio(candidate, kw) >= threshold or kw in candidate:
                has_exercise = True
                break
        for kw in GENERAL_ADVICE_ENTITIES["الالتزام بجدولك"]:
            if fuzz.ratio(candidate, kw) >= threshold or kw in candidate:
                has_commitment = True
                break

    return has_food, has_exercise, has_commitment

def handle(user_input, entity, is_short_func, user_data={}):
    if not entity:
        return "عايز نصيحة بخصوص ايه بالظبط؟ 💡"
    if is_short_func(user_input):
        return f"هل محتاج بعض النصايح بخصوص {entity}؟ 💡"
    has_food, has_exercise, has_commitment = detect_categories(user_input)

    # لو الـ entity اتحدد فعلاً (سواء من كلام اليوزر الحقيقي أو من نص تلقائي
    # مبني على DESCRIPTION)، نضمن إننا منسيبوش الفئة دي من غير ما تتحسب،
    # حتى لو الـ fuzzy matching على النص فشل (زي اختلاف الهمزة في "أكل"/"اكل")
    if entity == "الأكل":
        has_food = True
    elif entity == "التمارين":
        has_exercise = True
    elif entity == "الالتزام بجدولك":
        has_commitment = True

    tips = []

    if has_food and has_exercise:
        # الاتنين مع بعض
        if has_commitment:
            tips += random.sample(GENERAL_ADVICE_DATA["food_commitment"], 3)
            tips += random.sample(GENERAL_ADVICE_DATA["exercise_commitment"], 3)
        else:
            tips += random.sample(GENERAL_ADVICE_DATA["food_general"], 3)
            tips += random.sample(GENERAL_ADVICE_DATA["exercise_general"], 3)

    elif has_food:
        if has_commitment:
            tips = random.sample(GENERAL_ADVICE_DATA["food_commitment"], 4)
        else:
            tips = random.sample(GENERAL_ADVICE_DATA["food_general"], 4)

    elif has_exercise:
        if has_commitment:
            tips = random.sample(GENERAL_ADVICE_DATA["exercise_commitment"], 4)
        else:
            tips = random.sample(GENERAL_ADVICE_DATA["exercise_general"], 4)

    else:
        return "عايز نصيحة بخصوص ايه بالظبط؟ 💡"

    tips_text = "\n\n".join(f"💡 {tip}" for tip in tips)
    return f"تمام ✅ دي بعض النصايح اللي هتفيدك:\n\n{tips_text}"
