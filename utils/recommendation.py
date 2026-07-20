import pandas as pd


# ============================================
# AI FOOD RECOMMENDATION ENGINE
# ============================================

def recommend_foods(
    food_df,
    bmi_category,
    disease_info=None,
    deficiency_info=None,
    allergy_info=None
):

    recommendations = food_df.copy()

    # ===================================
    # BMI FILTER
    # ===================================

    if bmi_category == "Underweight":

        recommendations = recommendations[
            recommendations["Calories_kcal"] >= 250
        ]

    elif bmi_category == "Normal":

        recommendations = recommendations[
            recommendations["Calories_kcal"].between(150, 350)
        ]

    elif bmi_category == "Overweight":

        recommendations = recommendations[
            recommendations["Calories_kcal"] <= 250
        ]

    elif bmi_category == "Obese":

        recommendations = recommendations[
            recommendations["Calories_kcal"] <= 180
        ]

    # ===================================
    # BASE AI SCORE
    # ===================================

    recommendations = recommendations.copy()

    recommendations["AI_Score"] = (

        recommendations["Protein_g"] * 3

        + recommendations["Fiber_g"] * 2

        - recommendations["Sugar_g"] * 0.5

        - recommendations["Fat_g"] * 0.2

    )

    # ===================================
    # DISEASE SCORING
    # ===================================

    if disease_info is not None:

        for _, disease in disease_info.iterrows():

            # Protein
            if disease["Protein"] == "Increase":
                recommendations["AI_Score"] += recommendations["Protein_g"] * 2

            elif disease["Protein"] == "Decrease":
                recommendations["AI_Score"] -= recommendations["Protein_g"] * 2

            # Carbohydrates
            if disease["Carbohydrates"] == "Increase":
                recommendations["AI_Score"] += recommendations["Carbs_g"] * 1.5

            elif disease["Carbohydrates"] == "Decrease":
                recommendations["AI_Score"] -= recommendations["Carbs_g"] * 1.5

            # Fat
            if disease["Fat"] == "Increase":
                recommendations["AI_Score"] += recommendations["Fat_g"]

            elif disease["Fat"] == "Decrease":
                recommendations["AI_Score"] -= recommendations["Fat_g"]

            # Fiber
            if disease["Fiber"] == "Increase":
                recommendations["AI_Score"] += recommendations["Fiber_g"] * 3

            elif disease["Fiber"] == "Decrease":
                recommendations["AI_Score"] -= recommendations["Fiber_g"] * 3

            # Sugar
            if disease["Sugar"] == "Increase":
                recommendations["AI_Score"] += recommendations["Sugar_g"]

            elif disease["Sugar"] == "Decrease":
                recommendations["AI_Score"] -= recommendations["Sugar_g"] * 2

            # Sodium
            if disease["Sodium"] == "Increase":
                recommendations["AI_Score"] += recommendations["Sodium_mg"] / 100

            elif disease["Sodium"] == "Decrease":
                recommendations["AI_Score"] -= recommendations["Sodium_mg"] / 100

            # Potassium
            if disease["Potassium"] == "Increase":
                recommendations["AI_Score"] += recommendations["Potassium_mg"] / 100

            elif disease["Potassium"] == "Decrease":
                recommendations["AI_Score"] -= recommendations["Potassium_mg"] / 100

            # Calcium
            if disease["Calcium"] == "Increase":
                recommendations["AI_Score"] += recommendations["Calcium_mg"] / 100

            elif disease["Calcium"] == "Decrease":
                recommendations["AI_Score"] -= recommendations["Calcium_mg"] / 100

            # Iron
            if disease["Iron"] == "Increase":
                recommendations["AI_Score"] += recommendations["Iron_mg"] * 5

            elif disease["Iron"] == "Decrease":
                recommendations["AI_Score"] -= recommendations["Iron_mg"] * 5


    # ===================================
    # DEFICIENCY SCORING
    # ===================================

    if deficiency_info is not None:

        for _, deficiency in deficiency_info.iterrows():

            nutrient = deficiency["Nutrient"].strip().lower()

            # ==============================
            # Iron
            # ==============================
            if nutrient == "iron":

                recommendations["AI_Score"] += (
                    recommendations["Iron_mg"] * 5
                )

            # ==============================
            # Calcium
            # ==============================
            elif nutrient == "calcium":

                recommendations["AI_Score"] += (
                    recommendations["Calcium_mg"] / 100
                )

            # ==============================
            # Potassium
            # ==============================
            elif nutrient == "potassium":

                recommendations["AI_Score"] += (
                    recommendations["Potassium_mg"] / 100
                )

            # ==============================
            # Fiber
            # ==============================
            elif nutrient == "fiber":

                recommendations["AI_Score"] += (
                    recommendations["Fiber_g"] * 3
                )

            # ==============================
            # Protein
            # ==============================
            elif nutrient == "protein":

                recommendations["AI_Score"] += (
                    recommendations["Protein_g"] * 3
                )

            # ==============================
            # Vitamin C
            # ==============================
            elif nutrient == "vitamin c":

                recommendations["AI_Score"] += (
                    recommendations["Vitamin_C_mg"] / 10
                )

            # ==============================
            # Vitamin D
            # ==============================
            elif nutrient == "vitamin d":

                recommendations["AI_Score"] += (
                    recommendations["Vitamin_D_IU"] / 100
                )

            # ==============================
            # Vitamin B12
            # ==============================
            elif nutrient in ["vitamin b12", "b12"]:

                recommendations["AI_Score"] += (
                    recommendations["Vitamin_B12_mcg"] * 10
                )


    # ===================================
    # ALLERGY FILTERING
    # ===================================

    if allergy_info is not None:

        for _, allergy in allergy_info.iterrows():

            # -----------------------------
            # Remove Food Categories
            # -----------------------------

            category = str(allergy["Food_Category"]).strip()

            if category:

                recommendations = recommendations[
                    recommendations["Category"] != category
                ]

            # -----------------------------
            # Remove Specific Foods
            # -----------------------------

            foods = str(allergy["Foods_To_Avoid"]).split(";")

            for food in foods:

                food = food.strip()

                if food:

                    recommendations = recommendations[
                        ~recommendations["Food_Name"]
                        .str.contains(food, case=False, na=False)
                    ]



    # ===================================
    # SORT
    # ===================================

    recommendations = recommendations.sort_values(
        by="AI_Score",
        ascending=False
    )

    return recommendations.head(20)