from app.extensions import db, bcrypt
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user')  
    lost_reports = db.relationship('LostReport', back_populates='user', lazy=True)
    found_reports = db.relationship('FoundReport', back_populates='user', lazy=True)
    claims = db.relationship('Claim', back_populates='claim_user', lazy=True)
    rewards_received = db.relationship('Reward', foreign_keys='Reward.receiver_id', back_populates='receiver', lazy=True)
    rewards_paid = db.relationship('Reward', foreign_keys='Reward.payer_id', back_populates='payer', lazy=True)
    reset_tokens = db.relationship('PasswordResetToken', back_populates='user', lazy=True)
    comments = db.relationship('Comment', back_populates='user')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        return self.role == 'admin'

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,

        }

  