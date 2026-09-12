from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from datetime import datetime
from .database import Base


class TestRecord(Base):
    __tablename__ = "test_records"

    id = Column(Integer, primary_key=True, index=True)
    sample_id = Column(String(50), index=True, nullable=False)
    test_name = Column(String(100), nullable=False)
    operator = Column(String(100))
    equipment = Column(String(100))
    result_value = Column(Float)
    unit = Column(String(20))
    status = Column(String(20), default="pending")  # pending | pass | fail
    note = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
