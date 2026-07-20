# ============================================
# BMI FUNCTIONS
# ============================================

def calculate_bmi(weight, height):
    """
    Calculate BMI using:
    BMI = Weight (kg) / Height² (m²)
    """

    height_m = height / 100

    bmi = weight / (height_m ** 2)

    return round(bmi, 2)


# ============================================
# BMI DETAILS
# ============================================

def get_bmi_details(bmi, bmi_df):

    for _, row in bmi_df.iterrows():

        if row["BMI_Min"] <= bmi <= row["BMI_Max"]:

            return {
                "BMI_Category": row["BMI_Category"],
                "Health_Risk": row["Health_Risk"],
                "Recommendation": row["Recommendation"],
                "Goal": row["Goal"],
                "Target_Calorie_Adjustment": row["Target_Calorie_Adjustment"]
            }

    return {
        "BMI_Category": "Unknown",
        "Health_Risk": "-",
        "Recommendation": "-",
        "Goal": "-",
        "Target_Calorie_Adjustment": 0
    }