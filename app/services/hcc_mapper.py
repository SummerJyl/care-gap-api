# CMS-HCC V28 ICD-10 to HCC mapping (subset for demo)
# Full mapping: https://www.cms.gov/medicare/health-plans/medicareadvtgspecratestats/risk-adjustors

ICD10_TO_HCC = {
    # Diabetes
    "E11.9":  {"hcc_code": "HCC19",  "hcc_label": "Diabetes without Complication"},
    "E11.65": {"hcc_code": "HCC18",  "hcc_label": "Diabetes with Chronic Complications"},
    "E11.40": {"hcc_code": "HCC18",  "hcc_label": "Diabetes with Chronic Complications"},
    "E10.9":  {"hcc_code": "HCC19",  "hcc_label": "Diabetes without Complication"},

    # Chronic Kidney Disease
    "N18.3":  {"hcc_code": "HCC137", "hcc_label": "Chronic Kidney Disease, Stage 3"},
    "N18.4":  {"hcc_code": "HCC136", "hcc_label": "Chronic Kidney Disease, Stage 4"},
    "N18.5":  {"hcc_code": "HCC135", "hcc_label": "Chronic Kidney Disease, Stage 5"},

    # Heart Failure
    "I50.9":  {"hcc_code": "HCC85",  "hcc_label": "Congestive Heart Failure"},
    "I50.1":  {"hcc_code": "HCC85",  "hcc_label": "Congestive Heart Failure"},

    # COPD
    "J44.1":  {"hcc_code": "HCC111", "hcc_label": "COPD"},
    "J44.0":  {"hcc_code": "HCC111", "hcc_label": "COPD"},

    # Hypertension
    "I10":    {"hcc_code": "HCC96",  "hcc_label": "Hypertension"},
}

def map_icd10_to_hcc(icd10_code: str) -> dict | None:
    return ICD10_TO_HCC.get(icd10_code)