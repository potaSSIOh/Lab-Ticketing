import random
import string
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from flask_cors import CORS
from db import db
import logging
import traceback
import pymysql.cursors  # Use pymysql for database connection and DictCursor

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)

password_routes = Blueprint('password_routes', __name__)
CORS(password_routes, resources={r"/*": {"origins": ["http://localhost", "http://127.0.0.1"]}})

def validate_input(data):
    """Validate the input JSON and return the 'name_mail' field."""
    logging.debug("Validating input data")
    name_mail = data.get('name_mail')
    if not name_mail:
        logging.error("Missing 'name_mail' field in the request data")
        raise ValueError('Campo "name_mail" è obbligatorio')
    logging.debug(f"Validated 'name_mail': {name_mail}")
    return name_mail

def check_user_existence(name_mail):
    """Check if the user exists in the database and return the user ID."""
    logging.debug(f"Checking existence of user with name_mail: {name_mail}")
    # Use DictCursor to fetch results as dictionaries
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        cursor.execute("SELECT id FROM utenti WHERE name_mail = %s", (name_mail,))
        user = cursor.fetchone()
        logging.debug(f"Query result for user: {user}")
    except Exception as db_error:
        logging.error(f"Database error when fetching user: {str(db_error)}")
        traceback.print_exc()
        raise RuntimeError("Errore nel database")
    
    if not user:
        logging.error(f"No user found with email: {name_mail}")
        raise ValueError("Utente non trovato")
    
    return user['id']  # Access the 'id' field as a dictionary key

def generate_random_token(length=12):
    """Generate a random alphanumeric token."""
    logging.debug(f"Generating random token with length={length}")
    characters = string.ascii_letters + string.digits
    token = ''.join(random.choices(characters, k=length))
    logging.debug(f"Generated token: {token}")
    print(f"Generated token (for debugging): {token}")  # Print token for debugging
    return token

def insert_token_into_db(token_number, user_id, expiration_date):
    """Insert the token into the database."""
    logging.debug("Inserting token into the database")
    cursor = db.cursor()
    try:
        cursor.execute(
            "INSERT INTO token (token_number, user_id, expiration_date) VALUES (%s, %s, %s)",
            (token_number, user_id, expiration_date)
        )
        db.commit()
        logging.info("Token inserted into the database successfully.")
    except Exception as commit_error:
        logging.error(f"Error during database insertion or commit: {str(commit_error)}")
        traceback.print_exc()
        raise RuntimeError("Errore durante la generazione del token")

def send_email_with_token(email, token_number, expiration_date):
    """Send the generated token to the user via email."""
    logging.debug("Sending email with the token")
    EMAIL_ADDRESS = "labticketingprova@gmail.com"  # Replace with your email
    EMAIL_PASSWORD = "mouy jkpk lybi xfyz"  # Replace with your app password --> mouy jkpk lybi xfyz

    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587

    try:
        import smtplib
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            subject = "Codice di Ripristino Password"
            body = (f"Il tuo token di ripristino della password è: {token_number}\n"
                    f"Valido fino a: {expiration_date.strftime('%Y-%m-%d %H:%M:%S')}")
            msg = f"Subject: {subject}\n\n{body}"
            smtp.sendmail(EMAIL_ADDRESS, email, msg)
            logging.info("Email sent successfully.")
    except Exception as email_error:
        logging.error(f"Error during email sending: {str(email_error)}")
        traceback.print_exc()
        raise RuntimeError("Invio email fallito")

@password_routes.route('/send-code', methods=['POST'])
def send_code():
    try:
        # Step 1: Parse and validate the input
        data = request.get_json()
        name_mail = validate_input(data)

        # Step 2: Check if the user exists
        user_id = check_user_existence(name_mail)

        # Step 3: Generate a random token and expiration date
        try:
            token_number = generate_random_token()
            expiration_date = datetime.now() + timedelta(minutes=30)
            logging.debug(f"Expiration date calculated: {expiration_date.strftime('%Y-%m-%d %H:%M:%S')}")
        except Exception as token_error:
            logging.error(f"Error during token generation or expiration date calculation: {str(token_error)}")
            logging.debug(f"Generated token before the error (if any): {locals().get('token_number', None)}")
            traceback.print_exc()
            return jsonify({'error': 'Errore durante la generazione del token', 'generated_token': locals().get('token_number')}), 500

        # Step 4: Insert the token into the database
        insert_token_into_db(token_number, user_id, expiration_date)

        # Step 5: Send the token via email
        send_email_with_token(name_mail, token_number, expiration_date)

        # Step 6: Return success response
        logging.debug("Returning success response to the client")
        return jsonify({'message': 'Token inviato con successo'}), 200

    except ValueError as ve:
        logging.error(f"Validation error: {str(ve)}")
        return jsonify({'error': str(ve)}), 400
    except RuntimeError as re:
        logging.error(f"Runtime error: {str(re)}")
        return jsonify({'error': str(re)}), 500
    except Exception as general_error:
        logging.error(f"An unexpected error occurred: {str(general_error)}")
        traceback.print_exc()
        return jsonify({'error': 'An internal server error occurred'}), 500