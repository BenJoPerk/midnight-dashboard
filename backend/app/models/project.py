from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from ..database import Base


class Project(Base):
    __tablename__ = "projects"

    __table_args__ = (
        UniqueConstraint("user_id", "name", name="uq_user_project_name"),
    )

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)

    archived = Column(Boolean, nullable=False, default=False)

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default="now()",
    )

    user = relationship("User", back_populates="projects")
    tasks = relationship("Task", back_populates="project")
