"""
Database models for Inventory Management Tool.

This module defines the database schema using SQLAlchemy ORM,
including User and Product models with proper relationships and constraints.
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize SQLAlchemy instance
db = SQLAlchemy()


class BaseModel(db.Model):
    """
    Abstract base model with common fields and methods.
    
    Provides common functionality like timestamps and serialization
    that can be inherited by other models.
    """
    
    __abstract__ = True
    
    # Common fields
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def save(self):
        """Save the current instance to database."""
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
    
    def delete(self):
        """Delete the current instance from database."""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
    
    def to_dict(self):
        """Convert model instance to dictionary."""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }


class User(BaseModel):
    """
    User model for authentication and authorization.
    
    Handles user registration, authentication, and profile management.
    Each user can manage products in the inventory system.
    """
    
    __tablename__ = 'users'
    
    # User fields
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Relationships
    products = db.relationship('Product', backref='created_by_user', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, username, password, email=None):
        """Initialize User instance."""
        self.username = username
        self.set_password(password)
        self.email = email
    
    def set_password(self, password):
        """Set user password (hashed)."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches stored hash."""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert User to dictionary (excluding sensitive data)."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'total_products': len(self.products)
        }
    
    @classmethod
    def find_by_username(cls, username):
        """Find user by username."""
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def find_by_id(cls, user_id):
        """Find user by ID."""
        return cls.query.get(user_id)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Product(BaseModel):
    """
    Product model for inventory management.
    
    Represents items in the inventory with details like name, SKU,
    quantity, price, and other product information.
    """
    
    __tablename__ = 'products'
    
    # Product fields
    name = db.Column(db.String(120), nullable=False, index=True)
    type = db.Column(db.String(80), nullable=True, index=True)
    sku = db.Column(db.String(80), unique=True, nullable=False, index=True)
    image_url = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    price = db.Column(db.Float, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Foreign key to User
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    def __init__(self, name, sku, quantity, price, **kwargs):
        """Initialize Product instance."""
        self.name = name
        self.sku = sku
        self.quantity = quantity
        self.price = price
        
        # Optional fields
        self.type = kwargs.get('type')
        self.image_url = kwargs.get('image_url')
        self.description = kwargs.get('description')
        self.created_by = kwargs.get('created_by')
    
    def update_quantity(self, new_quantity):
        """Update product quantity."""
        if new_quantity < 0:
            raise ValueError("Quantity cannot be negative")
        
        self.quantity = new_quantity
        return self.save()
    
    def is_in_stock(self):
        """Check if product is in stock."""
        return self.quantity > 0
    
    def to_dict(self):
        """Convert Product to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'sku': self.sku,
            'image_url': self.image_url,
            'description': self.description,
            'quantity': self.quantity,
            'price': self.price,
            'is_active': self.is_active,
            'in_stock': self.is_in_stock(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'created_by': self.created_by
        }
    
    @classmethod
    def find_by_sku(cls, sku):
        """Find product by SKU."""
        return cls.query.filter_by(sku=sku, is_active=True).first()
    
    @classmethod
    def get_all_active(cls, page=1, per_page=10):
        """Get all active products with pagination."""
        return cls.query.filter_by(is_active=True).paginate(
            page=page, per_page=per_page, error_out=False
        )
    
    @classmethod
    def search_by_name(cls, search_term):
        """Search products by name."""
        return cls.query.filter(
            cls.name.contains(search_term),
            cls.is_active == True
        ).all()
    
    def __repr__(self):
        return f'<Product {self.name} ({self.sku})>'