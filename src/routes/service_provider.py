from flask import Blueprint, request, jsonify
from src.models.service_provider import ServiceProvider, ProviderService, ProviderMetric, ProviderActivity, ServiceSchedule, db
from datetime import datetime
import uuid

service_provider_bp = Blueprint('service_provider', __name__)

# Get all service providers or filter by status
@service_provider_bp.route('/service_providers', methods=['GET'])
def get_service_providers():
    status = request.args.get('status')
    if status:
        providers = ServiceProvider.query.filter_by(status=status).all()
    else:
        providers = ServiceProvider.query.all()
    return jsonify([provider.to_dict() for provider in providers]), 200

# Get a single service provider by ID
@service_provider_bp.route('/service_providers/<int:id>', methods=['GET'])
def get_service_provider(id):
    provider = ServiceProvider.query.get_or_404(id)
    return jsonify(provider.to_dict()), 200

# Create a new service provider
@service_provider_bp.route('/service_providers', methods=['POST'])
def create_service_provider():
    data = request.get_json()
    if not data or not data.get('name') or not data.get('code'):
        return jsonify({'error': 'Name and code are required'}), 400
    
    if ServiceProvider.query.filter_by(code=data['code']).first():
        return jsonify({'error': 'Code already exists'}), 400
    
    provider = ServiceProvider(
        name=data['name'],
        code=data['code'],
        tagline=data.get('tagline'),
        description=data.get('description'),
        icon=data.get('icon'),
        contact_phone=data.get('contact_phone'),
        contact_email=data.get('contact_email'),
        operating_hours=data.get('operating_hours'),
        status=data.get('status', 'active')
    )
    db.session.add(provider)
    db.session.commit()
    return jsonify(provider.to_dict()), 201

# Update a service provider
@service_provider_bp.route('/service_providers/<int:id>', methods=['PUT'])
def update_service_provider(id):
    provider = ServiceProvider.query.get_or_404(id)
    data = request.get_json()
    
    provider.name = data.get('name', provider.name)
    provider.tagline = data.get('tagline', provider.tagline)
    provider.description = data.get('description', provider.description)
    provider.icon = data.get('icon', provider.icon)
    provider.contact_phone = data.get('contact_phone', provider.contact_phone)
    provider.contact_email = data.get('contact_email', provider.contact_email)
    provider.operating_hours = data.get('operating_hours', provider.operating_hours)
    provider.status = data.get('status', provider.status)
    
    db.session.commit()
    return jsonify(provider.to_dict()), 200

# Delete a service provider
@service_provider_bp.route('/service_providers/<int:id>', methods=['DELETE'])
def delete_service_provider(id):
    provider = ServiceProvider.query.get_or_404(id)
    db.session.delete(provider)
    db.session.commit()
    return jsonify({'message': 'Service provider deleted'}), 200

# Create a provider service
@service_provider_bp.route('/service_providers/<int:provider_id>/services', methods=['POST'])
def create_provider_service(provider_id):
    provider = ServiceProvider.query.get_or_404(provider_id)
    data = request.get_json()
    
    if not data or not data.get('name'):
        return jsonify({'error': 'Service name is required'}), 400
    
    service = ProviderService(
        provider_id=provider_id,
        name=data['name'],
        description=data.get('description'),
        is_active=data.get('is_active', True)
    )
    db.session.add(service)
    db.session.commit()
    return jsonify(service.to_dict()), 201

# Create a provider metric
@service_provider_bp.route('/service_providers/<int:provider_id>/metrics', methods=['POST'])
def create_provider_metric(provider_id):
    provider = ServiceProvider.query.get_or_404(provider_id)
    data = request.get_json()
    
    if not data or not data.get('metric_name') or not data.get('metric_value'):
        return jsonify({'error': 'Metric name and value are required'}), 400
    
    metric = ProviderMetric(
        provider_id=provider_id,
        metric_name=data['metric_name'],
        metric_value=data['metric_value'],
        metric_type=data.get('metric_type', 'text'),
        display_order=data.get('display_order', 0)
    )
    db.session.add(metric)
    db.session.commit()
    return jsonify(metric.to_dict()), 201

# Create a provider activity
@service_provider_bp.route('/service_providers/<int:provider_id>/activities', methods=['POST'])
def create_provider_activity(provider_id):
    provider = ServiceProvider.query.get_or_404(provider_id)
    data = request.get_json()
    
    if not data or not data.get('activity_type') or not data.get('description'):
        return jsonify({'error': 'Activity type and description are required'}), 400
    
    activity = ProviderActivity(
        provider_id=provider_id,
        activity_type=data['activity_type'],
        description=data['description'],
        activity_date=data.get('activity_date', datetime.utcnow())
    )
    db.session.add(activity)
    db.session.commit()
    return jsonify(activity.to_dict()), 201

# Create a service schedule
@service_provider_bp.route('/service_providers/<int:provider_id>/schedules', methods=['POST'])
def create_service_schedule(provider_id):
    provider = ServiceProvider.query.get_or_404(provider_id)
    data = request.get_json()
    
    if not data or not data.get('service_id') or not data.get('scheduled_date') or not data.get('scheduled_time'):
        return jsonify({'error': 'Service ID, scheduled date, and time are required'}), 400
    
    service = ProviderService.query.get_or_404(data['service_id'])
    if service.provider_id != provider_id:
        return jsonify({'error': 'Service does not belong to this provider'}), 400
    
    schedule = ServiceSchedule(
        provider_id=provider_id,
        service_id=data['service_id'],
        scheduled_date=datetime.fromisoformat(data['scheduled_date']),
        scheduled_time=datetime.strptime(data['scheduled_time'], '%H:%M:%S').time(),
        special_requirements=data.get('special_requirements'),
        status=data.get('status', 'scheduled'),
        requested_by=data.get('requested_by')
    )
    db.session.add(schedule)
    db.session.commit()
    return jsonify(schedule.to_dict()), 201