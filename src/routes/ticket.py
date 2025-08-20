from flask import Blueprint, jsonify, request
from src.models.ticket import Ticket, db
from datetime import datetime

ticket_bp = Blueprint('ticket', __name__)

@ticket_bp.route('/tickets', methods=['GET'])
def get_tickets():
    """Get all tickets with optional filtering"""
    status = request.args.get('status')
    priority = request.args.get('priority')
    assigned_to = request.args.get('assigned_to')
    
    query = Ticket.query
    
    if status:
        query = query.filter(Ticket.status == status)
    if priority:
        query = query.filter(Ticket.priority == priority)
    if assigned_to:
        query = query.filter(Ticket.assigned_to == assigned_to)
    
    tickets = query.order_by(Ticket.created_at.desc()).all()
    return jsonify({
        'success': True,
        'data': [ticket.to_dict() for ticket in tickets],
        'message': f'Retrieved {len(tickets)} tickets'
    })

@ticket_bp.route('/tickets', methods=['POST'])
def create_ticket():
    """Create a new ticket"""
    try:
        data = request.json
        
        ticket = Ticket(
            title=data['title'],
            description=data.get('description'),
            priority=data.get('priority', 'medium'),
            status=data.get('status', 'open'),
            category=data.get('category'),
            assigned_to=data.get('assigned_to'),
            created_by=data['created_by'],
            location=data.get('location')
        )
        
        db.session.add(ticket)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': ticket.to_dict(),
            'message': 'Ticket created successfully'
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'data': None,
            'message': 'Failed to create ticket',
            'errors': [str(e)]
        }), 400

@ticket_bp.route('/tickets/<int:ticket_id>', methods=['GET'])
def get_ticket(ticket_id):
    """Get a specific ticket by ID"""
    ticket = Ticket.query.get_or_404(ticket_id)
    return jsonify({
        'success': True,
        'data': ticket.to_dict(),
        'message': 'Ticket retrieved successfully'
    })

@ticket_bp.route('/tickets/<int:ticket_id>', methods=['PUT'])
def update_ticket(ticket_id):
    """Update a ticket"""
    try:
        ticket = Ticket.query.get_or_404(ticket_id)
        data = request.json
        
        ticket.title = data.get('title', ticket.title)
        ticket.description = data.get('description', ticket.description)
        ticket.priority = data.get('priority', ticket.priority)
        ticket.status = data.get('status', ticket.status)
        ticket.category = data.get('category', ticket.category)
        ticket.assigned_to = data.get('assigned_to', ticket.assigned_to)
        ticket.location = data.get('location', ticket.location)
        ticket.updated_at = datetime.utcnow()
        
        # Set resolved_at if status is resolved or closed
        if data.get('status') in ['resolved', 'closed'] and not ticket.resolved_at:
            ticket.resolved_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': ticket.to_dict(),
            'message': 'Ticket updated successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'data': None,
            'message': 'Failed to update ticket',
            'errors': [str(e)]
        }), 400

@ticket_bp.route('/tickets/<int:ticket_id>', methods=['DELETE'])
def delete_ticket(ticket_id):
    """Delete a ticket"""
    try:
        ticket = Ticket.query.get_or_404(ticket_id)
        db.session.delete(ticket)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': None,
            'message': 'Ticket deleted successfully'
        }), 204
        
    except Exception as e:
        return jsonify({
            'success': False,
            'data': None,
            'message': 'Failed to delete ticket',
            'errors': [str(e)]
        }), 400

@ticket_bp.route('/tickets/<int:ticket_id>/assign', methods=['PUT'])
def assign_ticket(ticket_id):
    """Assign a ticket to a user"""
    try:
        ticket = Ticket.query.get_or_404(ticket_id)
        data = request.json
        
        ticket.assigned_to = data['assigned_to']
        ticket.status = 'in_progress'
        ticket.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': ticket.to_dict(),
            'message': 'Ticket assigned successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'data': None,
            'message': 'Failed to assign ticket',
            'errors': [str(e)]
        }), 400

@ticket_bp.route('/tickets/<int:ticket_id>/status', methods=['PUT'])
def update_ticket_status(ticket_id):
    """Update ticket status"""
    try:
        ticket = Ticket.query.get_or_404(ticket_id)
        data = request.json
        
        old_status = ticket.status
        ticket.status = data['status']
        ticket.updated_at = datetime.utcnow()
        
        # Set resolved_at if status is resolved or closed
        if data['status'] in ['resolved', 'closed'] and old_status not in ['resolved', 'closed']:
            ticket.resolved_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': ticket.to_dict(),
            'message': 'Ticket status updated successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'data': None,
            'message': 'Failed to update ticket status',
            'errors': [str(e)]
        }), 400

