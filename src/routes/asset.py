from flask import Blueprint, jsonify, request
from src.models.asset import Asset, db
from datetime import datetime

asset_bp = Blueprint('asset', __name__)

@asset_bp.route('/assets', methods=['GET'])
def get_assets():
    """Get all assets with optional filtering"""
    category = request.args.get('category')
    condition = request.args.get('condition')
    location = request.args.get('location')
    
    query = Asset.query
    
    if category:
        query = query.filter(Asset.category == category)
    if condition:
        query = query.filter(Asset.condition == condition)
    if location:
        query = query.filter(Asset.location == location)
    
    assets = query.order_by(Asset.created_at.desc()).all()
    return jsonify({
        'success': True,
        'data': [asset.to_dict() for asset in assets],
        'message': f'Retrieved {len(assets)} assets'
    })

@asset_bp.route('/assets', methods=['POST'])
def create_asset():
    """Create a new asset"""
    try:
        data = request.json
        
        asset = Asset(
            asset_tag=data['asset_tag'],
            name=data['name'],
            description=data.get('description'),
            category=data.get('category'),
            location=data.get('location'),
            condition=data.get('condition', 'good'),
            purchase_date=datetime.strptime(data['purchase_date'], '%Y-%m-%d').date() if data.get('purchase_date') else None,
            warranty_expiry=datetime.strptime(data['warranty_expiry'], '%Y-%m-%d').date() if data.get('warranty_expiry') else None,
            assigned_to=data.get('assigned_to')
        )
        
        db.session.add(asset)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': asset.to_dict(),
            'message': 'Asset created successfully'
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'data': None,
            'message': 'Failed to create asset',
            'errors': [str(e)]
        }), 400

@asset_bp.route('/assets/<int:asset_id>', methods=['GET'])
def get_asset(asset_id):
    """Get a specific asset by ID"""
    asset = Asset.query.get_or_404(asset_id)
    return jsonify({
        'success': True,
        'data': asset.to_dict(),
        'message': 'Asset retrieved successfully'
    })

@asset_bp.route('/assets/<int:asset_id>', methods=['PUT'])
def update_asset(asset_id):
    """Update an asset"""
    try:
        asset = Asset.query.get_or_404(asset_id)
        data = request.json
        
        asset.asset_tag = data.get('asset_tag', asset.asset_tag)
        asset.name = data.get('name', asset.name)
        asset.description = data.get('description', asset.description)
        asset.category = data.get('category', asset.category)
        asset.location = data.get('location', asset.location)
        asset.condition = data.get('condition', asset.condition)
        asset.assigned_to = data.get('assigned_to', asset.assigned_to)
        asset.updated_at = datetime.utcnow()
        
        if data.get('purchase_date'):
            asset.purchase_date = datetime.strptime(data['purchase_date'], '%Y-%m-%d').date()
        if data.get('warranty_expiry'):
            asset.warranty_expiry = datetime.strptime(data['warranty_expiry'], '%Y-%m-%d').date()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': asset.to_dict(),
            'message': 'Asset updated successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'data': None,
            'message': 'Failed to update asset',
            'errors': [str(e)]
        }), 400

@asset_bp.route('/assets/<int:asset_id>', methods=['DELETE'])
def delete_asset(asset_id):
    """Delete an asset"""
    try:
        asset = Asset.query.get_or_404(asset_id)
        db.session.delete(asset)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': None,
            'message': 'Asset deleted successfully'
        }), 204
        
    except Exception as e:
        return jsonify({
            'success': False,
            'data': None,
            'message': 'Failed to delete asset',
            'errors': [str(e)]
        }), 400

@asset_bp.route('/assets/scan/<string:barcode>', methods=['GET'])
def scan_asset(barcode):
    """Get asset by barcode/asset tag"""
    asset = Asset.query.filter_by(asset_tag=barcode).first()
    
    if not asset:
        return jsonify({
            'success': False,
            'data': None,
            'message': 'Asset not found',
            'errors': ['No asset found with this barcode']
        }), 404
    
    return jsonify({
        'success': True,
        'data': asset.to_dict(),
        'message': 'Asset found successfully'
    })

