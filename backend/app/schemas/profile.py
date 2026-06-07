from pydantic import BaseModel


class ProfileCreate(BaseModel):
    full_name: str
    nickname: str | None = None
    nrp: str
    program: str
    department: str
    institution: str


class ProfileUpdate(BaseModel):
    full_name: str
    nickname: str | None = None
    nrp: str
    program: str
    department: str
    institution: str


class ProfileResponse(BaseModel):
    id: int
    user_id: int
    full_name: str
    nickname: str | None = None
    nrp: str
    program: str
    department: str
    institution: str

    class Config:
        from_attributes = True
