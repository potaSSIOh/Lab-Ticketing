from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from routes.aule_routes import aule_routes
from routes.box_routes import box_routes
from routes.fissi_routes import fissi_routes
from routes.portatili_routes import portatili_routes
from routes.ticket_routes import ticket_routes
from routes.utenti_routes import utenti_routes

app = Flask(__name__)

# accetto tutte le origini
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

#tutte le opzioni accettate
@app.after_request
def apply_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"  
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = (
        "Content-Type,Authorization,Access-Control-Allow-Credentials"
    )
    return response

app.register_blueprint(aule_routes)
app.register_blueprint(box_routes)
app.register_blueprint(fissi_routes)
app.register_blueprint(portatili_routes)
app.register_blueprint(ticket_routes)
app.register_blueprint(utenti_routes)

if __name__ == '__main__':
    app.run(port=5000, debug=True)