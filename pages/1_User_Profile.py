import streamlit as st

from utils.load_data import load_datasets
from utils.bmi import calculate_bmi, get_bmi_details
from utils.nutrition import get_nutrition_requirements
from utils.disease import get_disease_list, get_disease_details
from utils.deficiency import (
    get_deficiency_list,
    get_deficiency_details
)
from utils.allergy import (
    get_allergy_list,
    get_allergy_details
)
from utils.recommendation import recommend_foods


# ============================================
# PAGE CONFIGURATION
# ============================================

st.set_page_config(
    page_title="User Profile",
    page_icon="👤",
    layout="wide"
)

# ============================================
# LOAD DATA
# ============================================

datasets = load_datasets()

food_df = datasets["food"]
bmi_df = datasets["bmi"]
nutrition_df = datasets["nutrition"]
disease_df = datasets["disease"]
deficiency_df = datasets["deficiency"]
allergy_df = datasets["allergy"]


disease_list = get_disease_list(disease_df)
deficiency_list = get_deficiency_list(deficiency_df)
allergy_list = get_allergy_list(allergy_df)


# ============================================
# SESSION STATE
# ============================================

if "profile_saved" not in st.session_state:
    st.session_state.profile_saved = False

if "user" not in st.session_state:
    st.session_state.user = {}

# ============================================
# TITLE
# ============================================

st.title("👤 User Profile")

st.write(
    "Please provide your details to receive personalized nutrition recommendations."
)

st.divider()

# ============================================
# USER DETAILS
# ============================================

col1, col2 = st.columns(2)

with col1:

    name = st.text_input("Full Name")

    age = st.number_input(
        "Age",
        min_value=13,
        max_value=100,
        value=18
    )

    gender = st.selectbox(
        "Gender",
        ["Male", "Female"]
    )

with col2:

    height = st.number_input(
        "Height (cm)",
        min_value=100.0,
        max_value=250.0,
        value=170.0
    )

    weight = st.number_input(
        "Weight (kg)",
        min_value=20.0,
        max_value=250.0,
        value=70.0
    )

    activity = st.selectbox(
        "Activity Level",
        [
            "Sedentary",
            "Moderate",
            "Active"
        ]
    )

st.divider()

# ============================================
# SAVE PROFILE
# ============================================

if st.button("Continue ➜", use_container_width=True):

    st.session_state.profile_saved = True

    st.session_state.user = {

        "Name": name,
        "Age": age,
        "Gender": gender,
        "Height": height,
        "Weight": weight,
        "Activity_Level": activity

    }

# ============================================
# SHOW RESULTS
# ============================================

