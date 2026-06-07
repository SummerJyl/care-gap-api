from fhir.resources.bundle import Bundle
from app.services.hcc_mapper import map_icd10_to_hcc

def parse_bundle(raw: dict) -> dict:
    bundle = Bundle.model_validate(raw)
    
    patient_id = None
    conditions = []

    for entry in bundle.entry or []:
        resource = entry.resource
        resource_type = resource.get_resource_type()

        if resource_type == "Patient":
            patient_id = resource.id

        elif resource_type == "Condition":
            condition = extract_condition(resource)
            if condition:
                conditions.append(condition)

    if not patient_id:
        raise ValueError("No Patient resource found in bundle")

    return {
        "patient_id": patient_id,
        "conditions": conditions
    }

def extract_condition(resource) -> dict | None:
    try:
        icd10_code = None
        display = None

        if resource.code and resource.code.coding:
            for coding in resource.code.coding:
                if coding.system and "icd" in coding.system.lower():
                    icd10_code = coding.code
                    display = coding.display
                    break

        hcc = map_icd10_to_hcc(icd10_code) if icd10_code else None

        return {
            "icd10_code": icd10_code,
            "display": display,
            "clinical_status": resource.clinicalStatus.coding[0].code
                if resource.clinicalStatus and resource.clinicalStatus.coding
                else None,
            "onset_date": str(resource.onsetDateTime)
                if hasattr(resource, "onsetDateTime") and resource.onsetDateTime
                else None,
            "hcc_mapping": hcc
        }
    except Exception:
        return None