import uuid
from datetime import datetime
from ..extensions import db


class Paper(db.Model):
    __tablename__ = "papers"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(512), nullable=False)
    authors = db.Column(db.Text)
    abstract = db.Column(db.Text)
    doi = db.Column(db.String(128), unique=True)
    arxiv_id = db.Column(db.String(64), unique=True)
    url = db.Column(db.String(256))
    source = db.Column(db.String(64))  # e.g. "openalex" or "semantic_scholar"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_papers = db.relationship("UserPaper", back_populates="paper", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Paper {self.title[:40]}...>"
