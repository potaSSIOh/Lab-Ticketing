from flask import Flask, request, jsonify
from flask_cors import CORS
from routes.aule_routes import aule_routes
from routes.box_routes import box_routes
from routes.fissi_routes import fissi_routes
from routes.portatili_routes import portatili_routes
from routes.ticket_routes import ticket_routes
from routes.utenti_routes import utenti_routes
from routes.login_routes import login_routes
from flask_jwt_extended import JWTManager


app = Flask(__name__, static_folder='static')
app.config["JWT_SECRET_KEY"] = "your_secret_key"  # Use a strong, random key
jwt = JWTManager(app)


# Enable CORS for all routes, allowing localhost:5000 and 127.0.0.1:5000
CORS(app, resources={r"/*": {"origins": ["http://localhost:5000", "http://127.0.0.1:5000"]}})


from flask_jwt_extended import jwt_required, get_jwt_identity

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

# Serve index.html at root
@app.route('/')
def serve_index():
    return app.send_static_file('index.html')

# Register blueprints for your routes (API)
app.register_blueprint(aule_routes)
app.register_blueprint(box_routes)
app.register_blueprint(fissi_routes)
app.register_blueprint(portatili_routes)
app.register_blueprint(ticket_routes)
app.register_blueprint(utenti_routes)
app.register_blueprint(login_routes)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
