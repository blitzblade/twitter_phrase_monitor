from flask import Blueprint, session
from flask import jsonify
from phrase_monitor.libs.decorators import ValidateApiRequest

api = Blueprint('api', __name__, url_prefix='/api')
api_request = ValidateApiRequest()

from phrase_monitor.controllers.v1 import tweets


@api.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api_base():
    return jsonify(code="00", msg="Tweet Phrase Monitor Entry", data={})
