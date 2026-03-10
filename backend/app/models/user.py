from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from ..database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    email = Column(
        String(255),
        nullable=False,
        unique=True,
        index=True,
    )

    hashed_password = Column(
        String(255),
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default="now()",
    )

    projects = relationship("Project", back_populates="user")
    tasks = relationship("Task", back_populates="user")
    activity_logs = relationship("ActivityLog", back_populates="user")
