# ============================================
# ALLERGY FUNCTIONS
# ============================================

def get_allergy_list(allergy_df):
    """
    Returns a sorted list of all allergies.
    """
    return sorted(allergy_df["Allergy_Name"].unique())


# ============================================
# GET ALLERGY DETAILS
# ============================================

def get_allergy_details(selected_allergies, allergy_df):

    if len(selected_allergies) == 0:
        return None

    filtered = allergy_df[
        allergy_df["Allergy_Name"].isin(selected_allergies)
    ]

    return filtered