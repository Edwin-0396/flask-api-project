from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from models import db, User

def setup_routes(app):
    # Ruta para registrar usuarios
    @app.route('/register', methods=['POST'])
    def register():
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({"error": "Username and password required"}), 400
        
        if User.query.filter_by(username=username).first():
            return jsonify({"error": "Username already exists"}), 409
        
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({"message": "User created successfully"}), 201

    # Ruta para login de usuarios
    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if not user or not user.check_password(password):
            return jsonify({"error": "Invalid username or password"}), 401
        
        access_token = create_access_token(identity=username)
        return jsonify({"access_token": access_token}), 200
