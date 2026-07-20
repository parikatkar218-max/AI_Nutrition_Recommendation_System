import streamlit as st

from utils.load_data import load_datasets
from utils.bmi import calculate_bmi, get_bmi_details
from utils.recommendation import recommend_foods

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Food Recommendations",
    page_icon="🍎",
    layout="wide"
)

# ==========================================
# CHECK PROFILE
# ==========================================

if "profile_saved" not in st.session_state or not st.session_state.profile_saved:
    st.warning("Please complete your profile first.")
    st.stop()

# ==========================================
# LOAD DATA
# ==========================================

datasets = load_datasets()

food_df = datasets["food"]
bmi_df = datasets["bmi"]

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

# ==========================================
# GET SAVED DATA
# ==========================================

disease_info = st.session_state.get("disease_info", None)
deficiency_info = st.session_state.get("deficiency_info", None)
allergy_info = st.session_state.get("allergy_info", None)

# ==========================================
# RECOMMEND FOODS
# ==========================================

recommended_foods = recommend_foods(
    food_df,
    bmi_details["BMI_Category"],
    disease_info=disease_info,
    deficiency_info=deficiency_info,
    allergy_info=allergy_info
)

# ==========================================
# PAGE TITLE
# ==========================================

st.title("🍎 AI Food Recommendations")

st.caption("Personalized food suggestions based on your health profile")

st.divider()

# ==========================================
# USER SUMMARY
# ==========================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("BMI", bmi)

with col2:
    st.metric("BMI Category", bmi_details["BMI_Category"])

with col3:
    st.metric("Recommended Foods", len(recommended_foods))

st.divider()



st.subheader("🔍 Filter Recommendations")

col1, col2, col3 = st.columns(3)

with col1:

    meal_filter = st.selectbox(
        "Meal Type",
        ["All"] + sorted(recommended_foods["Meal_Type"].dropna().unique().tolist())
    )

with col2:

    category_filter = st.selectbox(
        "Food Category",
        ["All"] + sorted(recommended_foods["Category"].dropna().unique().tolist())
    )

with col3:

    diet_filter = st.selectbox(
        "Diet Preference",
        [
            "All",
            "Vegetarian",
            "Vegan",
            "Gluten Free"
        ]
    )

filtered_foods = recommended_foods.copy()

# Meal Filter
if meal_filter != "All":
    filtered_foods = filtered_foods[
        filtered_foods["Meal_Type"] == meal_filter
    ]

# Category Filter
if category_filter != "All":
    filtered_foods = filtered_foods[
        filtered_foods["Category"] == category_filter
    ]

# Diet Filter
if diet_filter == "Vegetarian":
    filtered_foods = filtered_foods[
        filtered_foods["Vegetarian"] == "Yes"
    ]

elif diet_filter == "Vegan":
    filtered_foods = filtered_foods[
        filtered_foods["Vegan"] == "Yes"
    ]

elif diet_filter == "Gluten Free":
    filtered_foods = filtered_foods[
        filtered_foods["Gluten_Free"] == "Yes"
    ]

if filtered_foods.empty:

    st.warning("No foods match the selected filters.")

    st.stop()

st.subheader("📊 Recommendation Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "🍎 Foods",
        len(filtered_foods)
    )

with col2:
    st.metric(
        "🔥 Avg Calories",
        round(filtered_foods["Calories_kcal"].mean(), 1)
    )

with col3:
    st.metric(
        "🥩 Avg Protein",
        round(filtered_foods["Protein_g"].mean(), 1)
    )

with col4:
    st.metric(
        "🥦 Avg Fiber",
        round(filtered_foods["Fiber_g"].mean(), 1)
    )

st.divider()

# ==========================================
# TOP RECOMMENDATIONS
# ==========================================

st.subheader("⭐ Top 5 AI Recommendations")

display_columns = [

    "Food_Name",

    "Category",

    "Cuisine",

    "Meal_Type",

    "Calories_kcal",

    "Protein_g",

    "Carbs_g",

    "Fat_g",

    "Fiber_g",

    "AI_Score"

]


top5 =filtered_foods.head(5)

filtered_foods = filtered_foods.sort_values(
    by="AI_Score",
    ascending=False
)

for i, (_, food) in enumerate(top5.iterrows(), start=1):

    with st.container(border=True):

        col1, col2 = st.columns([3,1])

        with col1:

            st.markdown(f"### {i}. 🍽 {food['Food_Name']}")

            st.write(f"**Category:** {food['Category']}")

            st.write(f"**Meal:** {food['Meal_Type']}")

        with col2:

            st.metric(
                "⭐ AI Score",
                round(food["AI_Score"],2)
            )

        c1, c2, c3 = st.columns(3)

        c1.metric("Calories", f"{food['Calories_kcal']} kcal")

        c2.metric("Protein", f"{food['Protein_g']} g")

        c3.metric("Fiber", f"{food['Fiber_g']} g")

st.subheader("📋 Complete Recommendation List")

st.caption(f"Showing {len(filtered_foods)} food recommendation(s)")

st.dataframe(
    filtered_foods[display_columns],
    use_container_width=True,
    hide_index=True
)



