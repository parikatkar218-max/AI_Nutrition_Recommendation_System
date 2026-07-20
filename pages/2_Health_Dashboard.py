import streamlit as st

from utils.load_data import load_datasets
from utils.bmi import calculate_bmi, get_bmi_details
from utils.nutrition import get_nutrition_requirements

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Health Dashboard",
    page_icon="📊",
    layout="wide"
)

# ==========================================
# CHECK USER PROFILE
# ==========================================

if "profile_saved" not in st.session_state:

    st.warning("Please complete your profile first.")

    st.stop()

# ==========================================
# LOAD DATA
# ==========================================

datasets = load_datasets()

bmi_df = datasets["bmi"]
nutrition_df = datasets["nutrition"]

# ==========================================
# USER DATA
# ==========================================

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

# ==========================================
# TITLE
# ==========================================

st.title("📊 Health Dashboard")

st.caption("Your Personalized Health Summary")

st.divider()

st.subheader("👤 User Information")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Name", user["Name"])

with c2:
    st.metric("Age", user["Age"])

with c3:
    st.metric("Gender", user["Gender"])

st.divider()

st.subheader("📈 BMI Summary")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("BMI", bmi)

with c2:
    st.metric("Category", bmi_details["BMI_Category"])

with c3:
    st.metric("Health Risk", bmi_details["Health_Risk"])

with c4:
    st.metric("Goal", bmi_details["Goal"])

st.info(bmi_details["Recommendation"])

st.divider()

st.subheader("🥗 Daily Nutrition")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Calories", f"{nutrition['Calories_kcal']} kcal")
    st.metric("Protein", f"{nutrition['Protein_g']} g")

with c2:
    st.metric("Carbohydrates", f"{nutrition['Carbohydrates_g']} g")
    st.metric("Fat", f"{nutrition['Fat_g']} g")

with c3:
    st.metric("Fiber", f"{nutrition['Fiber_g']} g")
    st.metric("Water", f"{nutrition['Water_L']} L")


    st.divider()

st.subheader("🩺 Health Conditions")

col1, col2, col3 = st.columns(3)

# -----------------------------
# Diseases
# -----------------------------

with col1:

    st.markdown("### 🩺 Diseases")

    diseases = st.session_state.get(
        "selected_diseases",
        []
    )

    if diseases:

        for disease in diseases:
            st.success(disease)

    else:
        st.info("None")

# -----------------------------
# Deficiencies
# -----------------------------

with col2:

    st.markdown("### 🩸 Deficiencies")

    deficiencies = st.session_state.get(
        "selected_deficiencies",
        []
    )

    if deficiencies:

        for deficiency in deficiencies:
            st.warning(deficiency)

    else:
        st.info("None")

# -----------------------------
# Allergies
# -----------------------------

#st.write(st.session_state)

with col3:

    st.markdown("### 🚫 Allergies")

    allergies = st.session_state.get(
        "selected_allergies",
        []
    )

    if allergies:

        for allergy in allergies:
            st.error(allergy)

    else:
        st.info("None")