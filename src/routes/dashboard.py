from flask import Blueprint, jsonify
from src.models.ticket import Ticket
from src.models.asset import Asset
from src.models.tool import Tool
from src.models.staff import Staff
from src.models.user import db
from sqlalchemy import func

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    """Get dashboard statistics"""
    try:
        # Get counts
        total_tickets = Ticket.query.count()
        active_assets = Asset.query.filter(Asset.condition != 'broken').count()
        total_tools = Tool.query.count()
        total_staff = Staff.query.filter(Staff.status == 'active').count()
        
        # Get ticket stats by status
        ticket_stats = db.session.query(
            Ticket.status,
            func.count(Ticket.id).label('count')
        ).group_by(Ticket.status).all()
        
        # Get ticket stats by priority
        priority_stats = db.session.query(
            Ticket.priority,
            func.count(Ticket.id).label('count')
        ).group_by(Ticket.priority).all()
        
        # Get asset stats by condition
        asset_stats = db.session.query(
            Asset.condition,
            func.count(Asset.id).label('count')
        ).group_by(Asset.condition).all()
        
        # Get tool stats by status
        tool_stats = db.session.query(
            Tool.status,
            func.count(Tool.id).label('count')
        ).group_by(Tool.status).all()
        
        return jsonify({
            'success': True,
            'data': {
                'overview': {
                    'total_tickets': total_tickets,
                    'active_assets': active_assets,
                    'total_tools': total_tools,
                    'total_staff': total_staff
                },
                'ticket_by_status': {stat.status: stat.count for stat in ticket_stats},
                'ticket_by_priority': {stat.priority: stat.count for stat in priority_stats},
                'asset_by_condition': {stat.condition: stat.count for stat in asset_stats},
                'tool_by_status': {stat.status: stat.count for stat in tool_stats}
            },
            'message': 'Dashboard statistics retrieved successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'data': None,
            'message': 'Failed to retrieve dashboard statistics',
            'errors': [str(e)]
        }), 500

@dashboard_bp.route('/dashboard/recent-tickets', methods=['GET'])
def get_recent_tickets():
    """Get recent tickets for dashboard"""
    try:
        recent_tickets = Ticket.query.order_by(Ticket.created_at.desc()).limit(10).all()
        
        return jsonify({
            'success': True,
            'data': [ticket.to_dict() for ticket in recent_tickets],
            'message': f'Retrieved {len(recent_tickets)} recent tickets'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'data': None,
            'message': 'Failed to retrieve recent tickets',
            'errors': [str(e)]
        }), 500

@dashboard_bp.route('/dashboard/recent-activities', methods=['GET'])
def get_recent_activities():
    """Get recent activities for dashboard"""
    try:
        # Get recent tickets
        recent_tickets = Ticket.query.order_by(Ticket.created_at.desc()).limit(5).all()
        activities = [
            {
                'type': 'ticket_created',
                'description': f'New ticket created: {ticket.title}',
                'timestamp': ticket.created_at.isoformat(),
                'user': (
                    ticket.creator.username if ticket.creator else 'Unknown'
                ),
            }
            for ticket in recent_tickets
        ]
        # Get recently checked out tools
        checked_out_tools = Tool.query.filter(Tool.status == 'in_use').order_by(Tool.checked_out_at.desc()).limit(5).all()
        activities.extend(
            {
                'type': 'tool_checkout',
                'description': f'Tool checked out: {tool.tool_name}',
                'timestamp': tool.checked_out_at.isoformat(),
                'user': (
                    tool.checked_out_user.username
                    if tool.checked_out_user
                    else 'Unknown'
                ),
            }
            for tool in checked_out_tools
            if tool.checked_out_at
        )
        # Sort activities by timestamp
        activities.sort(key=lambda x: x['timestamp'], reverse=True)

        return jsonify({
            'success': True,
            'data': activities[:10],  # Return top 10 activities
            'message': f'Retrieved {len(activities[:10])} recent activities'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'data': None,
            'message': 'Failed to retrieve recent activities',
            'errors': [str(e)]
        }), 500