from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, date
from app.database import get_db
from app import models, schemas

router = APIRouter()

@router.post("/check-in", response_model=schemas.Attendance)
def check_in(attendance: schemas.AttendanceCreate, db: Session = Depends(get_db)):
    member = db.query(models.Member).filter(models.Member.id == attendance.member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    today = date.today()
    subscription = db.query(models.Subscription).filter(
        models.Subscription.member_id == attendance.member_id,
        models.Subscription.start_date <= today,
        models.Subscription.end_date >= today
    ).first()

    if not subscription:
        raise HTTPException(status_code=400, detail="No active subscription for this member")

    new_attendance = models.Attendance(
        member_id=attendance.member_id,
        check_in_time=datetime.utcnow()
    )

    db.add(new_attendance)
    db.commit()
    db.refresh(new_attendance)
    return new_attendance

@router.get("/{member_id}", response_model=list[schemas.Attendance])
def get_attendance(member_id: int, db: Session = Depends(get_db)):
    records = db.query(models.Attendance).filter(models.Attendance.member_id == member_id).all()
    if not records:
        raise HTTPException(status_code=404, detail="No attendance records found")
    return records
