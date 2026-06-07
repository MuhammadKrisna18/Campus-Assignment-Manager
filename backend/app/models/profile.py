from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

from app.core.database import Base


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    full_name = Column(
        String,
        nullable=False
    )

    nickname = Column(
        String,
        nullable=True
    )

    nrp = Column(
        String,
        nullable=False
    )

    program = Column(
        String,
        nullable=False
    )

    department = Column(
        String,
        nullable=False
    )

    institution = Column(
        String,
        nullable=False
    )
