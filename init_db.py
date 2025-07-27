#!/usr/bin/env python3
"""
Database Initialization Script for Inventory Management Tool

This script creates the database tables required for the application.
Run this script before starting the Flask application for the first time.

Usage:
    python init_db.py
"""

import os
import sys
from flask import Flask
from models import db, User, Product

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize database
    db.init_app(app)
    
    return app

def init_database():
    """Initialize the database with all required tables."""
    app = create_app()
    
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print("✓ Database tables created successfully!")
            
            # Check if tables were created
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"✓ Created tables: {', '.join(tables)}")
            
            return True
            
        except Exception as e:
            print(f"✗ Error creating database tables: {e}")
            return False

def main():
    """Main function to run the database initialization."""
    print("Inventory Management Tool - Database Initialization")
    print("=" * 50)
    
    # Check if database file already exists
    db_path = 'inventory.db'
    if os.path.exists(db_path):
        response = input(f"Database file '{db_path}' already exists. Recreate? (y/N): ")
        if response.lower() not in ['y', 'yes']:
            print("Database initialization cancelled.")
            return
        else:
            # Remove existing database
            os.remove(db_path)
            print(f"✓ Removed existing database file: {db_path}")
    
    # Initialize database
    if init_database():
        print("\n✓ Database initialization completed successfully!")
        print("You can now start the Flask application with: python app.py")
    else:
        print("\n✗ Database initialization failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()