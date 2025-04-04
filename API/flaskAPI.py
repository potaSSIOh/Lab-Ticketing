#REMEMBER TO IMPORT FLASK AND PYMYSQL IN THE MACHINE
from flask import Flask,jsonify,request,make_response 
import pymysql 
db = pymysql.connect(host="127.0.0.1", user="root", password="", database="labticketing",autocommit=True, cursorclass=pymysql.cursors.DictCursor)
app = Flask(__name__)

# GET methods

@app.route('/',methods=['GET'])
def hello():
    return "hello"

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

# POST methods

#Content-Type:application/json 
@app.route('/utenti', methods=['POST'])
def addUtenti(name_mail, password, autorizzato):
    data = request.json 
    cursor = db.cursor() 
    sql = "insert into utenti (name_mail, password, autorizzato) values (%s, %s, %s)" 
    cursor.execute(sql,(data["name_mail"]))
    cursor.execute(sql,(data["password"]))
    cursor.execute(sql,(data["autorizzato"]))  
    if cursor.rowcount==0: 
        res=make_response(jsonify({"Error":"risorsa non inserita"}),403) 
    else: 
        res=make_response(jsonify({"Status":"OK "}),201) 
        res.headers.add("location","/utenti/"+str(cursor.lastrowid)) 
    return res

app.run()