import random
import uuid
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from flask_cors import CORS  # Import CORS for handling cross-origin requests
from db import db  # Import your database connection object

password_routes = Blueprint('password_routes', __name__)
CORS(password_routes, resources={r"/*": {"origins": "*"}})  # Enable CORS for all routes

# -------------------- SEND CODE TO EMAIL --------------------
@password_routes.route('/send-code', methods=['POST'])
def send_code():
    data = request.get_json()
    name_mail = data.get('name_mail')  # Recipient's email address

    if not name_mail:
        return jsonify({'error': 'Campo "name_mail" è obbligatorio'}), 400

    # Check if the user exists in the database
    cursor = db.cursor()
    cursor.execute("SELECT id FROM utenti WHERE name_mail = %s", (name_mail,))
    user = cursor.fetchone()

    if not user:
        return jsonify({'error': 'Utente non trovato'}), 404

    # Generate a unique token and set expiration
    user_id = user[0]
    token_number = uuid.uuid4().hex  # Generate a unique token (UUID)
    expiration_date = datetime.now() + timedelta(minutes=30)

    # Store the token in the database
    cursor.execute(
        "INSERT INTO token (token_number, user_id, expiration_date) VALUES (%s, %s, %s)",
        (token_number, user_id, expiration_date)
    )
    db.commit()

    if cursor.rowcount == 0:
        return jsonify({'error': 'Errore durante la generazione del token'}), 500

    # Send the token via email
    try:
        EMAIL_ADDRESS = "lucafaccio30@gmail.com"  # Update to your Gmail address
        EMAIL_PASSWORD = "D0kj4G04t_"  # Generate and use an App Password for Gmail
        SMTP_SERVER = "smtp.gmail.com"  # Gmail's SMTP server
        SMTP_PORT = 587  # Common port for TLS; use 465 for SSL if required

        import smtplib
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.starttls()  # Start TLS encryption
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            subject = "Codice di Ripristino Password"
            body = f"Il tuo token di ripristino della password è: {token_number}\nValido fino a: {expiration_date.strftime('%Y-%m-%d %H:%M:%S')}"
            msg = f"Subject: {subject}\n\n{body}"

            # Send email to the provided name_mail (email address)
            smtp.sendmail(EMAIL_ADDRESS, name_mail, msg)
    except Exception as e:
        print(f"Errore durante l'invio dell'email: {e}")
        return jsonify({'error': 'Invio email fallito'}), 500

    return jsonify({'message': 'Token inviato con successo'}), 200