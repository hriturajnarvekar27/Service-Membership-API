from fastapi import FastAPI
from .database import Base, engine
from .routers import members, plans, subscriptions, attendance

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Service Membership API",
    description="Backend API for managing gym/salon/coaching memberships",
    version="1.0.0"
)

app.include_router(members.router, prefix="/members", tags=["Members"])
app.include_router(plans.router, prefix="/plans", tags=["Plans"])
app.include_router(subscriptions.router, prefix="/subscriptions", tags=["Subscriptions"])
app.include_router(attendance.router, prefix="/attendance", tags=["Attendance"])
