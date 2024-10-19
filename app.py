from flask import Flask
from flask_jwt_extended import JWTManager
from models import db  # Your database instance
from routes import setup_routes
from config import Config
from flask_migrate import Migrate  # Add Flask-Migrate

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
jwt = JWTManager(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)  # Add this line to set up migration support

# Set up routes
setup_routes(app)

# Run the application
if __name__ == '__main__':
    app.run()
