from pydantic import BaseModel


class CourseCreate(BaseModel):
    course_name: str
    credits: int
    class_name: str
    lecturer_name: str
    grade: str | None = None
    semester: int | None = None


class CourseResponse(BaseModel):
    id: int
    course_name: str
    credits: int
    class_name: str
    lecturer_name: str
    grade: str | None = None
    semester: int | None = None

    class Config:
        from_attributes = True


class CourseUpdate(BaseModel):
    course_name: str
    credits: int
    class_name: str
    lecturer_name: str
    grade: str | None = None
    semester: int | None = None