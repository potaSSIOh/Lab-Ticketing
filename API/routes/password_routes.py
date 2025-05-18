from flask import Blueprint, request, jsonify, make_response
from db import get_db_connection
import random
import string
from datetime import datetime, timedelta
from email.message import EmailMessage
import pymysql.cursors

password_routes = Blueprint('password_routes', __name__)

#-----------------------------------------------------

def validate_input(data):
    """Validate the input JSON and return the 'name_mail' field."""
    name_mail = data.get('name_mail')
    if not name_mail:
        raise ValueError('Campo "name_mail" è obbligatorio')
    return name_mail

#-----------------------------------------------------

def check_user_existence(name_mail):
    """Check if the user exists in the database and return the user ID."""
    conn = get_db_connection()
    
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("SELECT id FROM utenti WHERE name_mail = %s", (name_mail,))
    user = cursor.fetchone()

    if not user:
        raise ValueError("Utente non trovato")
    
    return user['id']

#-----------------------------------------------------

def generate_random_token(length=12):
    """Generate a random alphanumeric token."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

#-----------------------------------------------------

def insert_token_into_db(token_number, user_id, expiration_date):
    """Insert the token into the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO token (token_number, user_id, expiration_date) VALUES (%s, %s, %s)",
        (token_number, user_id, expiration_date)
    )
    conn.commit()

    if cursor.rowcount == 0:
        raise RuntimeError("Errore durante la generazione del token")

#-----------------------------------------------------

def send_email_with_token(email, token_number, expiration_date):
    """Send the generated token to the user via email."""
    EMAIL_ADDRESS = "labticketingprova@gmail.com"
    EMAIL_PASSWORD = "mouy jkpk lybi xfyz"
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587

    msg = EmailMessage()
    msg['Subject'] = "Codice di Ripristino Password"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = email
    msg.set_content(
        f"Il tuo token di ripristino della password è: {token_number}\n"
        f"Valido fino a: {expiration_date.strftime('%Y-%m-%d %H:%M:%S')}"
    )

    import smtplib
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

#-----------------------------------------------------

@password_routes.route('/send-code', methods=['POST'])
def send_code():
    data = request.get_json()
    try:
        name_mail = validate_input(data)
        user_id = check_user_existence(name_mail)
        token_number = generate_random_token()
        expiration_date = datetime.now() + timedelta(minutes=30)

        insert_token_into_db(token_number, user_id, expiration_date)
        send_email_with_token(name_mail, token_number, expiration_date)

        return jsonify({'message': 'Token inviato con successo'}), 200
    except ValueError as e:
        return make_response(jsonify({"Error": str(e)}), 400)
    except RuntimeError as e:
        return make_response(jsonify({"Error": str(e)}), 500)
    except Exception:
        return make_response(jsonify({"Error": "Si è verificato un errore interno"}), 500)

#-----------------------------------------------------

@password_routes.route('/update-password', methods=['PATCH'])
def change_password():
    data = request.get_json()
    try:
        token_number = data.get("token_number")
        new_password = data.get("new_password")

        if not token_number or not new_password:
            return make_response(jsonify({"Error": "Token e nuova password sono obbligatori"}), 400)

        conn = get_db_connection()

        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT user_id, expiration_date FROM token WHERE token_number = %s",
            (token_number,)
        )
        token_data = cursor.fetchone()

        if not token_data:
            return make_response(jsonify({"Error": "Token non valido"}), 404)

        expiration_date = token_data["expiration_date"]
        if datetime.now() > expiration_date:
            return make_response(jsonify({"Error": "Token scaduto"}), 400)

        user_id = token_data["user_id"]
        cursor.execute(
            "UPDATE utenti SET password = %s WHERE id = %s",
            (new_password, user_id)
        )
        conn.commit()

        if cursor.rowcount == 0:
            return make_response(jsonify({"Error": "Errore durante l'aggiornamento della password"}), 403)

        return jsonify({"Status": "Password aggiornata con successo"}), 200
    except Exception:
        return make_response(jsonify({"Error": "Si è verificato un errore interno"}), 500)