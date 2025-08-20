import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.main import app
from src.models.user import User, db
from src.models.ticket import Ticket
from src.models.asset import Asset
from src.models.tool import Tool
from src.models.staff import Staff
from datetime import datetime, date

with app.app_context():
    # Create sample users
    admin = User(username='admin', email='admin@facilitiespro.com', role='admin')
    admin.set_password('admin123')
    
    manager = User(username='sifiso.shezi', email='sifiso@facilitiespro.com', role='manager')
    manager.set_password('manager123')
    
    tech1 = User(username='john.doe', email='john@facilitiespro.com', role='technician')
    tech1.set_password('tech123')
    
    db.session.add_all([admin, manager, tech1])
    db.session.commit()
    
    # Create sample tickets
    ticket1 = Ticket(
        title='Air conditioning not working in Conference Room A',
        description='The AC unit is not cooling properly',
        priority='high',
        status='open',
        category='HVAC',
        created_by=manager.id,
        location='Conference Room A'
    )
    
    ticket2 = Ticket(
        title='Broken light fixture in hallway',
        description='Fluorescent light is flickering',
        priority='medium',
        status='in_progress',
        category='Electrical',
        created_by=manager.id,
        assigned_to=tech1.id,
        location='Main Hallway'
    )
    
    db.session.add_all([ticket1, ticket2])
    
    # Create sample assets
    asset1 = Asset(
        asset_tag='AC-001',
        name='Conference Room A Air Conditioner',
        description='Central AC unit for conference room',
        category='HVAC',
        location='Conference Room A',
        condition='fair',
        purchase_date=date(2020, 1, 15)
    )
    
    asset2 = Asset(
        asset_tag='PROJ-001',
        name='Conference Room Projector',
        description='HD projector for presentations',
        category='Electronics',
        location='Conference Room A',
        condition='good',
        purchase_date=date(2022, 6, 10)
    )
    
    db.session.add_all([asset1, asset2])
    
    # Create sample tools
    tool1 = Tool(
        tool_name='Cordless Drill',
        tool_category='Power Tools',
        serial_number='CD-001',
        condition='good',
        status='available',
        location='Tool Storage'
    )
    
    tool2 = Tool(
        tool_name='Multimeter',
        tool_category='Electrical',
        serial_number='MM-001',
        condition='good',
        status='in_use',
        checked_out_to=tech1.id,
        checked_out_at=datetime.utcnow(),
        location='With Technician'
    )
    
    db.session.add_all([tool1, tool2])
    
    # Create sample staff
    staff1 = Staff(
        employee_id='EMP-001',
        name='Sifiso Shezi',
        department='Facilities',
        position='Facilities Manager',
        email='sifiso@facilitiespro.com',
        phone='+27-11-123-4567',
        status='active'
    )
    
    staff2 = Staff(
        employee_id='EMP-002',
        name='John Doe',
        department='Maintenance',
        position='Maintenance Technician',
        email='john@facilitiespro.com',
        phone='+27-11-123-4568',
        status='active'
    )
    
    db.session.add_all([staff1, staff2])
    
    db.session.commit()
    print('Sample data created successfully!')

