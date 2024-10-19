from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from models import db, User

def setup_routes(app):
    # Root route
    @app.route('/')
    def index():
        return "Welcome to the Flask API"

    # Route for user registration
    @app.route('/register', methods=['POST'])
    def register():
        # Get the data from the request
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        # Ensure that username and password are provided
        if not username or not password:
            return jsonify({"error": "Username and password required"}), 400
        
        # Check if the user already exists
        if User.query.filter_by(username=username).first():
            return jsonify({"error": "Username already exists"}), 409
        
        # Create a new user, set the password, and save to the database
        new_user = User(username=username)
        new_user.set_password(password)  # Make sure this method is defined in the User model
        db.session.add(new_user)
        db.session.commit()
        
        # Return a success message
        return jsonify({"message": "User created successfully"}), 201

    # Route for user login
    @app.route('/login', methods=['POST'])
    def login():
        # Get the data from the request
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        # Find the user in the database
        user = User.query.filter_by(username=username).first()
        
        # Check if the user exists and if the password is correct
        if not user or not user.check_password(password):
            return jsonify({"error": "Invalid username or password"}), 401
        
        # Generate access token for the user
        access_token = create_access_token(identity=username)
        
        # Return the access token
        return jsonify({"access_token": access_token}), 200
