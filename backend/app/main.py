from flask import Flask
from app.api.routes import api_bp
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    
    # Register API blueprint
    app.register_blueprint(api_bp, url_prefix="/api")
    
    # Basic route for the web interface
    @app.route("/")
    def index():
        return render_template("index.html")
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)