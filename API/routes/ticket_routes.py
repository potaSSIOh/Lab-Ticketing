from flask import Blueprint, request, jsonify, make_response
from db import db

ticket_routes = Blueprint('ticket_routes', __name__)

@ticket_routes.route('/ticket', methods=['GET'])
def get_tickets():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM ticket")
    return jsonify(cursor.fetchall()), 200

#-----------------------------------------------------

@ticket_routes.route('/ticket', methods=['POST'])
def add_ticket():
    data = request.get_json()
    try:
        descrizione = data["descrizione"]
        dataOra = data["dataOra"]
        creatore = data["creatore"]
        hostnameF = data.get("hostnameF")
        hostnameP = data.get("hostnameP")
        tecnico = data.get("tecnico")
        stato = data["stato"]
    except KeyError as e:
        return make_response(jsonify({"Error": f"Campo mancante: {str(e)}"}), 400)

    cursor = db.cursor()
    sql = """INSERT INTO ticket (descrizione, dataOra, creatore, hostnameF, hostnameP, tecnico, stato)
             VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    cursor.execute(sql, (descrizione, dataOra, creatore, hostnameF, hostnameP, tecnico, stato))

    if cursor.rowcount == 0:
        return make_response(jsonify({"Error": "risorsa non inserita"}), 403)

    res = make_response(jsonify({"Status": "OK"}), 201)
    res.headers.add("location", f"/ticket/{cursor.lastrowid}")
    return res

#-----------------------------------------------------

@ticket_routes.route('/ticket/<int:id>', methods=['PATCH'])
def update_descrizione(id):
    data = request.get_json()
    try:
        descrizione = data["descrizione"]
    except KeyError:
        return make_response(jsonify({"Error": "Campo 'descrizione' mancante"}), 400)

    cursor = db.cursor()
    cursor.execute("UPDATE ticket SET descrizione = %s WHERE id = %s", (descrizione, id))
    db.commit()

    if cursor.rowcount == 0:
        return make_response(jsonify({"Error": "Ticket non trovato o descrizione non modificata"}), 404)

    return make_response(jsonify({"Status": "Descrizione aggiornata"}), 200)

@ticket_routes.route('/ticket/<int:id>/tecnico', methods=['PATCH'])
def update_tecnico(id):
    data = request.get_json()
    try:
        tecnico = data["tecnico"]
    except KeyError:
        return make_response(jsonify({"Error": "Campo 'tecnico' mancante"}), 400)

    cursor = db.cursor()
    cursor.execute("UPDATE ticket SET tecnico = %s WHERE id = %s", (tecnico, id))
    db.commit()

    if cursor.rowcount == 0:
        return make_response(jsonify({"Error": "Ticket non trovato o tecnico non modificato"}), 404)

    return make_response(jsonify({"Status": "Tecnico aggiornato"}), 200)

@ticket_routes.route('/ticket/<int:id>/stato', methods=['PATCH'])
def update_stato(id):
    data = request.get_json()
    try:
        stato = data["stato"]
    except KeyError:
        return make_response(jsonify({"Error": "Campo 'stato' mancante"}), 400)

    cursor = db.cursor()
    cursor.execute("UPDATE ticket SET stato = %s WHERE id = %s", (stato, id))
    db.commit()

    if cursor.rowcount == 0:
        return make_response(jsonify({"Error": "Ticket non trovato o stato non modificato"}), 404)

    return make_response(jsonify({"Status": "Stato aggiornato"}), 200)