if st.session_state.profile_saved:

    user = st.session_state.user

    bmi = calculate_bmi(
        user["Weight"],
        user["Height"]
    )

    bmi_details = get_bmi_details(
        bmi,
        bmi_df
    )

    nutrition = get_nutrition_requirements(
        user["Age"],
        user["Gender"],
        user["Activity_Level"],
        nutrition_df
    )

    st.success("Profile saved successfully!")

    # ========================================
    # BMI REPORT
    # ========================================

    st.divider()

    st.subheader("📊 BMI Report")

    c1, c2 = st.columns(2)

    with c1:

        st.metric("BMI", bmi)
        st.metric("BMI Category", bmi_details["BMI_Category"])

    with c2:

        st.metric("Health Risk", bmi_details["Health_Risk"])

    st.info(f"**Recommendation:** {bmi_details['Recommendation']}")

    st.success(f"**Goal:** {bmi_details['Goal']}")

    # ========================================
    # NUTRITION
    # ========================================

    st.divider()

    st.subheader("🥗 Daily Nutrition Requirements")

    if nutrition is not None:

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "🔥 Calories",
                f"{nutrition['Calories_kcal']} kcal"
            )

            st.metric(
                "🥩 Protein",
                f"{nutrition['Protein_g']} g"
            )

            st.metric(
                "🍞 Carbohydrates",
                f"{nutrition['Carbohydrates_g']} g"
            )

        with col2:

            st.metric(
                "🥑 Fat",
                f"{nutrition['Fat_g']} g"
            )

            st.metric(
                "🥦 Fiber",
                f"{nutrition['Fiber_g']} g"
            )

            st.metric(
                "🍬 Sugar Limit",
                f"{nutrition['Sugar_Max_g']} g"
            )

        with col3:

            st.metric(
                "💧 Water",
                f"{nutrition['Water_L']} L"
            )

            st.metric(
                "🧂 Sodium Limit",
                f"{nutrition['Sodium_Max_mg']} mg"
            )

            st.metric(
                "🍌 Potassium",
                f"{nutrition['Potassium_mg']} mg"
            )

        st.divider()

        st.subheader("🦴 Essential Minerals")

        m1, m2 = st.columns(2)

        with m1:

            st.metric(
                "🥛 Calcium",
                f"{nutrition['Calcium_mg']} mg"
            )

        with m2:

            st.metric(
                "🩸 Iron",
                f"{nutrition['Iron_mg']} mg"
            )

    else:

        st.error("No nutrition requirements found.")

    # ========================================
    # DISEASE MODULE
    # ========================================

    st.divider()

    st.subheader("🩺 Health Conditions")

    selected_diseases = st.multiselect(

        "Select Disease(s)",

        disease_list,

        placeholder="Choose one or more diseases"

    )

    st.session_state["selected_diseases"] = selected_diseases

    if selected_diseases:

        disease_info = get_disease_details(
            selected_diseases,
            disease_df
        )

        st.divider()

        st.subheader("🩺 Disease Recommendations")

        for _, disease in disease_info.iterrows():

            with st.expander(
                f"📌 {disease['Disease_Name']}",
                expanded=True
            ):

                st.write(
                    f"**Category:** {disease['Disease_Category']}"
                )

                st.write(
                    f"**Description:** {disease['Description']}"
                )

                st.success(
                    f"✅ Foods To Eat\n\n{disease['Foods_To_Eat']}"
                )

                st.error(
                    f"❌ Foods To Avoid\n\n{disease['Foods_To_Avoid']}"
                )

                c1, c2 = st.columns(2)

                with c1:

                    st.info(
                        f"💧 Water Intake\n\n{disease['Water_Intake_L']} L/day"
                    )

                with c2:

                    st.info(
                        f"🏃 Exercise\n\n{disease['Exercise_Minutes']} min/day"
                    )

                st.warning(
                    f"💡 Lifestyle Advice\n\n{disease['Lifestyle_Advice']}"
                )
        

    st.session_state["disease_info"] = (
        disease_info if selected_diseases else None
    )





    # ========================================
    # DEFICIENCY MODULE
    # ========================================

    st.divider()

    st.subheader("🩸 Nutritional Deficiencies")

    selected_deficiencies = st.multiselect(

        "Select Deficiency(s)",

        deficiency_list,

        placeholder="Choose one or more deficiencies"

    )

    st.session_state["selected_deficiencies"] = selected_deficiencies

    if selected_deficiencies:

        deficiency_info = get_deficiency_details(
            selected_deficiencies,
            deficiency_df
        )

        st.divider()

        st.subheader("🩸 Deficiency Recommendations")

        for _, deficiency in deficiency_info.iterrows():

            with st.expander(
                f"📌 {deficiency['Deficiency_Name']}",
                expanded=True
            ):

                st.write(
                    f"**Nutrient:** {deficiency['Nutrient']}"
                )

                st.write(
                    f"**Common Symptoms:** {deficiency['Common_Symptoms']}"
                )

                st.success(
                    f"✅ Foods To Eat\n\n{deficiency['Foods_To_Eat']}"
                )

                st.error(
                    f"❌ Foods To Avoid\n\n{deficiency['Foods_To_Avoid']}"
                )

                col1, col2 = st.columns(2)

                with col1:
                    
                    st.info(
                        f"🥦 Best Food Categories\n\n{deficiency['Best_Food_Categories']}"
                    )

                    st.info(
                        f"💧 Water Intake\n\n{deficiency['Water_Intake_L']} L/day"
                    )

                with col2:

                    st.warning(
                        f"⚠ Severity\n\n{deficiency['Severity']}"
                    )

                    st.info(
                        f"🥗 Recommended Daily Intake\n\n{deficiency['Recommended_Daily_Intake']}"
                    )

                st.info(
                    f"💡 Lifestyle Advice\n\n{deficiency['Lifestyle_Advice']}"
           )   

    st.session_state["deficiency_info"] = (
       deficiency_info if selected_deficiencies else None
    )



    # ========================================
    # ALLERGY MODULE
    # ========================================

    st.divider()

    st.subheader("🚫 Food Allergies")

    selected_allergies = st.multiselect(

        "Select Allergy(s)",

        allergy_list,

        placeholder="Choose one or more allergies"

    )

    #st.write("Selected:", selected_allergies)

    st.session_state["selected_allergies"] = selected_allergies

    #st.write("Session:", st.session_state.get("selected_allergies"))

    #st.session_state["selected_allergies"] = selected_allergies

    if selected_allergies:

        allergy_info = get_allergy_details(
            selected_allergies,
            allergy_df
        )

        st.divider()

        st.subheader("🚫 Allergy Recommendations")

        for _, allergy in allergy_info.iterrows():

            with st.expander(
                f"📌 {allergy['Allergy_Name']}",
            expanded=True
            ):

                st.write(
                    f"**Allergen:** {allergy['Allergen']}"
                )

                st.write(
                    f"**Common Symptoms:** {allergy['Common_Symptoms']}"
                )

                st.error(
                    f"❌ Foods To Avoid\n\n{allergy['Foods_To_Avoid']}"
                )

                st.success(
                    f"✅ Safe Alternatives\n\n{allergy['Safe_Alternatives']}"
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.info(
                        f"🥗 Food Category\n\n{allergy['Food_Category']}"
                    )

                with col2:

                    st.warning(
                        f"⚠ Severity\n\n{allergy['Severity']}"
                    )

    st.session_state["allergy_info"] = (
       allergy_info if selected_allergies else None
    )


    # ========================================
    # AI FOOD RECOMMENDATION ENGINE
    # ========================================

    st.divider()

    st.subheader("🤖 AI Food Recommendations")

    recommended_foods = recommend_foods(

        food_df,

        bmi_details["BMI_Category"],

        disease_info=disease_info if selected_diseases else None,

        deficiency_info=deficiency_info if selected_deficiencies else None,

        allergy_info=allergy_info if selected_allergies else None
    )

    st.success(
        f"Top food recommendations based on BMI Category: {bmi_details['BMI_Category']}"
    )

    display_columns = [

        "Food_Name",
        "Category",
        "Meal_Type",
        "Calories_kcal",
        "Protein_g",
        "Fiber_g",
        "AI_Score"

    ]

    st.dataframe(

        recommended_foods[display_columns],

        use_container_width=True

    )
    