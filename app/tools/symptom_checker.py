from langchain_core.tools import tool


# Demo-only symptom → possible condition mapping.
# These are NOT diagnoses.
SYMPTOM_CONDITION_MAP = {
    "headache": [
        "Migraine",
        "Tension headache",
        "Viral illness"
    ],

    "nausea": [
        "Gastrointestinal illness",
        "Migraine",
        "Viral illness"
    ],

    "vomiting": [
        "Gastrointestinal illness",
        "Food-related illness",
        "Viral illness"
    ],

    "fever": [
        "Viral illness",
        "Bacterial infection",
        "Influenza-like illness"
    ],

    "cough": [
        "Upper respiratory infection",
        "Influenza-like illness",
        "Bronchitis"
    ],

    "sore throat": [
        "Upper respiratory infection",
        "Tonsillitis",
        "Pharyngitis"
    ],

    "chest pain": [
        "Cardiac condition",
        "Respiratory condition",
        "Musculoskeletal condition"
    ],

    "joint pain": [
        "Musculoskeletal condition",
        "Arthritis-related condition",
        "Inflammatory condition"
    ],

    "skin rash": [
        "Dermatological condition",
        "Allergic reaction",
        "Skin infection"
    ]
}


@tool
def symptom_checker(symptoms: list[str]) -> dict:
    """
    Takes a list of patient symptoms and returns
    possible conditions for routing purposes.

    This is NOT a medical diagnostic tool.
    """

    normalized_symptoms = [
        symptom.strip().lower()
        for symptom in symptoms
    ]

    possible_conditions = set()

    for symptom in normalized_symptoms:
        conditions = SYMPTOM_CONDITION_MAP.get(symptom, [])

        for condition in conditions:
            possible_conditions.add(condition)

    return {
        "symptoms": normalized_symptoms,
        "possible_conditions": sorted(possible_conditions),
        "note": (
            "Possible conditions are provided only for "
            "demonstration and department-routing purposes. "
            "They are not a diagnosis."
        )
    }