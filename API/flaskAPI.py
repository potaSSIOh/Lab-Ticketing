#REMEMBER TO IMPORT FLASK AND PYMYSQL IN THE MACHINE
from flask import Flask,jsonify,request,make_response 
import pymysql
from flask_cors import CORS 
db = pymysql.connect(host="127.0.0.1", user="root", password="", database="labticketing",autocommit=True, cursorclass=pymysql.cursors.DictCursor)
app = Flask(__name__)
CORS(app)

#----------------------------------------------------------------------------------------
# GET methods

@app.route('/aule',methods=['GET']) 
def aule():
    cursor = db.cursor() 
    sql = "SELECT * FROM aule" 
    cursor.execute(sql) 
    results = cursor.fetchall() 
    return jsonify(results),200

@app.route('/box',methods=['GET']) 
def box():
    cursor = db.cursor() 
    sql = "SELECT * FROM box" 
    cursor.execute(sql) 
    results = cursor.fetchall() 
    return jsonify(results),200

@app.route('/utenti',methods=['GET']) 
def utenti():
    cursor = db.cursor() 
    sql = "SELECT * FROM utenti" 
    cursor.execute(sql) 
    results = cursor.fetchall() 
    return jsonify(results),200

@app.route('/fissi', methods=['GET'])
@app.route('/fissi/<int:Aula>', methods=['GET'])
def fissi(Aula=None):
    cursor = db.cursor()
    if Aula is not None:
        sql = "SELECT * FROM fissi WHERE Aula = %s"
        cursor.execute(sql, (Aula,))
    else:
        sql = "SELECT * FROM fissi"
        cursor.execute(sql)
    results = cursor.fetchall()
    if not results:
        return jsonify({"Error": "risorsa non trovata"}), 404
    else:
        return jsonify(results), 200

@app.route('/portatili', methods=['GET'])
@app.route('/portatili/<string:codBox>',methods=['GET']) 
def portatili(codBox=None):
    cursor = db.cursor()
    if codBox is not None:
        sql = "SELECT * FROM portatili WHERE codBox = %s"
        cursor.execute(sql, (codBox,))
    else:
        sql = "SELECT * FROM portatili"
        cursor.execute(sql)
    results = cursor.fetchall()

    if not results:
        return jsonify({"Error": "risorsa non trovata"}), 404
    else:
        return jsonify(results), 200

@app.route('/ticket',methods=['GET']) 
def ticket():
    cursor = db.cursor() 
    sql = "SELECT * FROM ticket" 
    cursor.execute(sql) 
    results = cursor.fetchall() 
    return jsonify(results),200

#----------------------------------------------------------------------------------------
# POST methods

#metodo per aggiungere un utente
@app.route('/utenti', methods=['POST'])
def addUtenti():
    data = request.get_json()
    try:
        name_mail = data["name_mail"]
        password = data["password"]
        autorizzato = data["autorizzato"]
    except KeyError as e:
        return make_response(jsonify({"Error": f"Campo mancante: {str(e)}"}), 400)
    cursor = db.cursor() 
    sql = "insert into utenti (name_mail, password, autorizzato) values (%s, %s, %s)" 
    cursor.execute(sql, (name_mail, password, autorizzato)) 
    if cursor.rowcount==0: 
        res=make_response(jsonify({"Error":"risorsa non inserita"}),403) 
    else: 
        res=make_response(jsonify({"Status":"OK "}),201) 
        res.headers.add("location","/utenti/"+str(cursor.lastrowid)) 
    return res

#metodo per aggiungere un ticket
@app.route('/ticket', methods=['POST'])
def addTicket():
    data = request.get_json()
    try:
        descrizione = data["descrizione"]
        dataOra = data["dataOra"]
        creatore = data["creatore"]
        hostnameF = data["hostnameF"] if "hostnameF" in data else None
        hostnameP = data["hostnameP"] if "hostnameP" in data else None
        tecnico = data["tecnico"] if "tecnico" in data else None
        stato = data["stato"]
    except KeyError as e:
        return make_response(jsonify({"Error": f"Campo mancante: {str(e)}"}), 400)
    cursor = db.cursor() 
    sql = "insert into ticket (descrizione, dataOra, creatore, hostnameF, hostnameP, tecnico, stato) values (%s, %s, %s, %s, %s, %s, %s)" 
    cursor.execute(sql, (descrizione, dataOra, creatore, hostnameF, hostnameP, tecnico, stato)) 
    if cursor.rowcount==0: 
        res=make_response(jsonify({"Error":"risorsa non inserita"}),403) 
    else: 
        res=make_response(jsonify({"Status":"OK "}),201) 
        res.headers.add("location","/ticket/"+str(cursor.lastrowid)) 
    return res

#metodo per aggiungere un fisso
@app.route('/fissi', methods=['POST'])
def addFisso():
    data = request.get_json()
    try:
        HostName = data["HostName"]
        Aula = data["Aula"]
    except KeyError as e:
        return make_response(jsonify({"Error": f"Campo mancante: {str(e)}"}), 400)
    cursor = db.cursor() 
    sql = "insert into fissi (HostName, Aula) values (%s, %s)" 
    cursor.execute(sql, (HostName, Aula)) 
    if cursor.rowcount==0: 
        res=make_response(jsonify({"Error":"risorsa non inserita"}),403) 
    else: 
        res=make_response(jsonify({"Status":"OK "}),201) 
        res.headers.add("location","/fissi/"+str(cursor.lastrowid)) 
    return res

