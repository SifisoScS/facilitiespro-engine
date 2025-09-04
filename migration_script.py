#!/usr/bin/env python3
"""
FacilitiesPro SQL Server Migration Script - Fixed Version
This script migrates data from SQLite to SQL Server and creates sample data
"""

import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

# Import Flask app first
from src.main import app

# Import database connection
from src.models.user import db

# Import models individually to avoid conflicts
from datetime import datetime, date, timedelta, timezone
import random
from sqlalchemy import text

def create_sample_facilities_assets():
    """Create sample assets that align with facilities stores Excel structure"""
    
    return [
        {
            'AssetType': 'Office Furniture',
            'Description': 'Executive Desk - Mahogany Finish',
            'SerialBarcode': 'DRV-DESK-001',
            'Building': 'Main Building',
            'Floor': 'Ground Floor',
            'RoomArea': 'Executive Office A',
            'AssignedTo': 'Executive Team',
            'PurchaseDate': date(2023, 1, 15),
            'Condition': 'Good',
            'WarrantyExpiry': date(2026, 1, 15),
            'InspectionDue': date(2025, 12, 1),
            'AssetStatus': 'Active',
            'Notes': 'High-quality executive desk with built-in cable management',
        },
        {
            'AssetType': 'IT Equipment',
            'Description': 'Dell OptiPlex 7090 Desktop Computer',
            'SerialBarcode': 'DRV-PC-001',
            'Building': 'Main Building',
            'Floor': '1st Floor',
            'RoomArea': 'Development Office',
            'AssignedTo': 'IT Department',
            'PurchaseDate': date(2024, 3, 10),
            'Condition': 'Excellent',
            'WarrantyExpiry': date(2027, 3, 10),
            'InspectionDue': date(2025, 9, 10),
            'AssetStatus': 'Active',
            'Notes': 'High-performance workstation for development team',
        },
        {
            'AssetType': 'HVAC Equipment',
            'Description': 'Daikin Inverter Air Conditioning Unit - 18000 BTU',
            'SerialBarcode': 'DRV-AC-001',
            'Building': 'Main Building',
            'Floor': 'Ground Floor',
            'RoomArea': 'Conference Room A',
            'AssignedTo': 'Facilities Management',
            'PurchaseDate': date(2022, 6, 20),
            'Condition': 'Good',
            'WarrantyExpiry': date(2025, 6, 20),
            'InspectionDue': date(2025, 10, 1),
            'AssetStatus': 'Active',
            'Notes': 'Energy efficient inverter AC unit with remote control',
        },
        {
            'AssetType': 'Audio Visual',
            'Description': 'Epson PowerLite L-Series Projector',
            'SerialBarcode': 'DRV-PROJ-001',
            'Building': 'Main Building',
            'Floor': '1st Floor',
            'RoomArea': 'Main Conference Room',
            'AssignedTo': 'General Use',
            'PurchaseDate': date(2023, 8, 5),
            'Condition': 'Excellent',
            'WarrantyExpiry': date(2026, 8, 5),
            'InspectionDue': date(2025, 11, 15),
            'AssetStatus': 'Active',
            'Notes': 'Laser projector with 4K support and wireless connectivity',
        },
        {
            'AssetType': 'Safety Equipment',
            'Description': 'Fire Extinguisher - ABC Dry Powder 5kg',
            'SerialBarcode': 'DRV-FIRE-001',
            'Building': 'Main Building',
            'Floor': 'Ground Floor',
            'RoomArea': 'Main Entrance',
            'AssignedTo': 'Safety Department',
            'PurchaseDate': date(2024, 1, 10),
            'Condition': 'Good',
            'WarrantyExpiry': date(2029, 1, 10),
            'InspectionDue': date(2025, 9, 1),
            'AssetStatus': 'Active',
            'Notes': 'Monthly pressure check required - compliant with SANS standards',
        },
        {
            'AssetType': 'Kitchen Equipment',
            'Description': 'Samsung Commercial Refrigerator 600L',
            'SerialBarcode': 'DRV-FRIDGE-001',
            'Building': 'Main Building',
            'Floor': 'Ground Floor',
            'RoomArea': 'Staff Kitchen',
            'AssignedTo': 'General Staff',
            'PurchaseDate': date(2023, 4, 12),
            'Condition': 'Good',
            'WarrantyExpiry': date(2025, 4, 12),
            'InspectionDue': date(2025, 10, 12),
            'AssetStatus': 'Active',
            'Notes': 'Energy star rated - temperature monitoring system installed',
        },
        {
            'AssetType': 'Office Furniture',
            'Description': 'Herman Miller Aeron Chair - Size B',
            'SerialBarcode': 'DRV-CHAIR-001',
            'Building': 'Main Building',
            'Floor': '1st Floor',
            'RoomArea': 'Development Office',
            'AssignedTo': 'John Smith',
            'PurchaseDate': date(2023, 2, 28),
            'Condition': 'Good',
            'WarrantyExpiry': date(2035, 2, 28),
            'InspectionDue': date(2026, 2, 1),
            'AssetStatus': 'Active',
            'Notes': 'Ergonomic office chair with 12-year warranty',
        },
        {
            'AssetType': 'Security Equipment',
            'Description': 'Hikvision IP Security Camera - 4MP',
            'SerialBarcode': 'DRV-CAM-001',
            'Building': 'Main Building',
            'Floor': 'Ground Floor',
            'RoomArea': 'Main Entrance',
            'AssignedTo': 'Security Department',
            'PurchaseDate': date(2023, 11, 8),
            'Condition': 'Excellent',
            'WarrantyExpiry': date(2026, 11, 8),
            'InspectionDue': date(2025, 11, 8),
            'AssetStatus': 'Active',
            'Notes': 'PoE powered camera with night vision capability',
        },
        {
            'AssetType': 'Printing Equipment',
            'Description': 'HP LaserJet Pro MFP M428fdw',
            'SerialBarcode': 'DRV-PRINTER-001',
            'Building': 'Main Building',
            'Floor': '1st Floor',
            'RoomArea': 'Printing Station',
            'AssignedTo': 'All Staff',
            'PurchaseDate': date(2023, 7, 14),
            'Condition': 'Good',
            'WarrantyExpiry': date(2024, 7, 14),
            'InspectionDue': date(2025, 9, 14),
            'AssetStatus': 'Active',
            'Notes': 'Multifunction printer with network connectivity and duplex printing',
        },
        {
            'AssetType': 'Cleaning Equipment',
            'Description': 'Karcher Professional Vacuum Cleaner',
            'SerialBarcode': 'DRV-VAC-001',
            'Building': 'Main Building',
            'Floor': 'Ground Floor',
            'RoomArea': 'Cleaning Storage',
            'AssignedTo': 'LivClean',
            'PurchaseDate': date(2024, 2, 5),
            'Condition': 'Excellent',
            'WarrantyExpiry': date(2026, 2, 5),
            'InspectionDue': date(2025, 12, 5),
            'AssetStatus': 'Active',
            'Notes': 'Industrial grade vacuum cleaner with HEPA filtration',
        },
    ]

