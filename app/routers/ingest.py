from fastapi import APIRouter, HTTPException
from app.services.fhir_parser import parse_bundle

router = APIRouter()

@router.post("/ingest")
async def ingest_bundle(bundle: dict):
    try:
        result = parse_bundle(bundle)
        return {"status": "accepted", "patient_id": result["patient_id"]}
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))