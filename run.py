from flask import Flask
from config import app_config

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    
    from app import api_bp
    app.register_blueprint(api_bp, url_prefix='/content')

    from Model import db
    db.init_app(app)

    return app


if __name__ == "__main__":
    app = create_app("development")
    app.run(debug=True)
