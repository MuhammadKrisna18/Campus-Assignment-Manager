from fastapi import FastAPI

from app.core.database import Base, engine
from app.models.user import User

from app.routers.auth import router as auth_router

# Membuat seluruh tabel yang terdaftar pada model
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Campus Assignment Manager"
)

app.include_router(auth_router)

@app.get("/")
def root():
    return {
        "message": "Campus Assignment Manager API"
    }