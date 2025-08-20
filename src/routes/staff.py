from flask import Blueprint, jsonify, request
from src.models.staff import Staff, db
from datetime import datetime

staff_bp = Blueprint('staff', __name__)

@staff_bp.route('/staff', methods=['GET'])
def get_staff():
    """Get all staff with optional filtering"""
    department = request.args.get('department')
    status = request.args.get('status')
    
    query = Staff.query
    
    if department:
        query = query.filter(Staff.department == department)
    if status:
        query = query.filter(Staff.status == status)
    
    staff_members = query.order_by(Staff.created_at.desc()).all()
    return jsonify({
        'success': True,
        'data': [staff.to_dict() for staff in staff_members],
        'message': f'Retrieved {len(staff_members)} staff members'
    })

@staff_bp.route('/staff', methods=['POST'])
def create_staff():
    """Create a new staff member"""
    try:
        data = request.json
        
        staff = Staff(
            employee_id=data['employee_id'],
            name=data['name'],
            department=data.get('department'),
            position=data.get('position'),
            email=data.get('email'),
            phone=data.get('phone'),
            status=data.get('status', 'active')
        )
        
        db.session.add(staff)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': staff.to_dict(),
            'message': 'Staff member created successfully'
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'data': None,
            'message': 'Failed to create staff member',
            'errors': [str(e)]
        }), 400

@staff_bp.route('/staff/<int:staff_id>', methods=['GET'])
def get_staff_member(staff_id):
    """Get a specific staff member by ID"""
    staff = Staff.query.get_or_404(staff_id)
    return jsonify({
        'success': True,
        'data': staff.to_dict(),
        'message': 'Staff member retrieved successfully'
    })

@staff_bp.route('/staff/<int:staff_id>', methods=['PUT'])
def update_staff(staff_id):
    """Update a staff member"""
    try:
        staff = Staff.query.get_or_404(staff_id)
        data = request.json
        
        staff.employee_id = data.get('employee_id', staff.employee_id)
        staff.name = data.get('name', staff.name)
        staff.department = data.get('department', staff.department)
        staff.position = data.get('position', staff.position)
        staff.email = data.get('email', staff.email)
        staff.phone = data.get('phone', staff.phone)
        staff.status = data.get('status', staff.status)
        staff.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': staff.to_dict(),
            'message': 'Staff member updated successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'data': None,
            'message': 'Failed to update staff member',
            'errors': [str(e)]
        }), 400

@staff_bp.route('/staff/<int:staff_id>', methods=['DELETE'])
def delete_staff(staff_id):
    """Delete a staff member"""
    try:
        staff = Staff.query.get_or_404(staff_id)
        db.session.delete(staff)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': None,
            'message': 'Staff member deleted successfully'
        }), 204
        
    except Exception as e:
        return jsonify({
            'success': False,
            'data': None,
            'message': 'Failed to delete staff member',
            'errors': [str(e)]
        }), 400

