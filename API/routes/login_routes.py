from flask import Blueprint, request, jsonify, make_response
from flask_cors import cross_origin  # Importing cross_origin to handle CORS per route
from db import db
from flask_jwt_extended import create_access_token #download flask_jwt with the command in the CMD (pip install Flask-JWT-Extended)
from datetime import timedelta

login_routes = Blueprint('login_routes', __name__)

@login_routes.route('/login', methods=['POST'])
@cross_origin(origins="http://127.0.0.1:5000")  # Allow CORS only from 127.0.0.1
def login():
    data = request.json
    email = data.get("name_mail")
    password = data.get("password")

    if not email or not password:
        return jsonify({"status": "fail", "message": "Missing credentials"}), 400

    user = check_user(email, password)

    if user:
        access_token = create_access_token(identity=email, expires_delta=timedelta(hours=1))
        return jsonify({
            "status": "success",
            "message": f"Welcome {email}",
            "access_token": access_token
        }), 200
    else:
        return jsonify({"status": "fail", "message": "Invalid credentials"}), 401
    
def check_user(name_mail, password):
    cursor = db.cursor() 
    cursor.execute("SELECT * FROM utenti WHERE name_mail=%s AND password=%s", (name_mail, password))
    user = cursor.fetchone()
    cursor.close()
    return user
