from sqlalchemy import Column, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class Patient(Base):
    __tablename__ = "patients"

    id = Column(String, primary_key=True)
    gender = Column(String)
    birth_date = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    conditions = relationship("Condition", back_populates="patient")
    gaps = relationship("CareGap", back_populates="patient")


class Condition(Base):
    __tablename__ = "conditions"

    id = Column(String, primary_key=True)
    patient_id = Column(String, ForeignKey("patients.id"))
    icd10_code = Column(String)
    display = Column(String)
    clinical_status = Column(String)
    onset_date = Column(String)
    hcc_mapping = Column(JSON)

    patient = relationship("Patient", back_populates="conditions")


class CareGap(Base):
    __tablename__ = "care_gaps"

    id = Column(String, primary_key=True)
    patient_id = Column(String, ForeignKey("patients.id"))
    gap_hcc = Column(String)
    triggered_by = Column(String)
    rationale = Column(String)
    priority_score = Column(Float)
    status = Column(String, default="open")
    created_at = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient", back_populates="gaps")