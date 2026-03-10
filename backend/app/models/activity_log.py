from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from ..database import Base


class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    task_id = Column(
        Integer,
        ForeignKey("tasks.id"),
        nullable=True,
        index=True,
    )

    category = Column(String(50), nullable=False)

    duration_minutes = Column(Integer, nullable=True)
    quantity = Column(Integer, nullable=True)

    notes = Column(String(1000), nullable=True)

    logged_at = Column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )

    user = relationship("User", back_populates="activity_logs")
    task = relationship("Task", back_populates="activity_logs")
