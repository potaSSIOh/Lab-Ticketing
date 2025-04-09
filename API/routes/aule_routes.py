from flask import Blueprint, request, jsonify, make_response
from db import db

aule_routes = Blueprint('aule_routes', __name__)

@aule_routes.route('/aule', methods=['GET'])
def get_aule():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM aule")
    return jsonify(cursor.fetchall()), 200

#-----------------------------------------------------

@aule_routes.route('/aule', methods=['POST'])
def add_aula():
    data = request.get_json()
    try:
        nAula = data["nAula"]
        Lab = data["Lab"]
    except KeyError as e:
        return make_response(jsonify({"Error": f"Campo mancante: {str(e)}"}), 400)

    cursor = db.cursor()
    sql = "INSERT INTO aule (nAula, Lab) VALUES (%s, %s)"
    cursor.execute(sql, (nAula, Lab))

    if cursor.rowcount == 0:
        return make_response(jsonify({"Error": "risorsa non inserita"}), 403)

    res = make_response(jsonify({"Status": "OK"}), 201)
    res.headers.add("location", f"/aule/{cursor.lastrowid}")
    return res
