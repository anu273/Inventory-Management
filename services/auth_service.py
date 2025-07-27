"""
Authentication service for Inventory Management Tool.

This module handles user authentication, registration, and JWT token management.
It provides a clean interface for auth-related operations.
"""

from flask_jwt_extended import create_access_token, get_jwt_identity
from models import User, db


class AuthService:
    """Service class for authentication operations."""
    
    @staticmethod
    def register_user(username, password, email=None):
        """Register a new user."""
        try:
            # Check if user already exists
            if User.find_by_username(username):
                return False, "User already exists", None
            
            # Create new user
            user = User(username=username, password=password, email=email)
            user.save()
            
            return True, "User created successfully", user
            
        except Exception as e:
            return False, f"Registration failed: {str(e)}", None
    
    @staticmethod
    def authenticate_user(username, password):
        """Authenticate user credentials."""
        try:
            # Find user by username
            user = User.find_by_username(username)
            
            if not user:
                return False, "User not found", None, None
            
            if not user.is_active:
                return False, "User account is deactivated", None, None
            
            # Check password
            if not user.check_password(password):
                return False, "Invalid password", None, None
            
            # Create JWT token
            access_token = create_access_token(identity=str(user.id))
            
            return True, "Login successful", access_token, user
            
        except Exception as e:
            return False, f"Authentication failed: {str(e)}", None, None
    
    @staticmethod
    def get_current_user():
        """Get current authenticated user from JWT token."""
        try:
            user_id = get_jwt_identity()
            if user_id:
                return User.find_by_id(int(user_id))
            return None
        except Exception:
            return None
    
    @staticmethod
    def validate_user_data(data):
        """Validate user registration/login data."""
        errors = []
        
        if not data:
            return False, ["No data provided"]
        
        # Check required fields
        if not data.get('username'):
            errors.append("Username is required")
        elif len(data['username']) < 3:
            errors.append("Username must be at least 3 characters long")
        
        if not data.get('password'):
            errors.append("Password is required")
        elif len(data['password']) < 6:
            errors.append("Password must be at least 6 characters long")
        
        # Validate email if provided
        email = data.get('email')
        if email and '@' not in email:
            errors.append("Invalid email format")
        
        return len(errors) == 0, errors
