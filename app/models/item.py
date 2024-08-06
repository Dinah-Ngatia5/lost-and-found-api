from app.extensions import db

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(250), nullable=True)
    lost_reports = db.relationship('LostReport', back_populates='item', lazy=True)  
    found_reports = db.relationship('FoundReport', back_populates='item', lazy=True)
    comments = db.relationship('Comment', back_populates='item', lazy=True)
    is_returned = db.Column(db.Boolean, default=False, nullable=False)
    is_claimed = db.Column(db.Boolean, default=False, nullable=False)
    is_recovered = db.Column(db.Boolean, default=False, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'image_url': self.image_url,
            'is_returned': self.is_returned,
            'is_claimed': self.is_claimed,
            'is_recovered': self.is_recovered,
            'lost_reports': [{'id': report.id, 'user_id': report.user_id} for report in self.lost_reports],
            'found_reports': [{'id': report.id, 'user_id': report.user_id} for report in self.found_reports],
            'comments': [
                {
                    'id': comment.id,
                    'user_id': comment.user_id,
                    'user_username': comment.user.username if comment.user else None,
                    'content': comment.content,
                    'timestamp': comment.timestamp.isoformat() if comment.timestamp else None
                } for comment in self.comments
            ]
        }

