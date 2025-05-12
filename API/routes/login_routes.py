from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from db import db
from flask_jwt_extended import create_access_token
from datetime import timedelta
from werkzeug.security import check_password_hash

login_routes = Blueprint('login_routes', __name__)

@login_routes.route('/login', methods=['POST'])
@cross_origin(origins="http://127.0.0.1:5000")
def login():
    data = request.json
    email = data.get("name_mail")
    password = data.get("password")

    if not email or not password:
        return jsonify({"status": "fail", "message": "Missing credentials"}), 400

    user = check_user(email, password)

    if user:
        user_id = user['id']  # Accedi tramite la chiave 'id' del dizionario
        access_token = create_access_token(identity=email, additional_claims={"user_id": user_id}, expires_delta=timedelta(hours=1))
        return jsonify({
            "status": "success",
            "message": f"Welcome {email}",
            "access_token": access_token
        }), 200
    else:
        return jsonify({"status": "fail", "message": "Invalid credentials"}), 401

def check_user(name_mail, password):
    cursor = db.cursor()
    cursor.execute("SELECT id, name_mail, password FROM utenti WHERE name_mail=%s", (name_mail,))
    user = cursor.fetchone()
    cursor.close()

    if user:
        # Confronta la password in chiaro
        if user['password'] == password:  # Verifica direttamente la password in chiaro
            return {'id': user['id'], 'name_mail': user['name_mail']}
    return None