def clear_existing_data():
    """Clear existing data using raw SQL to avoid model conflicts"""
    try:
        # Use raw SQL to clear data to avoid model conflicts
        db.session.execute(text("DELETE FROM ServiceSchedules"))
        db.session.execute(text("DELETE FROM ProviderActivities"))
        db.session.execute(text("DELETE FROM ProviderMetrics"))
        db.session.execute(text("DELETE FROM ProviderServices"))
        db.session.execute(text("DELETE FROM ServiceProviders"))
        db.session.execute(text("DELETE FROM Ticket"))
        db.session.execute(text("DELETE FROM Tool"))
        db.session.execute(text("DELETE FROM Asset"))
        db.session.execute(text("DELETE FROM Staff"))
        db.session.execute(text("DELETE FROM [User]"))

        db.session.commit()
        print("✓ Existing data cleared")

    except Exception as e:
        print(f"Note: Some tables may not exist yet: {e}")
        db.session.rollback()

def create_users_with_sql():
    """Create users using raw SQL to avoid model conflicts"""
    try:
        from werkzeug.security import generate_password_hash
        
        users_data = [
            ('admin', 'admin@derivco.com', generate_password_hash('admin123'), 'admin', 'System Administrator', 'IT'),
            ('sifiso.shezi', 'sifiso@derivco.com', generate_password_hash('manager123'), 'manager', 'Sifiso Shezi', 'Facilities Management'),
            ('john.doe', 'john@derivco.com', generate_password_hash('tech123'), 'technician', 'John Doe', 'Maintenance')
        ]
        
        for user in users_data:
            db.session.execute(
                text("""INSERT INTO [User] (Username, Email, PasswordHash, Role, FullName, Department, CreatedAt, UpdatedAt)
                   VALUES (:username, :email, :password_hash, :role, :full_name, :department, :created_at, :updated_at)"""),
                {
                    'username': user[0],
                    'email': user[1],
                    'password_hash': user[2],
                    'role': user[3],
                    'full_name': user[4],
                    'department': user[5],
                    'created_at': datetime.now(timezone.utc),
                    'updated_at': datetime.now(timezone.utc)
                }
            )
        
        db.session.commit()
        print("✓ Users created via SQL")
        
    except Exception as e:
        print(f"Error creating users: {e}")
        db.session.rollback()
        raise e

