from fastapi import APIRouter, HTTPException
from app.services.fhir_parser import parse_bundle
from app.services.gap_detector import detect_gaps

router = APIRouter()

@router.post("/ingest")
async def ingest_bundle(bundle: dict):
    try:
        result = parse_bundle(bundle)
        gaps = detect_gaps(result["conditions"])
        return {
            "status": "accepted",
            "patient_id": result["patient_id"],
            "conditions": result["conditions"],
            "care_gaps": gaps
        }
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))