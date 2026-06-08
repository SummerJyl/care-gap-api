from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.services.fhir_parser import parse_bundle
from app.services.gap_detector import detect_gaps
from app.database import get_db
from app.models.patient import Patient, Condition, CareGap
import uuid

router = APIRouter()

@router.post("/ingest")
async def ingest_bundle(bundle: dict, db: Session = Depends(get_db)):
    try:
        result = parse_bundle(bundle)
        gaps = detect_gaps(result["conditions"])

        # Save patient
        patient = db.query(Patient).filter(Patient.id == result["patient_id"]).first()
        if not patient:
            patient = Patient(id=result["patient_id"])
            db.add(patient)

        # Save conditions
        for c in result["conditions"]:
            condition = Condition(
                id=str(uuid.uuid4()),
                patient_id=result["patient_id"],
                icd10_code=c["icd10_code"],
                display=c["display"],
                clinical_status=c["clinical_status"],
                onset_date=c["onset_date"],
                hcc_mapping=c["hcc_mapping"]
            )
            db.add(condition)

        # Save care gaps
        for g in gaps:
            care_gap = CareGap(
                id=str(uuid.uuid4()),
                patient_id=result["patient_id"],
                gap_hcc=g["gap_hcc"],
                triggered_by=g["triggered_by"],
                rationale=g["rationale"],
                priority_score=g["priority_score"]
            )
            db.add(care_gap)

        db.commit()

        return {
            "status": "accepted",
            "patient_id": result["patient_id"],
            "conditions": result["conditions"],
            "care_gaps": gaps
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=422, detail=str(e))