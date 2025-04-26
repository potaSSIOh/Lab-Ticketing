from flask import Blueprint, request, jsonify, make_response

from db import db

utenti_routes = Blueprint('utenti_routes', __name__)

#-----------------------------------------------------

@utenti_routes.route('/utenti', methods=['GET'])
def get_utenti():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM utenti")
    return jsonify(cursor.fetchall()), 200

#-----------------------------------------------------

@utenti_routes.route('/utenti', methods=['POST'])
def add_utente():
    data = request.get_json()
    try:
        name_mail = data["name_mail"]
        password = data["password"]
        autorizzato = data["autorizzato"]
    except KeyError as e:
        return make_response(jsonify({"Error": f"Campo mancante: {str(e)}"}), 400)

    cursor = db.cursor()
    cursor.execute("INSERT INTO utenti (name_mail, password, autorizzato) VALUES (%s, %s, %s)",
                   (name_mail, password, autorizzato))
    db.commit()

    if cursor.rowcount == 0:
        return make_response(jsonify({"Error": "risorsa non inserita"}), 403)

    res = make_response(jsonify({"Status": "OK"}), 201)
    res.headers.add("location", f"/utenti/{cursor.lastrowid}")
    return res

#-----------------------------------------------------

@utenti_routes.route('/utenti/<int:id>', methods=['PATCH'])
def update_password(id):
    data = request.get_json()
    try:
        password = data["password"]
    except KeyError:
        return make_response(jsonify({"Error": "Campo 'password' mancante"}), 400)

    cursor = db.cursor()
    cursor.execute("UPDATE utenti SET password = %s WHERE id = %s", (password, id))
    db.commit()

    if cursor.rowcount == 0:
        return make_response(jsonify({"Error": "Utente non trovato o password non modificata"}), 404)

    return make_response(jsonify({"Status": "Password aggiornata"}), 200)
