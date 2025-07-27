"""
Configuration module for Inventory Management Tool.

This module handles all configuration settings for different environments
including database connections, JWT settings, and application secrets.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Base configuration class with common settings."""
    
    # Flask Core Settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-flask-secret-key-fallback')
    
    # Database Settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT Settings
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'dev-jwt-secret-key-fallback')
    JWT_ALGORITHM = 'HS256'
    JWT_DECODE_LEEWAY = 10
    JWT_ACCESS_TOKEN_EXPIRES = False  # No expiration for development


class DevelopmentConfig(Config):
    """Development environment configuration."""
    
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///inventory_dev.db'


class ProductionConfig(Config):
    """Production environment configuration."""
    
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///inventory_prod.db')
    
    # Override with secure defaults for production
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour token expiration


class TestingConfig(Config):
    """Testing environment configuration."""
    
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # In-memory database for tests


# Configuration mapping
config_mapping = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(environment=None):
    """
    Get configuration based on environment.
    
    Args:
        environment (str): Environment name ('development', 'production', 'testing')
        
    Returns:
        Config: Configuration class for the specified environment
    """
    if environment is None:
        environment = os.environ.get('FLASK_ENV', 'default')
    
    return config_mapping.get(environment, DevelopmentConfig)