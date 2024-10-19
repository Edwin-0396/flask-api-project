from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from models import db, User, Item  # Import models

def setup_routes(app):

    # User registration route
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

    # User login route
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

    # Protected route example
    @app.route('/protected', methods=['GET'])
    @jwt_required()
    def protected():
        return jsonify({"message": "This is a protected route"}), 200

    # CRUD operations for items

    # Create an item
    @app.route('/items', methods=['POST'])
    @jwt_required()
    def create_item():
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')

        if not name or len(name) < 3:
            return jsonify({"error": "Name must be at least 3 characters"}), 400

        new_item = Item(name=name, description=description)
        db.session.add(new_item)
        db.session.commit()

        return jsonify({"message": "Item created", "item": {"name": name, "description": description}}), 201

    # Read all items
    @app.route('/items', methods=['GET'])
    @jwt_required()
    def get_items():
        items = Item.query.all()
        return jsonify([{"id": item.id, "name": item.name, "description": item.description} for item in items]), 200

    # Update an item
    @app.route('/items/<int:item_id>', methods=['PUT'])
    @jwt_required()
    def update_item(item_id):
        data = request.get_json()
        item = Item.query.get_or_404(item_id)

        item.name = data.get('name', item.name)
        item.description = data.get('description', item.description)
        db.session.commit()

        return jsonify({"message": "Item updated", "item": {"name": item.name, "description": item.description}}), 200

    # Delete an item
    @app.route('/items/<int:item_id>', methods=['DELETE'])
    @jwt_required()
    def delete_item(item_id):
        item = Item.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()

        return jsonify({"message": "Item deleted"}), 200