def create_staff_with_sql():
    """Create staff using raw SQL"""
    try:
        staff_data = [
            ('EMP-001', 'Sifiso Shezi', 'Facilities Management', 'Facilities Steward | Systems Architect',
             'sifiso@derivco.com', '+27-31-123-4567', 'Active', datetime(2020, 1, 15),
             'Facilities Management lead with expertise in ISO 41001 standards'),
            ('EMP-002', 'John Doe', 'Maintenance', 'Senior Maintenance Technician',
             'john@derivco.com', '+27-31-123-4568', 'Active', datetime(2021, 6, 10),
             'Certified HVAC and electrical maintenance specialist'),
            ('EMP-003', 'Sarah Wilson', 'IT Support', 'IT Support Specialist',
             'sarah@derivco.com', '+27-31-123-4569', 'Active', datetime(2022, 3, 20),
             'Hardware and software support for all facilities equipment')
        ]
        
        for emp_id, name, dept, pos, email, phone, status, hire_date, notes in staff_data:
            db.session.execute(
                text("""INSERT INTO Staff (EmployeeID, FullName, Department, Position, Email, Phone, Status, HireDate, Notes)
                   VALUES (:employee_id, :full_name, :department, :position, :email, :phone, :status, :hire_date, :notes)"""),
                {
                    'employee_id': emp_id,
                    'full_name': name,
                    'department': dept,
                    'position': pos,
                    'email': email,
                    'phone': phone,
                    'status': status,
                    'hire_date': hire_date,
                    'notes': notes
                }
            )
        
        db.session.commit()
        print("✓ Staff created via SQL")
        
    except Exception as e:
        print(f"Error creating staff: {e}")
        db.session.rollback()
        raise e

def create_assets_with_sql():
    """Create assets using raw SQL - fixed to match actual schema"""
    try:
        assets_data = create_sample_facilities_assets()
        
        for asset in assets_data:
            db.session.execute(
                text("""INSERT INTO Asset (AssetType, Description, SerialBarcode, Building, Floor, RoomArea,
                                    AssignedTo, PurchaseDate, Condition, WarrantyExpiry, InspectionDue,
                                    AssetStatus, Notes)
                   VALUES (:asset_type, :description, :serial_barcode, :building, :floor, :room_area,
                           :assigned_to, :purchase_date, :condition, :warranty_expiry, :inspection_due,
                           :asset_status, :notes)"""),
                {
                    'asset_type': asset['AssetType'],
                    'description': asset['Description'],
                    'serial_barcode': asset['SerialBarcode'],
                    'building': asset['Building'],
                    'floor': asset['Floor'],
                    'room_area': asset['RoomArea'],
                    'assigned_to': asset['AssignedTo'],
                    'purchase_date': asset['PurchaseDate'],
                    'condition': asset['Condition'],
                    'warranty_expiry': asset['WarrantyExpiry'],
                    'inspection_due': asset['InspectionDue'],
                    'asset_status': asset['AssetStatus'],
                    'notes': asset['Notes']
                }
            )
        
        db.session.commit()
        print(f"✓ {len(assets_data)} assets created via SQL")
        
    except Exception as e:
        print(f"Error creating assets: {e}")
        db.session.rollback()
        raise e

def create_tickets_with_sql():
    """Create tickets using raw SQL - fixed to match actual schema"""
    try:
        tickets_data = [
            ('Air conditioning maintenance required in Conference Room A',
             'Annual maintenance and filter replacement for AC unit DRV-AC-001',
             'Medium', 'Open', 'HVAC Maintenance', None, 'sifiso.shezi', 'Conference Room A',
             'Scheduled maintenance as per warranty requirements'),
            ('Projector lamp replacement needed',
             'Projector DRV-PROJ-001 showing dim output, lamp replacement required',
             'High', 'In Progress', 'Audio Visual', 'john.doe', 'sifiso.shezi', 'Main Conference Room',
             'Replacement lamp ordered, ETA 2 days'),
            ('Fire extinguisher inspection overdue',
             'Monthly pressure check required for DRV-FIRE-001',
             'High', 'Open', 'Safety Compliance', None, 'sifiso.shezi', 'Main Entrance',
             'Compliance requirement - must be completed within 48 hours')
        ]
        
        for title, desc, priority, status, category, assigned, created_by, location, notes in tickets_data:
            db.session.execute(
                text("""INSERT INTO Ticket (Title, Description, Priority, Status, Category, AssignedTo,
                                     CreatedBy, Location, Notes)
                   VALUES (:title, :description, :priority, :status, :category, :assigned_to,
                           :created_by, :location, :notes)"""),
                {
                    'title': title,
                    'description': desc,
                    'priority': priority,
                    'status': status,
                    'category': category,
                    'assigned_to': assigned,
                    'created_by': created_by,
                    'location': location,
                    'notes': notes
                }
            )
        
        db.session.commit()
        print("✓ Tickets created via SQL")
        
    except Exception as e:
        print(f"Error creating tickets: {e}")
        db.session.rollback()
        raise e

