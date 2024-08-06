from app.extensions import db
from app.models.item import Item
from datetime import datetime

class LostReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    item_name = db.Column(db.String(150), nullable=True)
    place_lost = db.Column(db.String(150), nullable=False)
    date_lost = db.Column(db.Date, nullable=False)  
    time_lost = db.Column(db.Time, nullable=False) 
    contact = db.Column(db.String(255), nullable=True)  
    description = db.Column(db.String(255), nullable=True)
    primary_color = db.Column(db.String(50), nullable=True)
    secondary_color = db.Column(db.String(50), nullable=True)
    upload_image = db.Column(db.String(250), nullable=True)
    approved = db.Column(db.Boolean, default=False, nullable=False)

    user = db.relationship('User', back_populates='lost_reports')
    item = db.relationship('Item', back_populates='lost_reports')

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
            'place_lost': self.place_lost,
            'date_lost': self.date_lost.isoformat() if self.date_lost else None,
            'time_lost': self.time_lost.isoformat() if self.time_lost else None,
            'contact': self.contact,
            'description': self.description,
            'primary_color': self.primary_color,
            'secondary_color': self.secondary_color,
            'upload_image': self.upload_image,
            'approved': self.approved,
            'item': self.item.name if self.item else None  # Adjust according to the 'Item' model attributes
        }

