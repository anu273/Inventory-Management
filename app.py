# app.py

import os
from flask import send_from_directory
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from models import db, User, Product

# Load environment variables from .env file
load_dotenv()

# --- App Initialization ---
app = Flask(__name__)

# --- Configuration ---
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-super-secret-key-for-dev')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'default-jwt-secret-key-for-dev')
app.config['JWT_ALGORITHM'] = 'HS256'
app.config['JWT_DECODE_LEEWAY'] = 10

# --- Extensions Initialization ---
db.init_app(app)
jwt = JWTManager(app)
CORS(app)  # Enable CORS for frontend integration

# --- JWT Error Handlers ---
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"msg": "Token has expired"}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({"msg": "Invalid token"}), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({"msg": "Authorization token is required"}), 401

# --- CLI Commands ---
@app.cli.command("init-db")
def init_db_command():
    """Creates the database tables."""
    with app.app_context():
        db.create_all()
        print("Initialized the database.")

@app.cli.command("reset-db")
def reset_db_command():
    """Drops and recreates the database tables."""
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("Reset the database.")

# --- Helper Functions ---
def product_to_dict(product):
    """Serializes a Product object to a dictionary."""
    return {
        "id": product.id,
        "name": product.name,
        "type": product.type,
        "sku": product.sku,
        "image_url": product.image_url,
        "description": product.description,
        "quantity": product.quantity,
        "price": product.price,
        "is_active": product.is_active,
        "in_stock": product.is_in_stock(),
        "created_at": product.created_at.isoformat() if product.created_at else None,
        "updated_at": product.updated_at.isoformat() if product.updated_at else None,
        "created_by": product.created_by
    }

def user_to_dict(user):
    """Serializes a User object to a dictionary (excluding sensitive data)."""
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_active": user.is_active,
        "created_at": user.created_at.isoformat() if user.created_at else None,
        "updated_at": user.updated_at.isoformat() if user.updated_at else None,
        "total_products": len(user.products)
    }

# --- API Endpoints ---

## Root endpoint
@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')


## User Management
@app.route('/register', methods=['POST'])
def register():
    """Registers a new user."""
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"msg": "Missing username or password"}), 400

    # Check if username already exists
    if User.find_by_username(data['username']):
        return jsonify({"msg": "User already exists"}), 409  # Conflict

    # Check if email already exists (if provided)
    email = data.get('email')
    if email and User.query.filter_by(email=email).first():
        return jsonify({"msg": "Email already registered"}), 409

    try:
        # Create new user using the model's constructor
        new_user = User(
            username=data['username'], 
            password=data['password'],
            email=email
        )
        new_user.save()

        return jsonify({
            "msg": "User created successfully",
            "user": user_to_dict(new_user)
        }), 201

    except Exception as e:
        return jsonify({"msg": f"Error creating user: {str(e)}"}), 500

@app.route('/login', methods=['POST'])
def login():
    """Logs in a user and returns a JWT."""
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"msg": "Missing username or password"}), 400

    user = User.find_by_username(data['username'])

    if user and user.check_password(data['password']):
        if not user.is_active:
            return jsonify({"msg": "Account is deactivated"}), 403
            
        access_token = create_access_token(identity=str(user.id))
        return jsonify({
            "access_token": access_token,
            "user": user_to_dict(user)
        }), 200
    
    return jsonify({"msg": "Bad username or password"}), 401

@app.route('/profile', methods=['GET'])
@jwt_required()
def get_user_profile():
    """Get current user's profile."""
    current_user_id = get_jwt_identity()
    user = User.find_by_id(int(current_user_id))
    
    if not user:
        return jsonify({"msg": "User not found"}), 404
    
    return jsonify(user_to_dict(user)), 200

