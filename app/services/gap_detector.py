# Care gap detection based on documented HCC codes
# Logic: certain HCC codes are clinically associated with others
# If a patient has HCC X but is missing HCC Y, that's a potential gap

# Comorbidity rules: if patient HAS these HCCs...
# ...check if they're MISSING these related HCCs
COMORBIDITY_RULES = {
    "HCC19": {  # Diabetes without Complication
        "check_for": ["HCC18", "HCC137", "HCC136", "HCC96"],
        "rationale": "Diabetic patients commonly develop CKD and hypertension"
    },
    "HCC18": {  # Diabetes with Chronic Complications
        "check_for": ["HCC137", "HCC136", "HCC135", "HCC85"],
        "rationale": "Diabetes with complications often co-occurs with CKD and heart failure"
    },
    "HCC85": {  # Congestive Heart Failure
        "check_for": ["HCC96", "HCC19", "HCC137"],
        "rationale": "Heart failure patients commonly have hypertension, diabetes, and CKD"
    },
    "HCC111": {  # COPD
        "check_for": ["HCC96", "HCC85"],
        "rationale": "COPD patients commonly develop hypertension and heart failure"
    },
}

# Priority scores for gap severity (higher = more urgent)
HCC_PRIORITY = {
    "HCC18":  1.0,  # Diabetes with complications — highest impact
    "HCC85":  0.9,  # Heart failure
    "HCC135": 0.9,  # CKD Stage 5
    "HCC136": 0.8,  # CKD Stage 4
    "HCC137": 0.7,  # CKD Stage 3
    "HCC19":  0.6,  # Diabetes without complications
    "HCC111": 0.5,  # COPD
    "HCC96":  0.4,  # Hypertension
}

def detect_gaps(conditions: list[dict]) -> list[dict]:
    # Get all HCC codes currently documented for this patient
    documented_hccs = set()
    for condition in conditions:
        if condition.get("hcc_mapping"):
            documented_hccs.add(condition["hcc_mapping"]["hcc_code"])

    gaps = []

    for hcc_code in documented_hccs:
        rule = COMORBIDITY_RULES.get(hcc_code)
        if not rule:
            continue

        for missing_hcc in rule["check_for"]:
            if missing_hcc not in documented_hccs:
                gaps.append({
                    "gap_hcc": missing_hcc,
                    "triggered_by": hcc_code,
                    "rationale": rule["rationale"],
                    "priority_score": HCC_PRIORITY.get(missing_hcc, 0.3)
                })

    # Sort by priority score, highest first
    gaps.sort(key=lambda x: x["priority_score"], reverse=True)

    return gaps