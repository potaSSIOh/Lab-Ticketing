from flask import Blueprint, request, jsonify, make_response

from db import db

ticketf_routes = Blueprint('ticketf_routes', __name__)

@ticketf_routes.route('/ticketf', methods=['GET'])
@ticketf_routes.route('/ticketf/<string:hostnameF>', methods=['GET'])
def get_hostnameF(hostnameF=None):
    cursor = db.cursor()
    if hostnameF:
        cursor.execute("SELECT * FROM ticketf WHERE hostnameF = %s", (hostnameF,))
    else:
        cursor.execute("SELECT * FROM ticketf")
    results = cursor.fetchall()

    if not results:
        return jsonify({"Error": "risorsa non trovata"}), 404
    return jsonify(results), 200

#-----------------------------------------------------

@ticketf_routes.route('/ticketf', methods=['POST'])
def add_ticketf():
    data = request.get_json()
    try:
        descrizione = data["descrizione"]
        dataOra = data["dataOra"]
        creatore = data["creatore"]
        hostnameF = data.get("hostnameF")
        tecnico = data.get("tecnico")
        stato = data["stato"]
    except KeyError as e:
        return make_response(jsonify({"Error": f"Campo mancante: {str(e)}"}), 400)

    cursor = db.cursor()
    sql = """INSERT INTO ticketf (descrizione, dataOra, creatore, hostnameF, tecnico, stato)
             VALUES (%s, %s, %s, %s, %s, %s)"""
    cursor.execute(sql, (descrizione, dataOra, creatore, hostnameF, tecnico, stato))
    db.commit()

    if cursor.rowcount == 0:
        return make_response(jsonify({"Error": "risorsa non inserita"}), 403)

    res = make_response(jsonify({"Status": "OK"}), 201)
    res.headers.add("location", f"/ticketf/{cursor.lastrowid}")
    return res

#-----------------------------------------------------

@ticketf_routes.route('/ticketf/<int:id>', methods=['PATCH'])
def update_descrizione(id):
    data = request.get_json()
    try:
        descrizione = data["descrizione"]
    except KeyError:
        return make_response(jsonify({"Error": "Campo 'descrizione' mancante"}), 400)

    cursor = db.cursor()
    cursor.execute("UPDATE ticketf SET descrizione = %s WHERE id = %s", (descrizione, id))
    db.commit()

    if cursor.rowcount == 0:
        return make_response(jsonify({"Error": "Ticket non trovato o descrizione non modificata"}), 404)

    return make_response(jsonify({"Status": "Descrizione aggiornata"}), 200)

@ticketf_routes.route('/ticketf/<int:id>/tecnico', methods=['PATCH'])
def update_tecnico(id):
    data = request.get_json()

    if "tecnico" not in data:
        return make_response(jsonify({"Error": "Campo 'tecnico' mancante"}), 400)

    tecnico_email = data["tecnico"]

    # Opzionale: Verifica che il tecnico esista ed è autorizzato
    cursor = db.cursor()
    cursor.execute("SELECT * FROM utenti WHERE name_mail = %s AND autorizzato = 1", (tecnico_email,))
    tecnico = cursor.fetchone()

    if not tecnico:
        return make_response(jsonify({"Error": "Tecnico non valido o non autorizzato"}), 400)

    # Aggiorna il tecnico nel ticket
    cursor.execute("UPDATE ticketf SET tecnico = %s WHERE IdTicket = %s", (tecnico_email, id))
    db.commit()

    if cursor.rowcount == 0:
        return make_response(jsonify({"Error": "Ticket non trovato o tecnico non modificato"}), 404)

    return make_response(jsonify({"Status": "Tecnico aggiornato con successo"}), 200)


@ticketf_routes.route('/ticketf/<int:id>/stato', methods=['PATCH'])
def update_stato(id):
    data = request.get_json()
    try:
        stato = data["stato"]
    except KeyError:
        return make_response(jsonify({"Error": "Campo 'stato' mancante"}), 400)

    cursor = db.cursor()
    cursor.execute("UPDATE ticketf SET stato = %s WHERE IdTicket = %s", (stato, id))
    db.commit()

    if cursor.rowcount == 0:
        return make_response(jsonify({"Error": "Ticket non trovato o stato non modificato"}), 404)

    return make_response(jsonify({"Status": "Stato aggiornato"}), 200)
