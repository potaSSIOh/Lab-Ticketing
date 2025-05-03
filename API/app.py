from flask import Flask
from flask_cors import CORS
from routes.aule_routes import aule_routes
from routes.box_routes import box_routes
from routes.fissi_routes import fissi_routes
from routes.portatili_routes import portatili_routes
from routes.ticket_routes import ticket_routes
from routes.utenti_routes import utenti_routes
from routes.password_routes import password_routes

app = Flask(__name__)
CORS(app)

# Registrazione dei blueprint
app.register_blueprint(aule_routes)
app.register_blueprint(box_routes)
app.register_blueprint(fissi_routes)
app.register_blueprint(portatili_routes)
app.register_blueprint(ticket_routes)
app.register_blueprint(utenti_routes)
app.register_blueprint(password_routes)

if __name__ == '__main__':
    app.run(debug=True)