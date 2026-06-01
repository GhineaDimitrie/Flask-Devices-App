from flask import Flask
from flask_cors import CORS
from routes.devices import devices_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(devices_bp, url_prefix="/api/devices")

if __name__ == "__main__":
    app.run(debug=True)