from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class Tool(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tool_name = db.Column(db.String(200), nullable=False)
    tool_category = db.Column(db.String(50), nullable=True)
    serial_number = db.Column(db.String(100), unique=True, nullable=True)
    condition = db.Column(db.String(20), nullable=False, default='good')  # good, fair, needs_repair, broken
    status = db.Column(db.String(20), nullable=False, default='available')  # available, in_use, missing, obsolete
    location = db.Column(db.String(100), nullable=True)
    checked_out_to = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    checked_out_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    checked_out_user = db.relationship('User', backref='checked_out_tools')

    def __repr__(self):
        return f'<Tool {self.tool_name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'tool_name': self.tool_name,
            'tool_category': self.tool_category,
            'serial_number': self.serial_number,
            'condition': self.condition,
            'status': self.status,
            'location': self.location,
            'checked_out_to': self.checked_out_to,
            'checked_out_at': self.checked_out_at.isoformat() if self.checked_out_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'checked_out_user_name': self.checked_out_user.username if self.checked_out_user else None
        }

