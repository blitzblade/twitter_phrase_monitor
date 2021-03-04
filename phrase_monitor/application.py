from flask import Flask,jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from phrase_monitor.config import config
from phrase_monitor.controllers import api

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = config.SESSION_PERMANENT
app.config["SESSION_TYPE"] = config.SESSION_TYPE


engine = create_engine(config.DATABASE_URL)
db = scoped_session(sessionmaker(bind=engine))


app.register_blueprint(api)


@app.errorhandler(404)
def not_found(error):
    return jsonify(code="404", msg="Resource not found"), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify(code="405", msg="Method not allowed"), 405