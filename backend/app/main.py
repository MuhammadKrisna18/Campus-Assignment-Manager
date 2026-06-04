from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine
from app.models.user import User

from app.routers.auth import router as auth_router

# Membuat seluruh tabel yang terdaftar pada model
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Campus Assignment Manager"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)

@app.get("/")
def root():
    return {
        "message": "Campus Assignment Manager API"
    }