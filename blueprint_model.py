import logging
from flask import Blueprint, jsonify, request
from io import BytesIO, StringIO

import model
from collections import Counter
from random import choice

# define the blueprint
blueprint_model = Blueprint(name="blueprint_model", import_name=__name__)


logger = logging.getLogger('Prevision Model')
logging.basicConfig(
    format='[ %(name)s API ] %(asctime)s %(message)s', level=logging.DEBUG)




@blueprint_model.route("/health", methods=["GET"])
def health():
    res = {"msg": "I'm OK"}
    return res


@blueprint_model.route("/prediction", methods=["POST"])
def make_prediction_on_file(**kwargs):
    logger.info(">>>>>>>>>>>>>>  POST a file")
    logger.debug(kwargs)

    # Get the files from form
    source = request.files['img']
    print(source.filename)
    sourceBin = source.read()

    # Open 2 streams as thery are consumed
    #g = BytesIO(sourceBin)
    #storage.write(g, source.filename)

    # Do what you want with your file
    f = BytesIO(sourceBin)
    res = model.predict_file(f)

    res['source'] = source.filename
    logger.info("<<<<<<<<<<<<<<<File  Prediction API Output")

    return res
