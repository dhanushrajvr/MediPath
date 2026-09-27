from langchain_core.tools import tool


EMERGENCY_SYMPTOMS = {
    "severe chest pain",
    "difficulty breathing",
    "unconsciousness",
    "severe bleeding",
    "seizure",
    "stroke symptoms"
}


EMERGENCY_COMBINATIONS = [
    {
        "chest pain",
        "difficulty breathing"
    },

    {
        "chest pain",
        "fainting"
    }
]


@tool
def check_emergency(symptoms: list[str]) -> dict:
    """
    Deterministic emergency-indicator check.

    Returns True when predefined emergency indicators
    are detected.

    This does not diagnose a medical emergency.
    It is a safety-oriented demonstration mechanism.
    """

    normalized = {
        symptom.strip().lower()
        for symptom in symptoms
    }

    # Check direct emergency indicators
    for symptom in normalized:

        if symptom in EMERGENCY_SYMPTOMS:
            return {
                "emergency": True,
                "matched_indicator": symptom,
                "message": (
                    "Potential emergency indicator detected. "
                    "Seek immediate professional/emergency "
                    "medical care."
                )
            }

    # Check combinations
    for combination in EMERGENCY_COMBINATIONS:

        if combination.issubset(normalized):

            return {
                "emergency": True,
                "matched_indicator": list(combination),
                "message": (
                    "Potential emergency indicator combination "
                    "detected. Seek immediate professional/"
                    "emergency medical care."
                )
            }

    return {
        "emergency": False,
        "matched_indicator": None,
        "message": "No predefined emergency indicators detected."
    }