from .database import SessionLocal, engine, Base
from . import models, crud, schemas

SEED_SAMPLES = [
    ("SMP-00001", "Insulation Resistance", "Alice Chen", "Megohmmeter-A", 150.2, "MΩ", "pass", "Baseline sample"),
    ("SMP-00002", "Dielectric Withstand", "Bob Li", "Hipot-Tester", 3.5, "kV", "pass", ""),
    ("SMP-00003", "Continuity Test", "Carol Wu", "DMM-01", 0.02, "Ω", "fail", "High resistance"),
    ("SMP-00004", "Tensile Strength", "Alice Chen", "Tensile-Rig", 45.1, "MPa", "pass", ""),
    ("SMP-00005", "Thermal Cycling", "Dan Zhao", "Chamber-3", -40.0, "°C", "pending", "In progress"),
]


def seed_if_empty():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(models.TestRecord).count() == 0:
            for s in SEED_SAMPLES:
                rec = schemas.TestRecordCreate(
                    sample_id=s[0],
                    test_name=s[1],
                    operator=s[2],
                    equipment=s[3],
                    result_value=s[4],
                    unit=s[5],
                    status=s[6],
                    note=s[7],
                )
                crud.create_record(db, rec)
            return True
    finally:
        db.close()
    return False
