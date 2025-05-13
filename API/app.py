from flask import Flask
from flask_cors import CORS
from routes.aule_routes import aule_routes
from routes.box_routes import box_routes
from routes.fissi_routes import fissi_routes
from routes.portatili_routes import portatili_routes
from routes.ticketf_routes import ticketf_routes
from routes.ticketp_routes import ticketp_routes
from routes.utenti_routes import utenti_routes

app = Flask(__name__)
CORS(app)

# Registrazione dei blueprint
app.register_blueprint(aule_routes)
app.register_blueprint(box_routes)
app.register_blueprint(fissi_routes)
app.register_blueprint(portatili_routes)
app.register_blueprint(ticketf_routes)
app.register_blueprint(ticketp_routes)
app.register_blueprint(utenti_routes)

if __name__ == '__main__':
    app.run(debug=True)