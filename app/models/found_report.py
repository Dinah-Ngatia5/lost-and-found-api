from app.extensions import db
from app.models.item import Item

class FoundReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    item_name = db.Column(db.String(150), nullable=True)
    description = db.Column(db.String(255), nullable=True)
    date_found = db.Column(db.Date, nullable=False)
    time_found = db.Column(db.Time, nullable=False)
    primary_color = db.Column(db.String(50), nullable=True)
    secondary_color = db.Column(db.String(50), nullable=True)
    place_found = db.Column(db.String(255), nullable=False)
    upload_image = db.Column(db.String(250), nullable=True)
    contact = db.Column(db.String(255), nullable=True)  # Contact information

    # Relationships
    user = db.relationship('User', back_populates='found_reports')
    item = db.relationship('Item', back_populates='found_reports')
    claims = db.relationship('Claim', back_populates='found_report')
    rewards = db.relationship('Reward', back_populates='found_report')  

    @staticmethod
    def get_item_by_id(item_id):
        return Item.query.get(item_id)

    @staticmethod
    def get_item_by_name(name):
        return Item.query.filter_by(name=name).first()

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'item_id': self.item_id,
            'item_name': self.item_name,
            'description': self.description,
            'date_found': self.date_found.isoformat(),  # Convert date to string
            'time_found': str(self.time_found),  # Convert time to string
            'primary_color': self.primary_color,
            'secondary_color': self.secondary_color,
            'place_found': self.place_found,
            'upload_image': self.upload_image,
            'contact': self.contact,
            'claims': [claim.to_dict() for claim in self.claims],
            'rewards': [reward.to_dict() for reward in self.rewards]
        }