def create_tools_with_sql():
    """Create tools using raw SQL"""
    try:
        tools_data = [
            ('Digital Multimeter - Fluke 87V', 'Electrical Testing', 'FLK-87V-001',
             'Good', 'Available', 'Tool Storage Room', None, None, None,
             'Calibrated and ready for electrical diagnostics'),
            ('Cordless Drill Set - Makita DHP484', 'Power Tools', 'MAK-DHP484-001',
             'Excellent', 'In Use', 'With Technician', 'John Doe', 
             datetime.now(timezone.utc) - timedelta(hours=2), datetime.now(timezone.utc) + timedelta(days=1),
             'Complete set with bits and carrying case'),
            ('HVAC Gauge Set - Manifold', 'HVAC Tools', 'HVAC-MAN-001',
             'Good', 'Available', 'HVAC Tool Cabinet', None, None, None,
             'R410A compatible gauge set with hoses')
        ]
        
        for name, category, serial, condition, status, location, checked_to, checked_at, return_date, notes in tools_data:
            db.session.execute(
                text("""INSERT INTO Tool (ToolName, ToolCategory, SerialNumber, Condition, Status,
                                   Location, CheckedOutTo, CheckedOutAt, ExpectedReturnDate, Notes)
                   VALUES (:tool_name, :tool_category, :serial_number, :condition, :status,
                           :location, :checked_out_to, :checked_out_at, :expected_return_date, :notes)"""),
                {
                    'tool_name': name,
                    'tool_category': category,
                    'serial_number': serial,
                    'condition': condition,
                    'status': status,
                    'location': location,
                    'checked_out_to': checked_to,
                    'checked_out_at': checked_at,
                    'expected_return_date': return_date,
                    'notes': notes
                }
            )
        
        db.session.commit()
        print("✓ Tools created via SQL")
        
    except Exception as e:
        print(f"Error creating tools: {e}")
        db.session.rollback()
        raise e

def migrate_to_sql_server():
    """Main migration function using raw SQL to avoid model conflicts"""
    
    with app.app_context():
        try:
            _extracted_from_migrate_to_sql_server_6()
        except Exception as e:
            print(f"❌ Migration failed: {str(e)}")
            db.session.rollback()
            raise e


# TODO Rename this here and in `migrate_to_sql_server`
def _extracted_from_migrate_to_sql_server_6():
    print("Starting migration to SQL Server...")

    # Create all tables
    db.create_all()
    print("✓ Database tables created")

    # Clear existing data
    print("Clearing existing data...")
    clear_existing_data()

    # Create data using raw SQL to avoid model conflicts
    print("Creating sample users...")
    create_users_with_sql()

    print("Creating sample staff...")
    create_staff_with_sql()

    print("Creating sample assets...")
    create_assets_with_sql()

    print("Creating sample tickets...")
    create_tickets_with_sql()

    print("Creating sample tools...")
    create_tools_with_sql()

    print("✅ Migration completed successfully!")

    # Get counts using raw SQL
    user_count = db.session.execute(text("SELECT COUNT(*) FROM [User]")).scalar()
    staff_count = db.session.execute(text("SELECT COUNT(*) FROM Staff")).scalar()
    asset_count = db.session.execute(text("SELECT COUNT(*) FROM Asset")).scalar()
    ticket_count = db.session.execute(text("SELECT COUNT(*) FROM Ticket")).scalar()
    tool_count = db.session.execute(text("SELECT COUNT(*) FROM Tool")).scalar()

    print("\nSummary:")
    print(f"- Users: {user_count}")
    print(f"- Staff: {staff_count}")
    print(f"- Assets: {asset_count}")
    print(f"- Tickets: {ticket_count}")
    print(f"- Tools: {tool_count}")

if __name__ == '__main__':
    migrate_to_sql_server()