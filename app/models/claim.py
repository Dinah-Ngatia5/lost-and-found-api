from app.extensions import db
from sqlalchemy.sql import func

class Claim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    found_report_id = db.Column(db.Integer, db.ForeignKey('found_report.id'), nullable=False)  # Updated field
    description = db.Column(db.String(255), nullable=False)
    date_claimed = db.Column(db.Date, server_default=func.current_date(), nullable=True)
    time_claimed = db.Column(db.Time, server_default=func.current_time(), nullable=True)

    # Relationships
    claim_user = db.relationship('User', back_populates='claims')
    found_report = db.relationship('FoundReport', back_populates='claims')  

    def __init__(self, user_id, found_report_id, description):  # Updated constructor
        self.user_id = user_id
        self.found_report_id = found_report_id
        self.description = description

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'found_report_id': self.found_report_id,
            'description': self.description,
            'date_claimed': self.date_claimed.isoformat() if self.date_claimed else None,
            'time_claimed': self.time_claimed.isoformat() if self.time_claimed else None,
            'claim_user_username': self.claim_user.username if self.claim_user else None,
            'found_report_item_name': self.found_report.item_name if self.found_report else None
        }
