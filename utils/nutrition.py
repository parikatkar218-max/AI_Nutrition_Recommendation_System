# ============================================
# NUTRITION REQUIREMENTS
# ============================================

def get_age_group(age):

    if 13 <= age <= 17:
        return "13-17"

    elif 18 <= age <= 30:
        return "18-30"

    elif 31 <= age <= 50:
        return "31-50"

    elif 51 <= age <= 70:
        return "51-70"

    else:
        return "71+"


# ============================================
# GET DAILY NUTRITION REQUIREMENTS
# ============================================

def get_nutrition_requirements(age, gender, activity_level, nutrition_df):

    age_group = get_age_group(age)

    result = nutrition_df[
        (nutrition_df["Age_Group"] == age_group) &
        (nutrition_df["Gender"] == gender) &
        (nutrition_df["Activity_Level"] == activity_level)
    ]

    if result.empty:
        return None

    return result.iloc[0]