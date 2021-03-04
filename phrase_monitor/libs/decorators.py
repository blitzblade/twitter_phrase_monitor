import json
import traceback
from functools import wraps
from flask import jsonify
from flask import request
from phrase_monitor.libs.logger import Logger


class ValidateApiRequest:
    def json(self, func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            request_headers = dict(request.headers)
            # print("Printing request.data{}".format(request.data))
            # Logger.debug(__name__, "request_headers", "00", "Printing request_headers")
            if 'Content-Type' not in request_headers or 'application/json' not in request_headers['Content-Type']:
                return jsonify(msg='This API requires JSON'), 411
            elif request.data is None:
                return jsonify(msg='No JSON data'), 400

            try:
                json_data = json.loads(request.data.decode('utf8'))
                # print("Printing json_data {}".format(json_data))
            except Exception:
                return jsonify(msg='Malformed JSON'), 400

            return func(*args, **kwargs)

        return wrapper

    def required_body_params(self, *required_params):
        """
        Utility function for checking request body parameters flagged as required
        """

        def wrapper(f):

            @wraps(f)
            def wrapped(*args, **kwargs):
                Logger.debug(__name__, "required_body_params", "00",
                             "Required Parameter(s): {}".format(required_params))
                try:
                    # extract the json body into a python dict
                    request_data = json.loads(request.data.decode('utf-8'))
                except Exception as e:
                    traceback.print_exc()
                    Logger.error(__name__, "required_body_params", "02", "Malformed JSON Body passed",
                                 traceback.format_exc())
                    response = {'msg': 'Malformed JSON', 'data': {}}
                    return jsonify(**response), 400

                # check the parameters received against the required parameters, add missing/blank parameters to list
                missing_params = []
                # print("Printing required_params {}".format(required_params))
                # print("Printing request_data {}".format(request_data))
                for param in required_params:
                    print("Printing param {}".format(param))
                    if param not in request_data or str(request_data[param]) == '':
                        missing_params.append(param)

                print("Printing missing_params | {}".format(missing_params))

                # display the missing parameters
                if len(missing_params) > 0:
                    response = {
                                'msg': 'Missing and/or blank parameters: {}'.format(', '.join(missing_params))
                                }
                    return jsonify(**response), 400
                return f(*args, **kwargs)
            return wrapped
        return wrapper

    def required_form_params(self, *required_params):
        """
        Utility function for checking request body parameters flagged as required
        """

        def wrapper(f):

            @wraps(f)
            def wrapped(*args, **kwargs):
                Logger.debug(__name__, "required_form_params", "00",
                             "Required Parameter(s): {}".format(required_params))
                try:
                    # extract form data into python dict
                    form_data = dict(request.form)
                except Exception as e:
                    traceback.print_exc()
                    Logger.error(__name__, "required_form_params", "02", "Invalid form data", traceback.format_exc())
                    response = {'msg': 'Invalid form'}
                    return jsonify(**response), 400

                # check the parameters received against the required parameters, add missing/blank parameters to list
                missing_params = []
                for param in required_params:
                    if param not in form_data or str(form_data[param]) == '':
                        missing_params.append(param)

                # display the missing parameters
                if len(missing_params) > 0:
                    response = {
                                'msg': 'Missing and/or blank parameters: {}'.format(', '.join(missing_params))
                                }
                    return jsonify(**response), 400
                return f(*args, **kwargs)
            return wrapped
        return wrapper

    def required_query_params(self, *required_params):
        """
        Utility function for checking request body parameters flagged as required
        """

        def wrapper(f):

            @wraps(f)
            def wrapped(*args, **kwargs):
                Logger.debug(__name__, "required_query_params", "00",
                             "Required Parameter(s): {}".format(required_params))
                try:
                    # extract the json body into a python dict
                    request_params = request.args.to_dict()
                except Exception as e:
                    traceback.print_exc()
                    Logger.error(__name__, "required_query_params", "02", "Error while getting query params",
                                 traceback.format_exc())
                    response = {'msg': 'Could not get query parameters'}
                    return jsonify(**response), 400

                # check the parameters received against the required parameters, add missing/blank parameters to list
                missing_params = []
                for param in required_params:
                    if param not in request_params or str(request_params[param]) == '':
                        missing_params.append(param)

                # display the missing parameters
                if len(missing_params) > 0:
                    response = {
                        'msg': 'Missing and/or blank parameters: {}'.format(', '.join(missing_params))
                    }
                    return jsonify(**response), 400
                return f(*args, **kwargs)
            return wrapped
        return wrapper