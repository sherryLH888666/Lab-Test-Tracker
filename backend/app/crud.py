from sqlalchemy.orm import Session
import random
from . import models, schemas


def _apply_filters(q, status, keyword):
    if status:
        q = q.filter(models.TestRecord.status == status)
    if keyword:
        q = q.filter(
            models.TestRecord.sample_id.contains(keyword)
            | models.TestRecord.test_name.contains(keyword)
        )
    return q


def get_records(db: Session, skip=0, limit=50, status=None, keyword=None):
    q = db.query(models.TestRecord)
    q = _apply_filters(q, status, keyword)
    return q.order_by(models.TestRecord.id.desc()).offset(skip).limit(limit).all()


def count_records(db: Session, status=None, keyword=None):
    q = db.query(models.TestRecord)
    q = _apply_filters(q, status, keyword)
    return q.count()


def get_record(db: Session, record_id: int):
    return db.query(models.TestRecord).filter(models.TestRecord.id == record_id).first()


def create_record(db: Session, rec: schemas.TestRecordCreate):
    db_rec = models.TestRecord(**rec.model_dump())
    db.add(db_rec)
    db.commit()
    db.refresh(db_rec)
    return db_rec


def update_record(db: Session, record_id: int, rec: schemas.TestRecordUpdate):
    db_rec = get_record(db, record_id)
    if not db_rec:
        return None
    for k, v in rec.model_dump(exclude_unset=True).items():
        setattr(db_rec, k, v)
    db.commit()
    db.refresh(db_rec)
    return db_rec


def delete_record(db: Session, record_id: int):
    db_rec = get_record(db, record_id)
    if not db_rec:
        return False
    db.delete(db_rec)
    db.commit()
    return True


def bulk_create(db: Session, n: int):
    """Generate n mock records to demo large-dataset performance (pagination)."""
    tests = ["Tensile", "Insulation", "Dielectric", "Continuity", "Load", "Thermal"]
    eq = ["DMM-01", "Oscilloscope-A", "PowerSupply-X", "Chamber-3"]
    recs = []
    for i in range(n):
        recs.append(
            models.TestRecord(
                sample_id="SMP-%05d" % (i + 1),
                test_name=random.choice(tests),
                operator="op%d" % (i % 7),
                equipment=random.choice(eq),
                result_value=round(random.uniform(0, 100), 2),
                unit="unit",
                status=random.choice(["pass", "fail", "pending"]),
            )
        )
    db.bulk_save_objects(recs)
    db.commit()
    return n
