import pandas as pd
import streamlit as st

@st.cache_data
def load_datasets():

    return {

        "food": pd.read_csv("Datasets/food_nutrition.csv"),

        "nutrition": pd.read_csv("Datasets/nutrition_requirements.csv"),

        "disease": pd.read_csv("Datasets/disease_food_mapping.csv"),

        "deficiency": pd.read_csv("Datasets/deficiencies.csv"),

        "allergy": pd.read_csv("Datasets/allergies.csv"),

        "bmi": pd.read_csv("Datasets/bmi_categories.csv")

    }
