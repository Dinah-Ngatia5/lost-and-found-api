from app.extensions import db
from sqlalchemy.sql import func

class Reward(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    date_paid = db.Column(db.Date, nullable=False)
    date_offered = db.Column(db.Date, server_default=func.current_date(), nullable=True)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_username = db.Column(db.String(80), nullable=False)
    payer_username = db.Column(db.String(80), nullable=False)
    payer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    found_report_id = db.Column(db.Integer, db.ForeignKey('found_report.id'), nullable=False)
    
    receiver = db.relationship('User', foreign_keys=[receiver_id], back_populates='rewards_received')
    payer = db.relationship('User', foreign_keys=[payer_id], back_populates='rewards_paid')
    found_report = db.relationship('FoundReport', back_populates='rewards')
