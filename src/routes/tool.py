from flask import Blueprint, jsonify, request
from src.models.tool import Tool, db
from datetime import datetime

tool_bp = Blueprint('tool', __name__)

@tool_bp.route('/tools', methods=['GET'])
def get_tools():
    """Get all tools with optional filtering"""
    category = request.args.get('category')
    condition = request.args.get('condition')
    status = request.args.get('status')
    
    query = Tool.query
    
    if category:
        query = query.filter(Tool.tool_category == category)
    if condition:
        query = query.filter(Tool.condition == condition)
    if status:
        query = query.filter(Tool.status == status)
    
    tools = query.order_by(Tool.created_at.desc()).all()
    return jsonify({
        'success': True,
        'data': [tool.to_dict() for tool in tools],
        'message': f'Retrieved {len(tools)} tools'
    })

@tool_bp.route('/tools', methods=['POST'])
def create_tool():
    """Create a new tool"""
    try:
        data = request.json
        
        tool = Tool(
            tool_name=data['tool_name'],
            tool_category=data.get('tool_category'),
            serial_number=data.get('serial_number'),
            condition=data.get('condition', 'good'),
            status=data.get('status', 'available'),
            location=data.get('location')
        )
        
        db.session.add(tool)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': tool.to_dict(),
            'message': 'Tool created successfully'
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'data': None,
            'message': 'Failed to create tool',
            'errors': [str(e)]
        }), 400

@tool_bp.route('/tools/<int:tool_id>', methods=['GET'])
def get_tool(tool_id):
    """Get a specific tool by ID"""
    tool = Tool.query.get_or_404(tool_id)
    return jsonify({
        'success': True,
        'data': tool.to_dict(),
        'message': 'Tool retrieved successfully'
    })

@tool_bp.route('/tools/<int:tool_id>', methods=['PUT'])
def update_tool(tool_id):
    """Update a tool"""
    try:
        tool = Tool.query.get_or_404(tool_id)
        data = request.json
        
        tool.tool_name = data.get('tool_name', tool.tool_name)
        tool.tool_category = data.get('tool_category', tool.tool_category)
        tool.serial_number = data.get('serial_number', tool.serial_number)
        tool.condition = data.get('condition', tool.condition)
        tool.status = data.get('status', tool.status)
        tool.location = data.get('location', tool.location)
        tool.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': tool.to_dict(),
            'message': 'Tool updated successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'data': None,
            'message': 'Failed to update tool',
            'errors': [str(e)]
        }), 400

@tool_bp.route('/tools/<int:tool_id>', methods=['DELETE'])
def delete_tool(tool_id):
    """Delete a tool"""
    try:
        tool = Tool.query.get_or_404(tool_id)
        db.session.delete(tool)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': None,
            'message': 'Tool deleted successfully'
        }), 204
        
    except Exception as e:
        return jsonify({
            'success': False,
            'data': None,
            'message': 'Failed to delete tool',
            'errors': [str(e)]
        }), 400

@tool_bp.route('/tools/<int:tool_id>/checkout', methods=['POST'])
def checkout_tool(tool_id):
    """Check out a tool to a user"""
    try:
        tool = Tool.query.get_or_404(tool_id)
        data = request.json
        
        if tool.status != 'available':
            return jsonify({
                'success': False,
                'data': None,
                'message': 'Tool is not available for checkout',
                'errors': ['Tool status must be available']
            }), 400
        
        tool.status = 'in_use'
        tool.checked_out_to = data['user_id']
        tool.checked_out_at = datetime.utcnow()
        tool.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': tool.to_dict(),
            'message': 'Tool checked out successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'data': None,
            'message': 'Failed to checkout tool',
            'errors': [str(e)]
        }), 400

@tool_bp.route('/tools/<int:tool_id>/checkin', methods=['POST'])
def checkin_tool(tool_id):
    """Check in a tool"""
    try:
        tool = Tool.query.get_or_404(tool_id)
        
        if tool.status != 'in_use':
            return jsonify({
                'success': False,
                'data': None,
                'message': 'Tool is not checked out',
                'errors': ['Tool status must be in_use']
            }), 400
        
        tool.status = 'available'
        tool.checked_out_to = None
        tool.checked_out_at = None
        tool.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': tool.to_dict(),
            'message': 'Tool checked in successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'data': None,
            'message': 'Failed to checkin tool',
            'errors': [str(e)]
        }), 400

