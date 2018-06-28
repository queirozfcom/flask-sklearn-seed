import logging
import pickle
import re
import traceback

from concurrent_log_handler import ConcurrentRotatingFileHandler
from flask import Flask, request, jsonify, make_response
from schema import SchemaError

import settings
from helpers import features, validation
from utils import files

app = Flask(__name__)
clf = None


#####################################################################################
################################### ROUTES ##########################################
#####################################################################################

@app.route('/<version>/healthcheck', methods=['GET'])
def healthcheck(version):
    if models.get(version, None) is not None:
        return ("OK", 200)
    else:
        return ("Not OK", 200)


@app.route('/<version>/predict', methods=['POST'])
def predict(version):
    if models.get(version, None) is not None:

        try:

            payload = request.json

            validation.validate("predict", payload)

            feature_vector = features.make_feature_vector(payload)

            prediction = models[version].predict_proba(feature_vector)[:, 1]

            rounded_prediction = round(prediction, 4)

            return make_response((jsonify({'id': payload["id"], 'prediction': rounded_prediction})))

        except SchemaError as ex:
            return make_response(jsonify({"message": ex.message}), 400)

    else:
        return make_response(jsonify({"message": "Trained model version '{}' was not found.".format(version)}), 404)


@app.after_request
def after_request(response):
    # 500 is already logged via @app.errorhandler.
    if response.status_code != 500:
        app.logger.info('%s %s %s %s %s',
                        request.remote_addr,
                        request.method,
                        request.scheme,
                        request.full_path,
                        response.status)
    return response


@app.errorhandler(Exception)
def exceptions(e):
    tb = traceback.format_exc()

    resp = "Internal Server Error", 500

    app.logger.error('%s %s %s %s 5XX INTERNAL SERVER ERROR\n%s',
                     request.remote_addr,
                     request.method,
                     request.scheme,
                     request.full_path,
                     tb)

    return resp


#####################################################################################
############################### INTIALIZATION CODE ##################################
#####################################################################################

if __name__ == '__main__':
    try:
        port = int(settings.PORT)
    except Exception as e:
        print("Failed to bind to port {}".format(settings.PORT))
        port = 80

    pattern = '^.+\-(v\d+)\.p$'

    models_available = files.get_files_matching(settings.MODELS_ROOT, '^.+\-v\d+\.p$')

    models = dict()

    # load the models to memory only once, when the app boots
    for path_to_model in models_available:
        version_id = re.match(pattern, path_to_model).group(1)
        models[version_id] = pickle.load(open(path_to_model, "rb"))

    # 10M = 1024*1000*10 bytes
    handler = ConcurrentRotatingFileHandler(settings.LOG_FILE, maxBytes=1024 * 1000 * 10, backupCount=5, use_gzip=True)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    app.logger.addHandler(handler)

    # https://stackoverflow.com/a/20423005/436721
    app.logger.setLevel(logging.INFO)

    app.run(host='0.0.0.0', port=port)

else:
    pattern = '^.+\-(v\d+)\.p$'

    models_available = files.get_files_matching(settings.MODELS_ROOT, '^.+\-v\d+\.p$')

    models = dict()

    # load the models only once, when the app boots
    for path_to_model in models_available:
        version_id = re.match(pattern, path_to_model).group(1)
        models[version_id] = pickle.load(open(path_to_model, "rb"))

    # disable logging so it doesn't interfere with testing
    app.logger.disabled = True
