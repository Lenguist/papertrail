import uuid
from datetime import datetime
from ..extensions import db


class UserPaper(db.Model):
    __tablename__ = "user_papers"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    paper_id = db.Column(db.String(36), db.ForeignKey("papers.id"), nullable=False)
    status = db.Column(db.String(32), default="to_read")  # "to_read" | "reading" | "finished"
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="user_papers")
    paper = db.relationship("Paper", back_populates="user_papers")

    __table_args__ = (db.UniqueConstraint("user_id", "paper_id", name="_user_paper_uc"),)

    def __repr__(self):
        return f"<UserPaper user={self.user_id}, paper={self.paper_id}>"
