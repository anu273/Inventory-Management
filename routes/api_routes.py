"""
API routes for Inventory Management Tool.

This module defines all REST API endpoints with proper error handling,
validation, and response formatting. Routes are organized by functionality.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.auth_service import AuthService
from services.product_service import ProductService

# Create API blueprint
api_bp = Blueprint('api', __name__)


def success_response(data=None, message="Success", status_code=200):
    """Create standardized success response."""
    response = {"success": True, "message": message}
    if data is not None:
        response["data"] = data
    return response, status_code


def error_response(message="An error occurred", status_code=400, errors=None):
    """Create standardized error response."""
    response = {"success": False, "message": message}
    if errors:
        response["errors"] = errors
    return response, status_code


@api_bp.route('/')
def index():
    """API information endpoint."""
    return jsonify({
        "message": "Inventory Management Tool API",
        "version": "1.0.0",
        "endpoints": {
            "register": "POST /register",
            "login": "POST /login", 
            "add_product": "POST /products",
            "update_quantity": "PUT /products/{id}/quantity",
            "get_products": "GET /products"
        }
    }), 200


@api_bp.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    try:
        data = request.get_json()
        
        # Validate input data
        is_valid, errors = AuthService.validate_user_data(data)
        if not is_valid:
            return jsonify({"msg": "; ".join(errors)}), 400
        
        # Register user
        success, message, user = AuthService.register_user(
            username=data['username'],
            password=data['password'],
            email=data.get('email')
        )
        
        if success:
            return jsonify({"msg": message}), 201
        else:
            status_code = 409 if "already exists" in message else 400
            return jsonify({"msg": message}), status_code
            
    except Exception as e:
        return jsonify({"msg": f"Registration failed: {str(e)}"}), 500


@api_bp.route('/login', methods=['POST'])
def login():
    """Authenticate user and return JWT token."""
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({"msg": "Missing username or password"}), 400
        
        # Authenticate user
        success, message, token, user = AuthService.authenticate_user(
            username=data['username'],
            password=data['password']
        )
        
        if success:
            return jsonify(access_token=token), 200
        else:
            return jsonify({"msg": message}), 401
            
    except Exception as e:
        return jsonify({"msg": f"Login failed: {str(e)}"}), 500


@api_bp.route('/products', methods=['POST'])
@jwt_required()
def add_product():
    """Add a new product to inventory."""
    try:
        data = request.get_json()
        current_user_id = int(get_jwt_identity())
        
        # Create product
        success, message, product = ProductService.create_product(
            data=data,
            created_by=current_user_id
        )
        
        if success:
            return jsonify({
                "message": message,
                "product_id": product.id
            }), 201
        else:
            status_code = 409 if "already exists" in message else 400
            return jsonify({"msg": message}), status_code
            
    except Exception as e:
        return jsonify({"msg": f"Product creation failed: {str(e)}"}), 500


@api_bp.route('/products/<int:product_id>/quantity', methods=['PUT'])
@jwt_required()
def update_product_quantity(product_id):
    """Update product quantity."""
    try:
        data = request.get_json()
        
        if 'quantity' not in data:
            return jsonify({"msg": "Quantity is required"}), 400
        
        # Update quantity
        success, message, product = ProductService.update_product_quantity(
            product_id=product_id,
            new_quantity=data['quantity']
        )
        
        if success:
            return jsonify(product.to_dict()), 200
        else:
            status_code = 404 if "not found" in message else 400
            return jsonify({"msg": message}), status_code
            
    except Exception as e:
        return jsonify({"msg": f"Quantity update failed: {str(e)}"}), 500


@api_bp.route('/products', methods=['GET'])
@jwt_required()
def get_products():
    """Get all products."""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search')
        
        # Get products
        products, total, has_next, has_prev = ProductService.get_all_products(
            page=page,
            per_page=per_page,
            search=search
        )
        
        # Convert to dict format
        products_list = [product.to_dict() for product in products]
        
        return jsonify(products_list), 200
            
    except Exception as e:
        return jsonify({"msg": f"Failed to retrieve products: {str(e)}"}), 500
