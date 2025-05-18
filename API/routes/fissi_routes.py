from flask import Blueprint, request, jsonify, make_response

from db import get_db_connection

fissi_routes = Blueprint('fissi_routes', __name__)

@fissi_routes.route('/fissi', methods=['GET'])
@fissi_routes.route('/fissi/<int:Aula>', methods=['GET'])
def get_fissi(Aula=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if Aula:
        cursor.execute("SELECT * FROM fissi WHERE Aula = %s", (Aula,))
    else:
        cursor.execute("SELECT * FROM fissi")
    results = cursor.fetchall()

    if not results:
        return jsonify({"Error": "risorsa non trovata"}), 404
    return jsonify(results), 200

#-----------------------------------------------------

@fissi_routes.route('/fissi', methods=['POST'])
def add_fisso():
    data = request.get_json()
    try:
        HostName = data["HostName"]
        Aula = data["Aula"]
    except KeyError as e:
        return make_response(jsonify({"Error": f"Campo mancante: {str(e)}"}), 400)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO fissi (HostName, Aula) VALUES (%s, %s)", (HostName, Aula))
    conn.commit()

    if cursor.rowcount == 0:
        return make_response(jsonify({"Error": "risorsa non inserita"}), 403)

    res = make_response(jsonify({"Status": "OK"}), 201)
    res.headers.add("location", f"/fissi/{cursor.lastrowid}")
    return res
