from flask import Blueprint, request, jsonify, make_response

from db import get_db_connection
box_routes = Blueprint('box_routes', __name__)


@box_routes.route('/box')


@box_routes.route('/box', methods=['GET'])

def get_box():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM box")
    return jsonify(cursor.fetchall()), 200

#-----------------------------------------------------

@box_routes.route('/box', methods=['POST'])
def add_box():
    data = request.get_json()
    try:
        codBox = data["codBox"]
    except KeyError as e:
        return make_response(jsonify({"Error": f"Campo mancante: {str(e)}"}), 400)

    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO box (codBox) VALUES (%s)"
    cursor.execute(sql, (codBox,))
    conn.commit()

    if cursor.rowcount == 0:
        return make_response(jsonify({"Error": "risorsa non inserita"}), 403)

    res = make_response(jsonify({"Status": "OK"}), 201)
    res.headers.add("location", f"/box/{cursor.lastrowid}")
    return res
