from fhir.resources.bundle import Bundle

def parse_bundle(raw: dict) -> dict:
    bundle = Bundle.model_validate(raw)
    
    patient_id = None
    for entry in bundle.entry or []:
        resource = entry.resource
        if resource.get_resource_type() == "Patient":
            patient_id = resource.id
            break
    
    if not patient_id:
        raise ValueError("No Patient resource found in bundle")
    
    return {"patient_id": patient_id}