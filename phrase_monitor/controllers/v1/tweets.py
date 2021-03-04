import traceback
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
        return jsonify(msg="Could not fetch feeds", data=[]), 404

    return jsonify(msg="Data retrieved successfully'", data=feeds), 200


@api.route('/v1/phrase/<id>', methods=['PUT'])
@api_request.required_form_params('phrase')
def edit_phrase(id):
    phrase = request.form["phrase"]
    if id:
        exist_phrase = TweetService.get_phrase_by_id(id)
        if exist_phrase is None:
            return jsonify(msg="Phrase does not exist"), 404
    try:
        response = TweetService.edit_phrase(id, phrase)
        if response:
            return jsonify(msg="Phrase updated successfully'"), 200

        return jsonify(msg="Could not update phrase"), 404
    except Exception as ex:
        Logger.error(__name__, "edit_phrase", "02", "Exception occurred: {}".format(str(ex)),
                     traceback.format_exc())
        return jsonify(msg="Could not update phrase"), 404


@api.route('/v1/phrase', methods=['POST'])
@api_request.required_form_params('phrase', 'user_id')
def add_phrase():
    phrase = request.form["phrase"]
    user_id = request.form["user_id"]

    if phrase:
        exist_phrase = TweetService.get_phrase_by_name(phrase)
        if exist_phrase is not None:
            return jsonify(msg="Phrase already exist"), 404
    try:
        response = TweetService.add_phrase(user_id, phrase)
        if response:
            return jsonify(msg="Phrase added successfully'"), 200

        return jsonify(msg="Could not add phrase"), 404
    except Exception as ex:
        Logger.error(__name__, "add_phrase", "02", "Exception occurred: {}".format(str(ex)),
                     traceback.format_exc())
        return jsonify(msg="Could not add phrase"), 404


@api.route('/v1/phrases', methods=['GET'])
def get_phrases():
    user_id = request.args.get('user_id')
    try:
        phrases = TweetService.get_phrases(user_id)
    except Exception as ex:
        Logger.error(__name__, "get_phrases", "02", "Exception occurred: {}".format(str(ex)),
                     traceback.format_exc())
        return jsonify(msg="Could not fetch phrases", data=[]), 404

    return jsonify(msg="Data retrieved successfully'", data=phrases), 200


@api.route('/v1/phrase/occurrences', methods=['GET'])
def get_phrase_occurrences():
    try:
        phrases = TweetService.get_phrase_occurrences()
    except Exception as ex:
        Logger.error(__name__, "get_phrase_occurrences", "02", "Exception occurred: {}".format(str(ex)),
                     traceback.format_exc())
        return jsonify(msg="Could not fetch phrase occurrences", data=[]), 404

    return jsonify(msg="Data retrieved successfully'", data=phrases), 200


@api.route('/v1/phrase/average_phrase_per_minute', methods=['GET'])
def get_average_phrase_per_minute():
    try:
        phrases = TweetService.get_average_phrase_per_minute()
    except Exception as ex:
        Logger.error(__name__, "get_average_phrase_per_minute", "02", "Exception occurred: {}".format(str(ex)),
                     traceback.format_exc())
        return jsonify(msg="Could not fetch average phrase per minute", data=[]), 404

    return jsonify(msg="Data retrieved successfully'", data=phrases), 200


@api.route('/v1/phrase/chart_data_for_minutes', methods=['GET'])
def get_chart_data_for_minutes():
    try:
        phrases = TweetService.get_chart_data_for_minutes()
    except Exception as ex:
        Logger.error(__name__, "get_chart_data_for_minutes", "02", "Exception occurred: {}".format(str(ex)),
                     traceback.format_exc())
        return jsonify(msg="Could not fetch chart data for minutes", data=[]), 404

    return jsonify(msg="Data retrieved successfully'", data=phrases), 200
