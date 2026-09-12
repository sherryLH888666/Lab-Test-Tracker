from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TestRecordBase(BaseModel):
    sample_id: str
    test_name: str
    operator: Optional[str] = None
    equipment: Optional[str] = None
    result_value: Optional[float] = None
    unit: Optional[str] = None
    status: Optional[str] = "pending"
    note: Optional[str] = None


class TestRecordCreate(TestRecordBase):
    pass


class TestRecordUpdate(BaseModel):
    sample_id: Optional[str] = None
    test_name: Optional[str] = None
    operator: Optional[str] = None
    equipment: Optional[str] = None
    result_value: Optional[float] = None
    unit: Optional[str] = None
    status: Optional[str] = None
    note: Optional[str] = None


class TestRecordOut(TestRecordBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}
