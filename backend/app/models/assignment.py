from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Date
from sqlalchemy import ForeignKey

from app.core.database import Base


class Assignment(Base):
    __tablename__ = "assignments"

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

    course_id = Column(
        Integer,
        ForeignKey("courses.id"),
        nullable=False
    )

    title = Column(
        String,
        nullable=False
    )

    due_date = Column(
        Date,
        nullable=False
    )

    priority = Column(
        String,
        nullable=False,
        default="medium"
    )

    status = Column(
        String,
        nullable=False,
        default="pending"
    )
