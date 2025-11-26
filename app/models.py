from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Member(Base):
    __tablename__ = "members"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    status = Column(String, default="active")
    total_check_ins = Column(Integer, default=0)

    subscriptions = relationship("Subscription", back_populates="member")
    attendance = relationship("Attendance", back_populates="member")

class Plan(Base):
    __tablename__ = "plans"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    duration_days = Column(Integer, nullable=False)

class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id"))
    plan_id = Column(Integer, ForeignKey("plans.id"))
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    member = relationship("Member", back_populates="subscriptions")
    plan = relationship("Plan")

class Attendance(Base):
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey("members.id"))
    check_in_time = Column(DateTime, default=datetime.utcnow)

    member = relationship("Member", back_populates="attendance")
