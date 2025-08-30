#!/usr/bin/env python3

import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from src.models.user import db
from src.models.service_provider import ServiceProvider, ProviderService, ProviderMetric, ProviderActivity
from src.main import app
from datetime import datetime, timedelta
import random

def create_service_provider_data():
    """Create sample service provider data"""
    
    with app.app_context():
        # Clear existing service provider data
        ProviderActivity.query.delete()
        ProviderMetric.query.delete()
        ProviderService.query.delete()
        ServiceProvider.query.delete()

        # Create service providers
        providers_data = [
            {
                'name': 'STORES & INFRASTRUCTURE',
                'code': 'stores',
                'tagline': 'Precision Management | ISO 41001 Excellence',
                'description': 'Comprehensive asset management and infrastructure oversight for Derivco Durban facilities.',
                'icon': 'fas fa-warehouse',
                'contact_phone': '+27 31 123 4567',
                'contact_email': 'stores@derivco.co.za',
                'operating_hours': 'Mon-Fri: 8:00 AM - 5:00 PM',
                'services': [
                    'Asset Register Management',
                    'Work Order Processing',
                    'Inventory Control',
                    'Compliance Monitoring'
                ],
                'metrics': [
                    ('Assets Under Management', '428', 'number', 1),
                    ('Inventory Accuracy', '97.3%', 'percentage', 2),
                    ('Active Work Orders', '12', 'number', 3),
                    ('Compliance Score', '100%', 'percentage', 4)
                ],
                'activities': [
                    ('task_completed', 'Asset PROJ-001 registered and tagged'),
                    ('task_completed', 'Work order #WO-2025-001 completed'),
                    ('audit_completed', 'Monthly inventory audit completed'),
                    ('compliance_check', 'ISO 41001 compliance review passed')
                ]
            },
            {
                'name': 'LEITCH LANDSCAPE',
                'code': 'leitch',
                'tagline': 'Commercial Landscaping Services',
                'description': 'Professional landscaping and grounds maintenance services for corporate facilities.',
                'icon': 'fas fa-tree',
                'contact_phone': '+27 31 234 5678',
                'contact_email': 'info@leitchlandscape.co.za',
                'operating_hours': 'Mon-Fri: 7:00 AM - 4:00 PM',
                'services': [
                    'Landscape Design & Installation',
                    'Grounds Maintenance',
                    'Irrigation Systems',
                    'Seasonal Plantings'
                ],
                'metrics': [
                    ('Hours This Week', '24', 'number', 1),
                    ('Tasks Completed', '9', 'number', 2),
                    ('Active Projects', '3', 'number', 3),
                    ('Client Satisfaction', '98%', 'percentage', 4)
                ],
                'activities': [
                    ('maintenance', 'Completed weekly lawn maintenance'),
                    ('installation', 'Installed new irrigation system - Block A'),
                    ('preparation', 'Seasonal flower bed preparation'),
                    ('assessment', 'Tree pruning and health assessment')
                ]
            },
            {
                'name': 'SABELIWE GARDEN',
                'code': 'sabeliwe',
                'tagline': 'Garden & Property Maintenance',
                'description': 'Specialized garden maintenance and property care services.',
                'icon': 'fas fa-leaf',
                'contact_phone': '+27 31 345 6789',
                'contact_email': 'contact@sabeliwegarden.co.za',
                'operating_hours': 'Mon-Fri: 7:30 AM - 4:30 PM',
                'services': [
                    'Garden Maintenance',
                    'Plant Care & Nurturing',
                    'Pest Control',
                    'Seasonal Garden Planning'
                ],
                'metrics': [
                    ('Hours This Week', '18', 'number', 1),
                    ('Tasks Completed', '7', 'number', 2),
                    ('Active Projects', '2', 'number', 3),
                    ('Garden Health Score', '95%', 'percentage', 4)
                ],
                'activities': [
                    ('maintenance', 'Completed rose garden pruning'),
                    ('treatment', 'Applied organic fertilizer treatment'),
                    ('inspection', 'Pest control inspection passed'),
                    ('installation', 'New herb garden installation started')
                ]
            },
            {
                'name': 'CSG FOODS',
                'code': 'csg',
                'tagline': 'Canteen & Catering Services',
                'description': 'Professional food service and catering for corporate dining facilities.',
                'icon': 'fas fa-utensils',
                'contact_phone': '+27 31 456 7890',
                'contact_email': 'catering@csgfoods.co.za',
                'operating_hours': 'Mon-Fri: 6:00 AM - 6:00 PM',
                'services': [
                    'Daily Meal Service',
                    'Special Event Catering',
                    'Menu Planning',
                    'Food Safety Compliance'
                ],
                'metrics': [
                    ('Meals Served Today', '342', 'number', 1),
                    ('Customer Satisfaction', '94%', 'percentage', 2),
                    ('Special Events', '2', 'number', 3),
                    ('Food Safety Score', '100%', 'percentage', 4)
                ],
                'activities': [
                    ('service', 'Served 342 meals today'),
                    ('catering', 'Catered executive board meeting'),
                    ('planning', 'Weekly menu planning completed'),
                    ('audit', 'Food safety audit passed with excellence')
                ]
            },
            {
                'name': 'LIVCLEAN',
                'code': 'livclean',
                'tagline': 'Cleaning & Sanitation Services',
                'description': 'Professional cleaning and sanitation services for corporate facilities.',
                'icon': 'fas fa-broom',
                'contact_phone': '+27 31 567 8901',
                'contact_email': 'services@livclean.co.za',
                'operating_hours': 'Mon-Fri: 6:00 AM - 10:00 PM',
                'services': [
                    'Daily Office Cleaning',
                    'Deep Sanitization',
                    'Restroom Maintenance',
                    'Waste Management'
                ],
                'metrics': [
                    ('Areas Completed', '98%', 'percentage', 1),
                    ('Quality Score', '4.8/5', 'text', 2),
                    ('Special Requests', '2', 'number', 3),
                    ('Compliance Rate', '100%', 'percentage', 4)
                ],
                'activities': [
                    ('cleaning', 'Completed daily office cleaning rounds'),
                    ('sanitization', 'Deep sanitization of conference rooms'),
                    ('maintenance', 'Restroom supplies restocked'),
                    ('inspection', 'Quality inspection passed - all areas')
                ]
            }
        ]

        for provider_data in providers_data:
            # Create provider
            provider = ServiceProvider(
                name=provider_data['name'],
                code=provider_data['code'],
                tagline=provider_data['tagline'],
                description=provider_data['description'],
                icon=provider_data['icon'],
                contact_phone=provider_data['contact_phone'],
                contact_email=provider_data['contact_email'],
                operating_hours=provider_data['operating_hours']
            )
            db.session.add(provider)
            db.session.flush()  # Get the ID

            # Create services
            for service_name in provider_data['services']:
                service = ProviderService(
                    provider_id=provider.id,
                    name=service_name,
                    description=f'{service_name} provided by {provider.name}'
                )
                db.session.add(service)

            # Create metrics
            for metric_name, metric_value, metric_type, display_order in provider_data['metrics']:
                metric = ProviderMetric(
                    provider_id=provider.id,
                    metric_name=metric_name,
                    metric_value=metric_value,
                    metric_type=metric_type,
                    display_order=display_order
                )
                db.session.add(metric)

            # Create activities
            for activity_type, description in provider_data['activities']:
                # Create activities with different timestamps
                activity_date = datetime.now() - timedelta(hours=random.randint(1, 24))
                activity = ProviderActivity(
                    provider_id=provider.id,
                    activity_type=activity_type,
                    description=description,
                    activity_date=activity_date
                )
                db.session.add(activity)

        db.session.commit()
        print("Service provider data created successfully!")

if __name__ == '__main__':
    create_service_provider_data()