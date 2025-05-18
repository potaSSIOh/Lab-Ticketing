from flask import Blueprint, request, jsonify, make_response

from db import get_db_connection

portatili_routes = Blueprint('portatili_routes', __name__)

#-----------------------------------------------------

@portatili_routes.route('/portatili', methods=['GET'])
@portatili_routes.route('/portatili/<string:codBox>', methods=['GET'])
def get_portatili(codBox=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if codBox:
        cursor.execute("SELECT * FROM portatili WHERE codBox = %s", (codBox,))
    else:
        cursor.execute("SELECT * FROM portatili")
    results = cursor.fetchall()

    if not results:
        return jsonify({"Error": "risorsa non trovata"}), 404
    return jsonify(results), 200

#-----------------------------------------------------

@portatili_routes.route('/portatili', methods=['POST'])
def add_portatile():
    data = request.get_json()
    try:
        hostname = data["hostname"]
        codBox = data["codBox"]
    except KeyError as e:
        return make_response(jsonify({"Error": f"Campo mancante: {str(e)}"}), 400)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO portatili (hostname, codBox) VALUES (%s, %s)", (hostname, codBox))
    conn.commit()

    if cursor.rowcount == 0:
        return make_response(jsonify({"Error": "risorsa non inserita"}), 403)

    res = make_response(jsonify({"Status": "OK"}), 201)
    res.headers.add("location", f"/portatili/{cursor.lastrowid}")
    return res
