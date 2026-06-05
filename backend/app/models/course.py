from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Date
from sqlalchemy import Time
from sqlalchemy import ForeignKey

from app.core.database import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    course_name = Column(
        String,
        nullable=False
    )

    credits = Column(
        Integer,
        nullable=False
    )

    class_name = Column(
        String,
        nullable=False
    )

    lecturer_name = Column(
        String,
        nullable=False
    )

    day = Column(
        String,
        nullable=False
    )

    schedule_date = Column(
        Date,
        nullable=False
    )

    schedule_time = Column(
        Time,
        nullable=False
    )