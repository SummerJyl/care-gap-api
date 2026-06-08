from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.patient import Patient, CareGap

router = APIRouter()

@router.get("/patients/{patient_id}")
def get_patient(patient_id: str, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {
        "patient_id": patient.id,
        "gender": patient.gender,
        "birth_date": patient.birth_date,
        "created_at": patient.created_at
    }

@router.get("/patients/{patient_id}/gaps")
def get_patient_gaps(patient_id: str, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    gaps = db.query(CareGap)\
        .filter(CareGap.patient_id == patient_id)\
        .order_by(CareGap.priority_score.desc())\
        .all()

    return {
        "patient_id": patient_id,
        "total_gaps": len(gaps),
        "care_gaps": [
            {
                "gap_hcc": g.gap_hcc,
                "triggered_by": g.triggered_by,
                "rationale": g.rationale,
                "priority_score": g.priority_score,
                "status": g.status,
                "created_at": g.created_at
            }
            for g in gaps
        ]
    }