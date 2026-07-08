# ============================================================
# general_advice.py
# ============================================================
import random
from thefuzz import fuzz

# أسماء الفئات بالإنجليزي
CATEGORY_EN = {
    "الأكل": "food or nutrition",
    "التمارين": "exercise",
    "الالتزام بجدولك": "sticking to your schedule",
}

def DESCRIPTION(entity="الأكل أو الجيم", lang="ar"):
    if entity is None or entity == "":
        entity = "الأكل أو الجيم" if lang != "en" else "food or the gym"
    if lang == "en":
        entity_en = CATEGORY_EN.get(entity, entity)
        return f"Want some general advice that could help with {entity_en}? 💡"
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
    "food_general_en": [
        "Protein is the most important nutrient for an athlete; aim for 1.6-2.2g per kg of your body weight",
        "Water matters a lot; drink at least 8 cups a day and more if you sweat heavily",
        "Carbs aren't your enemy, they're your body's main energy source for training",
        "Healthy fats (olive oil, avocado, nuts) matter for hormone health",
        "Vegetables and fruits aren't just vitamins; they have fiber that improves digestion and fullness",
        "Cut down on processed and canned food as much as possible",
        "Pre-workout meal, 2 hours before: moderate carbs + light protein + low fat",
        "Post-workout meal: protein + carbs to replenish energy and build muscle",
        "Added sugar is your number one diet enemy, even fruit juices have a lot of it",
        "Eating slowly helps you eat less and feel full sooner",
        "Cooking at home is healthier, cheaper, and gives you more control than eating out",
        "Supplements aren't magic; they only complement good eating, not replace it",
        "Counting calories for a while teaches you to estimate portions even if you won't do it forever",
        "Extreme hunger is your enemy; keep regular meals so you don't overeat",
        "Protein from whole foods (chicken, eggs, milk) is better than protein powder if you're already eating well",
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
    "food_commitment_en": [
        "Meal prep at the start of the week so you don't end up eating whatever's around",
        "Don't deprive yourself of everything you love; aim for 80% on-plan and 20% flexibility",
        "If you slip up one day, it's not the end of the world; get back on track next meal",
        "Gradual change beats sudden change; start by changing one thing a week",
        "Learn to read nutrition labels so you know exactly what you're eating",
        "Before/after photos and tracking numbers help keep you motivated",
        "Having someone else on the same plan helps you stay more committed",
        "If you eat out a lot, learn to pick smartly from the menu instead of breaking your plan",
        "Boredom with healthy food often comes from repeating the same meals; try new recipes",
        "Remind yourself of your goal every day; what made you start this plan?",
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
    "exercise_general_en": [
        "Warming up before training isn't optional; 5-10 minutes protects you from injuries",
        "Enough sleep (7-9 hours) matters as much as training itself; muscle is built during sleep",
        "Rest between sessions matters; a muscle needs at least 48 hours",
        "Progressive overload is key; only add 5-10% weight every two weeks",
        "Focus on correct form before adding more weight",
        "Compound exercises (squat, deadlift, bench) matter more than isolation for building muscle",
        "Correct breathing in training matters; exhale on the hardest part of the movement",
        "Hydration during training matters; drink every 15-20 minutes",
        "Core exercises protect your back in every other exercise",
        "Log your workouts so you know whether you're progressing or not",
        "If you feel sharp pain during training, stop immediately",
        "Stretching after training improves flexibility and reduces muscle stiffness",
        "Cooling down after training helps speed up recovery"
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
    "exercise_commitment_en": [
        "Consistency beats intensity; 3 regular days beat 6 inconsistent ones",
        "If you don't feel progress, that doesn't mean you're not progressing; change shows up over time",
        "Start with small, achievable goals instead of one huge goal that discourages you",
        "Training at the same time every day helps you stay committed and turns it into a habit",
        "If you're not motivated by the gym, try another type of sport, it doesn't have to be the gym",
        "Having a training partner helps you show up even when you don't feel like it",
        "If you miss a day or two, get back on track without feeling guilty",
        "Tracking your body with photos and measurements every month keeps you motivated",
        "Your favorite music during training improves performance and enjoyment",
        "Think of training as time just for you, not as an obligation",
        "Celebrate small wins; lifted more weight today? That's an achievement worth celebrating",
        "If you're carrying a heavy load in life, moderate exercise will help, not stopping",
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

def handle(user_input, entity, is_short_func, user_data={}, lang="ar"):
    if lang == "en":
        if not entity:
            return "What would you like advice about exactly? 💡"
        entity_en = CATEGORY_EN.get(entity, entity)
        if is_short_func(user_input):
            return f"Would you like some tips about {entity_en}? 💡"

        has_food, has_exercise, has_commitment = detect_categories(user_input)

        if entity == "الأكل":
            has_food = True
        elif entity == "التمارين":
            has_exercise = True
        elif entity == "الالتزام بجدولك":
            has_commitment = True

        tips = []

        if has_food and has_exercise:
            if has_commitment:
                tips += random.sample(GENERAL_ADVICE_DATA["food_commitment_en"], 3)
                tips += random.sample(GENERAL_ADVICE_DATA["exercise_commitment_en"], 3)
            else:
                tips += random.sample(GENERAL_ADVICE_DATA["food_general_en"], 3)
                tips += random.sample(GENERAL_ADVICE_DATA["exercise_general_en"], 3)

        elif has_food:
            if has_commitment:
                tips = random.sample(GENERAL_ADVICE_DATA["food_commitment_en"], 4)
            else:
                tips = random.sample(GENERAL_ADVICE_DATA["food_general_en"], 4)

        elif has_exercise:
            if has_commitment:
                tips = random.sample(GENERAL_ADVICE_DATA["exercise_commitment_en"], 4)
            else:
                tips = random.sample(GENERAL_ADVICE_DATA["exercise_general_en"], 4)

        else:
            return "What would you like advice about exactly? 💡"

        tips_text = "\n\n".join(f"💡 {tip}" for tip in tips)
        return f"Sure ✅ Here are some tips that should help you:\n\n{tips_text}"

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
