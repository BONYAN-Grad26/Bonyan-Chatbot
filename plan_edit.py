# ============================================================
# plan_edit.py
# كل حاجة خاصة بتصنيف plan_edit
# ============================================================

PLAN_EDIT_ENTITIES = {
    "meals": ["breakfast", "فطار", "صباح", "dinner", "عشاء", "بليل", "lunch", "غداء", "العصر", "اكل", "وجبات", "food", "meals"],
    "workout": ["تمرين", "رياضي", "exercises", "gym", "جيم","workout","fitness"],
}

def DESCRIPTION (entity="الأكل أو التمارين"): 
   return f"عايزني اغيرلك جدول {entity}"

# هنا هتحط الـ API calls بتاعت الباك ايند عشان يعمل generate لخطة جديدة
# محتاج تتفق مع زميلك على الـ endpoint

def handle(user_input, entity, is_short_func, user_data={}):
    """الـ handler الخاص بـ plan_edit - محتاج ربط بالباك ايند"""
    if not entity:
        return "عايز تعدل إيه في خطتك؟"
    if is_short_func(user_input):
        return f"هل عايز تعدل {entity}؟"

    if entity == "meals_edit":
        # مؤقت لحد ما تتواصل مع الباك ايند
        return "[plan_edit | meals] - محتاج ربط بالباك ايند عشان يعمل generate لخطة أكل جديدة"

    elif entity == "workout_edit":
        return "[plan_edit | workout] - محتاج ربط بالباك ايند عشان يعمل generate لخطة تمرين جديدة"

    return f"[plan_edit | entity: {entity}]"
