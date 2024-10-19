from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from routes import setup_routes  # Import your routes setup function
from config import Config  # Import configuration
from models import db  # Import the database (initialized in models.py)

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)  # Initialize SQLAlchemy
jwt = JWTManager(app)  # Initialize JWT manager
migrate = Migrate(app, db)  # Initialize Flask-Migrate

# Set up routes
setup_routes(app)

# Error Handlers
@app.errorhandler(404)
def not_found(error):
    return {"error": "Resource not found"}, 404

@app.errorhandler(500)
def internal_server_error(error):
    return {"error": "An internal error occurred"}, 500

# Start the application
if __name__ == '__main__':
    app.run(debug=True)
