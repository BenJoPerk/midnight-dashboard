from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from ..database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    project_id = Column(
        Integer,
        ForeignKey("projects.id"),
        nullable=True,
        index=True,
    )

    title = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)

    due_date = Column(DateTime(timezone=True), nullable=True)

    completed = Column(Boolean, nullable=False, default=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default="now()",
    )

    user = relationship("User", back_populates="tasks")
    project = relationship("Project", back_populates="tasks")
    activity_logs = relationship("ActivityLog", back_populates="task")
