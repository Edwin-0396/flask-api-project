import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecretkey')  # Use a secure secret key
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'  # SQLite for local development, switch to PostgreSQL in production
    SQLALCHEMY_TRACK_MODIFICATIONS = False
