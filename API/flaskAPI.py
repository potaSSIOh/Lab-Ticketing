#REMEMBER TO IMPORT FLASK AND PYMYSQL IN THE MACHINE
from flask import Flask,jsonify,request,make_response 
import pymysql 
db = pymysql.connect(host="127.0.0.1", user="root", password="", database="labticketing",autocommit=True, cursorclass=pymysql.cursors.DictCursor)
app = Flask(__name__)

# GET method

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

@app.route('/fissi/<int:Aula>', methods=['GET']) 
def fissi(Aula): 
    cursor = db.cursor()
    sql = "SELECT * FROM fissi WHERE Aula = %s"
    cursor.execute(sql, (Aula,))
    result = cursor.fetchone()

    if result is None:
        return jsonify({"Error": "risorsa non trovata"}), 404
    else:
        return jsonify(result), 200



@app.route('/portatili/<string:codBox>',methods=['GET']) 
def portatili():
    cursor = db.cursor() 
    codBox = "%s"
    sql = "SELECT * FROM portatili where codBox=%s" 
    cursor.execute(sql, (codBox)) 
    results = cursor.fetchone() 
    if results==None:
        return jsonify({"Error":"risorsa non trovata"}),404
    else:
        return jsonify(results),200

@app.route('/ticket',methods=['GET']) 
def ticket():
    cursor = db.cursor() 
    sql = "SELECT * FROM ticket" 
    cursor.execute(sql) 
    results = cursor.fetchall() 
    return jsonify(results),200



app.run()