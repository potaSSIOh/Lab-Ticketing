from flask import Blueprint, request, jsonify, make_response
from db import get_db_connection

ticketp_routes = Blueprint('ticketp_routes', __name__)


@ticketp_routes.route('/ticketp', methods=['GET'])
@ticketp_routes.route('/ticketp/<string:hostnameP>', methods=['GET'])
def get_hostnameP(hostnameP=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if hostnameP:
        cursor.execute("SELECT * FROM ticketp WHERE hostnameP = %s", (hostnameP,))
    else:
        cursor.execute("SELECT * FROM ticketP")
    results = cursor.fetchall()

    if not results:
        return jsonify({"Error": "risorsa non trovata"}), 404
    return jsonify(results), 200

#-----------------------------------------------------

@ticketp_routes.route('/ticketp', methods=['POST'])
def add_ticketp():
    data = request.get_json()
    try:
        descrizione = data["descrizione"]
        dataOra = data["dataOra"]
        creatore = data["creatore"]
        hostnameP = data.get("hostnameP")
        tecnico = data.get("tecnico")
        stato = data["stato"]
    except KeyError as e:
        return make_response(jsonify({"Error": f"Campo mancante: {str(e)}"}), 400)

    conn = get_db_connection()
    cursor = conn.cursor()
    sql = """INSERT INTO ticketp (descrizione, dataOra, creatore, hostnameP, tecnico, stato)
             VALUES (%s, %s, %s, %s, %s, %s)"""
    cursor.execute(sql, (descrizione, dataOra, creatore, hostnameP, tecnico, stato))
    conn.commit()

    if cursor.rowcount == 0:
        return make_response(jsonify({"Error": "risorsa non inserita"}), 403)

    res = make_response(jsonify({"Status": "OK"}), 201)
    res.headers.add("location", f"/ticketp/{cursor.lastrowid}")
    return res

#-----------------------------------------------------

@ticketp_routes.route('/ticketp/<int:id>', methods=['PATCH'])
def update_descrizione(id):
    data = request.get_json()
    try:
        descrizione = data["descrizione"]
    except KeyError:
        return make_response(jsonify({"Error": "Campo 'descrizione' mancante"}), 400)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE ticketp SET descrizione = %s WHERE id = %s", (descrizione, id))
    conn.commit()

    if cursor.rowcount == 0:
        return make_response(jsonify({"Error": "Ticket non trovato o descrizione non modificata"}), 404)

    return make_response(jsonify({"Status": "Descrizione aggiornata"}), 200)

@ticketp_routes.route('/ticketp/<int:id>/tecnico', methods=['PATCH'])
def update_tecnico(id):
    data = request.get_json()

    if "tecnico" not in data:
        return make_response(jsonify({"Error": "Campo 'tecnico' mancante"}), 400)

    tecnico_email = data["tecnico"]

    # Verifica che il tecnico esista ed è autorizzato
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM utenti WHERE name_mail = %s AND autorizzato = 1", (tecnico_email,))
    tecnico = cursor.fetchone()

    if not tecnico:
        return make_response(jsonify({"Error": "Tecnico non valido o non autorizzato"}), 400)

    # Aggiorna il tecnico nel ticket
    cursor.execute("UPDATE ticketp SET tecnico = %s WHERE IdTicket = %s", (tecnico_email, id))
    conn.commit()

    if cursor.rowcount == 0:
        return make_response(jsonify({"Error": "Ticket non trovato o tecnico non modificato"}), 404)

    return make_response(jsonify({"Status": "Tecnico aggiornato con successo"}), 200)

@ticketp_routes.route('/ticketp/<int:id>/stato', methods=['PATCH'])
def update_stato(id):
    data = request.get_json()
    try:
        stato = data["stato"]
    except KeyError:
        return make_response(jsonify({"Error": "Campo 'stato' mancante"}), 400)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE ticketp SET stato = %s WHERE IdTicket = %s", (stato, id))
    conn.commit()

    if cursor.rowcount == 0:
        return make_response(jsonify({"Error": "Ticket non trovato o stato non modificato"}), 404)

    return make_response(jsonify({"Status": "Stato aggiornato"}), 200)
