from src.models.user import db
from datetime import datetime

class ServiceProvider(db.Model):
    __tablename__ = 'service_providers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)  # e.g., 'stores', 'leitch', etc.
    tagline = db.Column(db.String(200))
    description = db.Column(db.Text)
    icon = db.Column(db.String(50))  # FontAwesome icon class
    contact_phone = db.Column(db.String(20))
    contact_email = db.Column(db.String(100))
    operating_hours = db.Column(db.String(100))
    status = db.Column(db.String(20), default='active')  # active, inactive, suspended
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    services = db.relationship('ProviderService', backref='provider', lazy=True, cascade='all, delete-orphan')
    metrics = db.relationship('ProviderMetric', backref='provider', lazy=True, cascade='all, delete-orphan')
    activities = db.relationship('ProviderActivity', backref='provider', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'tagline': self.tagline,
            'description': self.description,
            'icon': self.icon,
            'contact_phone': self.contact_phone,
            'contact_email': self.contact_email,
            'operating_hours': self.operating_hours,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'services': [service.to_dict() for service in self.services],
            'metrics': [metric.to_dict() for metric in self.metrics],
            'recent_activities': [activity.to_dict() for activity in self.activities[-5:]]  # Last 5 activities
        }

class ProviderService(db.Model):
    __tablename__ = 'provider_services'
    
    id = db.Column(db.Integer, primary_key=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('service_providers.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class ProviderMetric(db.Model):
    __tablename__ = 'provider_metrics'
    
    id = db.Column(db.Integer, primary_key=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('service_providers.id'), nullable=False)
    metric_name = db.Column(db.String(100), nullable=False)
    metric_value = db.Column(db.String(50), nullable=False)
    metric_type = db.Column(db.String(20), default='text')  # text, percentage, number, currency
    display_order = db.Column(db.Integer, default=0)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'metric_name': self.metric_name,
            'metric_value': self.metric_value,
            'metric_type': self.metric_type,
            'display_order': self.display_order,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class ProviderActivity(db.Model):
    __tablename__ = 'provider_activities'
    
    id = db.Column(db.Integer, primary_key=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('service_providers.id'), nullable=False)
    activity_type = db.Column(db.String(50), nullable=False)  # task_completed, service_scheduled, etc.
    description = db.Column(db.String(200), nullable=False)
    activity_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'activity_type': self.activity_type,
            'description': self.description,
            'activity_date': self.activity_date.isoformat() if self.activity_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class ServiceSchedule(db.Model):
    __tablename__ = 'service_schedules'
    
    id = db.Column(db.Integer, primary_key=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('service_providers.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('provider_services.id'), nullable=False)
    scheduled_date = db.Column(db.DateTime, nullable=False)
    scheduled_time = db.Column(db.Time, nullable=False)
    special_requirements = db.Column(db.Text)
    status = db.Column(db.String(20), default='scheduled')  # scheduled, in_progress, completed, cancelled
    requested_by = db.Column(db.Integer)  # Reference to user ID (simplified)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    provider = db.relationship('ServiceProvider', backref='schedules')
    service = db.relationship('ProviderService', backref='schedules')
    
    def to_dict(self):
        return {
            'id': self.id,
            'provider_id': self.provider_id,
            'service_id': self.service_id,
            'scheduled_date': self.scheduled_date.isoformat() if self.scheduled_date else None,
            'scheduled_time': self.scheduled_time.isoformat() if self.scheduled_time else None,
            'special_requirements': self.special_requirements,
            'status': self.status,
            'requested_by': self.requested_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'provider_name': self.provider.name if self.provider else None,
            'service_name': self.service.name if self.service else None
        }