#metodo per aggiungere un'aula
@app.route('/aule', methods=['POST'])
def addAula():
    data = request.get_json()
    try:
        nAula = data["nAula"]
        Lab = data["Lab"]
    except KeyError as e:
        return make_response(jsonify({"Error": f"Campo mancante: {str(e)}"}), 400)
    cursor = db.cursor() 
    sql = "insert into aule (nAula, Lab) values (%s, %s)" 
    cursor.execute(sql, (nAula, Lab)) 
    if cursor.rowcount==0: 
        res=make_response(jsonify({"Error":"risorsa non inserita"}),403) 
    else: 
        res=make_response(jsonify({"Status":"OK "}),201) 
        res.headers.add("location","/aule/"+str(cursor.lastrowid)) 
    return res

#metodo per aggiungere un portatile
@app.route('/portatili', methods=['POST'])
def addPortatile():
    data = request.get_json()
    try:
        HostName = data["HostName"]
        codBox = data["codBox"]
    except KeyError as e:
        return make_response(jsonify({"Error": f"Campo mancante: {str(e)}"}), 400)
    cursor = db.cursor() 
    sql = "insert into portatili (HostName, codBox) values (%s, %s)" 
    cursor.execute(sql, (HostName, codBox)) 
    if cursor.rowcount==0: 
        res=make_response(jsonify({"Error":"risorsa non inserita"}),403) 
    else: 
        res=make_response(jsonify({"Status":"OK "}),201) 
        res.headers.add("location","/portatili/"+str(cursor.lastrowid)) 
    return res

#metodo per aggiungere un box
@app.route('/box', methods=['POST'])
def addBox():
    data = request.get_json()
    try:
        codBox = data["codBox"]
    except KeyError as e:
        return make_response(jsonify({"Error": f"Campo mancante: {str(e)}"}), 400)
    cursor = db.cursor() 
    sql = "insert into box (codBox) values (%s)" 
    cursor.execute(sql, (codBox,)) 
    if cursor.rowcount==0: 
        res=make_response(jsonify({"Error":"risorsa non inserita"}),403) 
    else: 
        res=make_response(jsonify({"Status":"OK "}),201) 
        res.headers.add("location","/box/"+str(cursor.lastrowid)) 
    return res

#----------------------------------------------------------------------------------------
# PATCH method

#metodo per modificare la password di un utente
@app.route('/utenti/<int:id>', methods=['PATCH'])
def update_password(id):
    try:
        data = request.get_json()
    except KeyError:
        return make_response(jsonify({"Error": "Campo 'descrizione' mancante"}), 400)
    new_password = data["password"]
    cursor = db.cursor()
    sql = "UPDATE utenti SET password = %s WHERE id = %s"
    cursor.execute(sql, (new_password, id))
    db.commit()

    if cursor.rowcount == 0:
        return make_response(jsonify({"Error": "Utente non trovato o password non modificata"}), 404)

    return make_response(jsonify({"Status": "Password aggiornata"}), 200)

#metodo per modificare la descrizione di un ticket
@app.route('/ticket/<int:id>', methods=['PATCH'])
def update_ticket_description(id):
    data = request.get_json()
    try:
        new_descrizione = data["descrizione"]
    except KeyError:
        return make_response(jsonify({"Error": "Campo 'descrizione' mancante"}), 400)
    cursor = db.cursor()
    sql = "UPDATE ticket SET descrizione = %s WHERE id = %s"
    cursor.execute(sql, (new_descrizione, id))
    db.commit()
    if cursor.rowcount == 0:
        return make_response(jsonify({"Error": "Ticket non trovato o descrizione non modificata"}), 404)
    return make_response(jsonify({"Status": "Descrizione aggiornata"}), 200)

#metodo per modificare il tecnico
@app.route('/ticket/<int:id>/tecnico', methods=['PATCH'])
def update_ticket_tecnico(id):
    data = request.get_json()
    try:
        new_tecnico = data["tecnico"]
    except KeyError:
        return make_response(jsonify({"Error": "Campo 'tecnico' mancante"}), 400)
    cursor = db.cursor()
    sql = "UPDATE ticket SET tecnico = %s WHERE id = %s"
    cursor.execute(sql, (new_tecnico, id))
    db.commit()
    if cursor.rowcount == 0:
        return make_response(jsonify({"Error": "Ticket non trovato o tecnico non modificato"}), 404)
    return make_response(jsonify({"Status": "Tecnico aggiornato"}), 200)

#metodo per cambiare lo stato dei ticket
@app.route('/ticket/<int:id>/stato', methods=['PATCH'])
def update_ticket_stato(id):
    data = request.get_json()
    try:
        new_stato = data["stato"]
    except KeyError:
        return make_response(jsonify({"Error": "Campo 'stato' mancante"}), 400)
    cursor = db.cursor()
    sql = "UPDATE ticket SET stato = %s WHERE id = %s"
    cursor.execute(sql, (new_stato, id))
    db.commit()
    if cursor.rowcount == 0:
        return make_response(jsonify({"Error": "Ticket non trovato o stato non modificato"}), 404)
    return make_response(jsonify({"Status": "Stato aggiornato"}), 200)

#----------------------------------------------------------------------------------------

app.run()