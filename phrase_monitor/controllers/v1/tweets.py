import json
import traceback

import requests

from flask import g, jsonify
from flask import request
from phrase_monitor.controllers import api, api_request
from phrase_monitor.libs.logger import Logger
from phrase_monitor.services.v1.tweets import TweetService


@api.route('/v1/feeds', methods=['GET'])
def get_feeds():
    try:
        feeds = TweetService.get_feeds()
    except Exception as ex:
        Logger.error(__name__, "get_feeds", "02", "Exception occurred: {}".format(str(ex)),
                     traceback.format_exc())
        return jsonify(msg="Could not fetch feeds", data=[]), 400

    return jsonify(msg="Data retrieved successfully'", data=feeds), 200
