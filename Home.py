import streamlit as st
from utils.load_data import load_datasets

# ============================================
# PAGE CONFIGURATION
# ============================================

st.set_page_config(
    page_title="AI Nutrition Recommendation System",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# LOAD DATASETS
# ============================================

datasets = load_datasets()

food_df = datasets["food"]
nutrition_df = datasets["nutrition"]
disease_df = datasets["disease"]
deficiency_df = datasets["deficiency"]
allergy_df = datasets["allergy"]
bmi_df = datasets["bmi"]

print(food_df.columns.tolist())
print(nutrition_df.columns.tolist())
print(disease_df.columns.tolist())
print(deficiency_df.columns.tolist())
print(allergy_df.columns.tolist())
print(bmi_df.columns.tolist())
# ============================================
# SIDEBAR
# ============================================

with st.sidebar:

    st.image("https://img.icons8.com/color/96/salad.png", width=80)

    st.title("Nutrition AI")

    st.markdown("---")

    st.success("🥗 Healthy Choices • Better Life")

# ============================================
# MAIN PAGE
# ============================================

st.title("🥗 AI Nutrition Recommendation System")

st.caption("Personalized Nutrition for a Healthier Lifestyle")

st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:

    st.header("Welcome!")

    st.write("""
This intelligent nutrition recommendation system helps users make healthier food choices using:

- 🧮 Body Mass Index (BMI)
- 🍽 Daily Nutrition Requirements
- 🩺 Disease-Based Recommendations
- 🩸 Nutritional Deficiencies
- 🚫 Allergy Detection
- 🤖 AI-Based Food Recommendation Engine

Simply enter your health information and receive personalized food recommendations.
""")

with col2:

    st.info(f"""
### Quick Facts

🍎 **{len(food_df)} Foods**

🩺 **{len(disease_df)} Diseases**

🥦 **{food_df["Category"].nunique()} Food Categories**

📊 Personalized Recommendations

💧 Nutrition Tracking
""")

st.markdown("---")

st.subheader("📈 System Highlights")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🍎 Foods", len(food_df))

with col2:
    st.metric("🩺 Diseases", len(disease_df))

with col3:
    st.metric("🥦 Food Categories", food_df["Category"].nunique())

with col4:
    st.metric("🎯 Recommendation", "Personalized")

st.markdown("---")

st.subheader("💡 Why Use This System?")

left, right = st.columns(2)

with left:

    st.success("""
✔ Personalized Food Recommendations

✔ Easy-to-Use Interface

✔ Disease-Based Diet Guidance

✔ Nutritionally Balanced Suggestions
""")

with right:

    st.success("""
✔ Supports Multiple Diseases

✔ Allergy-Aware Recommendations

✔ Nutrient Deficiency Support

✔ AI-Based Recommendation Engine
""")