from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    priority = db.Column(db.String(20), nullable=False, default='medium')  # low, medium, high
    status = db.Column(db.String(20), nullable=False, default='open')  # open, in_progress, resolved, closed
    category = db.Column(db.String(50), nullable=True)
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    location = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = db.Column(db.DateTime, nullable=True)

    # Relationships
    assignee = db.relationship('User', foreign_keys=[assigned_to], backref='assigned_tickets')
    creator = db.relationship('User', foreign_keys=[created_by], backref='created_tickets')

    def __repr__(self):
        return f'<Ticket {self.title}>'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'status': self.status,
            'category': self.category,
            'assigned_to': self.assigned_to,
            'created_by': self.created_by,
            'location': self.location,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None,
            'assignee_name': self.assignee.username if self.assignee else None,
            'creator_name': self.creator.username if self.creator else None
        }

