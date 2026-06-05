from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine
from app.models.user import User

from app.routers.auth import router as auth_router

from app.models.course import Course
from app.routers.course import (router as course_router)

from app.models.schedule import Schedule
from app.routers.schedule import (router as schedule_router)

# Membuat tabel users jika belum ada
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Campus Assignment Manager"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router
app.include_router(auth_router)
app.include_router(course_router)
app.include_router(schedule_router)

@app.get("/")
def root():
    return {
        "message": "Campus Assignment Manager API"
    }