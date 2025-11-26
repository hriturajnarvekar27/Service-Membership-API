from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter()

@router.post("/", response_model=schemas.Member)
def create_member(member: schemas.MemberCreate, db: Session = Depends(get_db)):
    existing_member = db.query(models.Member).filter(models.Member.phone == member.phone).first()
    if existing_member:
        raise HTTPException(status_code=400, detail="Phone number already exists")
    
    new_member = models.Member(**member.dict())
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return new_member

@router.get("/", response_model=list[schemas.Member])
def get_all_members(status: str | None = None, db: Session = Depends(get_db)):
    query = db.query(models.Member)
    if status:
        query = query.filter(models.Member.status == status)
    return query.all()
