"""SQLAlchemy models for tasks and tags."""
from __future__ import annotations

from . import db

# Association table for the many-to-many relation between tasks and tags

task_tags = db.Table(
    "task_tags",
    db.Column("task_id", db.Integer, db.ForeignKey("tasks.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id"), primary_key=True),
)


class Task(db.Model):
    """Represents a task item."""

    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text)

    tags = db.relationship(
        "Tag", secondary=task_tags, back_populates="tasks", lazy="dynamic"
    )

    def __repr__(self) -> str:  # pragma: no cover - simple representation
        return f"<Task {self.title}>"


class Tag(db.Model):
    """Represents a label attached to a task."""

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    tasks = db.relationship(
        "Task", secondary=task_tags, back_populates="tags", lazy="dynamic"
    )

    def __repr__(self) -> str:  # pragma: no cover - simple representation
        return f"<Tag {self.name}>"
