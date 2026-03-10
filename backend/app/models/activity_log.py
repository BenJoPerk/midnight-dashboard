from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from ..database import Base


class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)

    category = Column(String, nullable=False)
    duration_minutes = Column(Integer, nullable=True)
    quantity = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)

    logged_at = Column(DateTime(timezone=True), nullable=False)

    user = relationship("User", back_populates="activity_logs")
    task = relationship("Task", back_populates="activity_logs")
