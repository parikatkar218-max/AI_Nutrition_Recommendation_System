# ============================================
# DEFICIENCY FUNCTIONS
# ============================================

def get_deficiency_list(deficiency_df):
    """
    Returns a sorted list of all deficiencies.
    """

    return sorted(deficiency_df["Deficiency_Name"].unique())


# ============================================
# GET DEFICIENCY DETAILS
# ============================================

def get_deficiency_details(selected_deficiencies, deficiency_df):

    if len(selected_deficiencies) == 0:
        return None

    filtered = deficiency_df[
        deficiency_df["Deficiency_Name"].isin(selected_deficiencies)
    ]

    return filtered