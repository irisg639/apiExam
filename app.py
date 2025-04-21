from flask import Flask, send_from_directory
from config import db, migrate
from routes.usuario import user_bp
from flask_cors import CORS
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
import os
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint

load_dotenv()
app=Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY']='jacky2710'
jwt=JWTManager(app)

app.config['SQLALCHEMY_DATABASE_URI']=os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

app.config['SQLALCHEMY_DATABASE_URI']=os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db.init_app(app)
migrate.init_app(app, db)

app.register_blueprint(user_bp, url_prefix='/users')

@app.route("/swagger.yaml")
def get_swagger_yaml():
    return send_from_directory(os.path.dirname(__file__), "swagger.yaml")

SWAGGER_URL = "/docs"
API_URL = "/swagger.yaml"
swagger_ui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

if __name__=='__main__':
    app.run(debug=True)