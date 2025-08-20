from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asset_tag = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), nullable=True)
    location = db.Column(db.String(100), nullable=True)
    condition = db.Column(db.String(20), nullable=False, default='good')  # good, fair, needs_repair, broken
    purchase_date = db.Column(db.Date, nullable=True)
    warranty_expiry = db.Column(db.Date, nullable=True)
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    assignee = db.relationship('User', backref='assigned_assets')

    def __repr__(self):
        return f'<Asset {self.asset_tag}: {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'asset_tag': self.asset_tag,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'location': self.location,
            'condition': self.condition,
            'purchase_date': self.purchase_date.isoformat() if self.purchase_date else None,
            'warranty_expiry': self.warranty_expiry.isoformat() if self.warranty_expiry else None,
            'assigned_to': self.assigned_to,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'assignee_name': self.assignee.username if self.assignee else None
        }