@app.route('/profile', methods=['PUT'])
@jwt_required()
def update_user_profile():
    """Update current user's profile."""
    current_user_id = get_jwt_identity()
    user = User.find_by_id(int(current_user_id))
    
    if not user:
        return jsonify({"msg": "User not found"}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({"msg": "No data provided"}), 400
    
    try:
        # Update email if provided
        if 'email' in data:
            new_email = data['email']
            if new_email and new_email != user.email:
                # Check if email is already taken
                existing_user = User.query.filter_by(email=new_email).first()
                if existing_user and existing_user.id != user.id:
                    return jsonify({"msg": "Email already registered"}), 409
                user.email = new_email
        
        # Update password if provided
        if 'password' in data and data['password']:
            user.set_password(data['password'])
        
        user.save()
        return jsonify({
            "msg": "Profile updated successfully",
            "user": user_to_dict(user)
        }), 200
        
    except Exception as e:
        return jsonify({"msg": f"Error updating profile: {str(e)}"}), 500

## Product Management
@app.route('/products', methods=['POST'])
@jwt_required()
def add_product():
    """Adds a new product to the inventory."""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    required_fields = ["name", "sku", "quantity", "price"]
    if not all(field in data for field in required_fields):
        return jsonify({"msg": "Missing required product fields"}), 400

    if Product.find_by_sku(data['sku']):
        return jsonify({"msg": f"Product with SKU {data['sku']} already exists"}), 409

    try:
        new_product = Product(
            name=data['name'],
            sku=data['sku'],
            quantity=data['quantity'],
            price=data['price'],
            type=data.get('type'),
            image_url=data.get('image_url'),
            description=data.get('description'),
            created_by=int(current_user_id)
        )
        new_product.save()

        return jsonify({
            "message": "Product added successfully", 
            "product_id": new_product.id
        }), 201
        
    except Exception as e:
        return jsonify({"msg": f"Error adding product: {str(e)}"}), 500

@app.route('/products/<int:id>', methods=['PUT'])
@jwt_required()
def update_product(id):
    """Updates a product."""
    product = Product.query.get_or_404(id)
    data = request.get_json()
    
    if not data:
        return jsonify({"msg": "No data provided"}), 400
    
    try:
        # Update allowed fields
        if 'name' in data:
            product.name = data['name']
        if 'type' in data:
            product.type = data['type']
        if 'description' in data:
            product.description = data['description']
        if 'image_url' in data:
            product.image_url = data['image_url']
        if 'price' in data:
            product.price = data['price']
        if 'quantity' in data:
            product.update_quantity(data['quantity'])
        
        product.save()
        return jsonify(product_to_dict(product)), 200
        
    except ValueError as e:
        return jsonify({"msg": str(e)}), 400
    except Exception as e:
        return jsonify({"msg": f"Error updating product: {str(e)}"}), 500

@app.route('/products/<int:id>/quantity', methods=['PUT'])
@jwt_required()
def update_product_quantity(id):
    """Updates the quantity of a specific product."""
    product = Product.query.get_or_404(id)
    data = request.get_json()

    if 'quantity' not in data or not isinstance(data['quantity'], int):
        return jsonify({"msg": "Invalid or missing quantity"}), 400
    
    try:
        product.update_quantity(data['quantity'])
        return jsonify(product_to_dict(product)), 200
    except ValueError as e:
        return jsonify({"msg": str(e)}), 400
    except Exception as e:
        return jsonify({"msg": f"Error updating quantity: {str(e)}"}), 500

@app.route('/products', methods=['GET'])
@jwt_required()
def get_products():
    """Gets a list of products with optional filtering and search."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('search', '', type=str)
    
    try:
        if search:
            # Search by name
            products = Product.search_by_name(search)
            products_list = [product_to_dict(p) for p in products]
        else:
            # Get all active products
            all_products = Product.query.filter_by(is_active=True).all()
            products_list = [product_to_dict(p) for p in all_products]

        return jsonify(products_list), 200
        
    except Exception as e:
        return jsonify({"msg": f"Error fetching products: {str(e)}"}), 500

@app.route('/products/<int:id>', methods=['GET'])
@jwt_required()
def get_product(id):
    """Get a specific product by ID."""
    product = Product.query.get_or_404(id)
    return jsonify(product_to_dict(product)), 200

@app.route('/products/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_product(id):
    """Soft delete a product (mark as inactive)."""
    product = Product.query.get_or_404(id)
    
    try:
        product.is_active = False
        product.save()
        return jsonify({"msg": "Product deleted successfully"}), 200
    except Exception as e:
        return jsonify({"msg": f"Error deleting product: {str(e)}"}), 500

# --- Error Handlers ---
@app.errorhandler(404)
def not_found(error):
    return jsonify({"msg": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({"msg": "Internal server error"}), 500

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"msg": "Bad request"}), 400

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)

