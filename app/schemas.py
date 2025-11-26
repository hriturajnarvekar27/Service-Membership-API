from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, List

class MemberBase(BaseModel):
    name: str
    phone: str
    status: Optional[str] = "active"

class MemberCreate(MemberBase):
    pass

class Member(MemberBase):
    id: int
    total_check_ins: int
    class Config:
        from_attributes = True

class PlanBase(BaseModel):
    name: str
    price: int
    duration_days: int

class PlanCreate(PlanBase):
    pass

class Plan(PlanBase):
    id: int
    class Config:
        from_attributes = True

class SubscriptionBase(BaseModel):
    member_id: int
    plan_id: int
    start_date: date

class Subscription(SubscriptionBase):
    id: int
    end_date: date
    class Config:
        from_attributes = True

class AttendanceCreate(BaseModel):
    member_id: int

class Attendance(BaseModel):
    id: int
    member_id: int
    check_in_time: datetime
    class Config:
        from_attributes = True
