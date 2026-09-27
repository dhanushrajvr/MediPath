from langchain_core.tools import tool


DEPARTMENT_RULES = {

    "Cardiology": {
        "symptoms": [
            "chest pain",
            "palpitations"
        ],
        "conditions": [
            "Cardiac condition"
        ]
    },

    "Neurology": {
        "symptoms": [
            "severe headache",
            "migraine",
            "seizure",
            "numbness",
            "weakness"
        ],
        "conditions": [
            "Migraine"
        ]
    },

    "Dermatology": {
        "symptoms": [
            "skin rash",
            "itching",
            "skin irritation"
        ],
        "conditions": [
            "Dermatological condition",
            "Skin infection",
            "Allergic reaction"
        ]
    },

    "Orthopedics": {
        "symptoms": [
            "joint pain",
            "bone pain",
            "back pain"
        ],
        "conditions": [
            "Musculoskeletal condition",
            "Arthritis-related condition"
        ]
    },

    "ENT": {
        "symptoms": [
            "sore throat",
            "ear pain",
            "hearing problem"
        ],
        "conditions": [
            "Tonsillitis",
            "Pharyngitis"
        ]
    },

    "General Medicine": {
        "symptoms": [
            "fever",
            "cough",
            "nausea",
            "vomiting",
            "headache"
        ],
        "conditions": [
            "Viral illness",
            "Upper respiratory infection",
            "Gastrointestinal illness",
            "Influenza-like illness"
        ]
    }
}


@tool
def department_lookup(symptoms: list[str], possible_conditions: list[str]) -> dict:
    """
    Finds an appropriate department using symptoms
    and possible conditions.

    This is for routing and demonstration purposes,
    not diagnosis.
    """

    normalized_symptoms = {
        symptom.strip().lower()
        for symptom in symptoms
    }

    matched_departments = []

    for department, rules in DEPARTMENT_RULES.items():

        symptom_match = any(
            symptom in normalized_symptoms
            for symptom in rules["symptoms"]
        )

        condition_match = any(
            condition in possible_conditions
            for condition in rules["conditions"]
        )

        if symptom_match or condition_match:
            matched_departments.append(department)

    if not matched_departments:
        return {
            "department": "General Medicine",
            "reason": "No specific department matched. General Medicine can perform initial evaluation.",
            "matched_departments": ["General Medicine"]
        }

    # For this simple version, return the first matching department.
    department = matched_departments[0]

    return {
        "department": department,
        "reason": f"Symptoms/possible conditions matched the {department} routing rules.",
        "matched_departments": matched_departments
    }