# ============================================
# DISEASE FUNCTIONS
# ============================================

def get_disease_list(disease_df):
    """
    Returns a sorted list of all diseases.
    """

    return sorted(disease_df["Disease_Name"].unique())


# ============================================
# GET DISEASE DETAILS
# ============================================

def get_disease_details(selected_diseases, disease_df):

    if len(selected_diseases) == 0:
        return None

    filtered = disease_df[
        disease_df["Disease_Name"].isin(selected_diseases)
    ]

    return filtered