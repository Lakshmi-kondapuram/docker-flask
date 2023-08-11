# Local imports
import datetime
import gzip
import json

# Third part imports
from flask import render_template, request
import joblib
import pandas as pd

from ms import app
from ms.functions import get_model_response


model_name = "Breast Cancer Wisconsin (Diagnostic)"
model_file = 'model_binary.dat.gz'
version = "v1.0.0"

@app.route('/',methods=["Get","POST"])
def home():
    return render_template("index.html")

@app.route('/info', methods=['GET'])
def info():
    """Return model information, version, how to call"""
    result = {}

    result["name"] = model_name
    result["version"] = version

    return result


@app.route('/health', methods=['GET'])
def health():
    """Return service health"""
    return 'ok'


@app.route('/predict', methods=['POST'])
def predict():
    feature_dict = request.get_json()
    if not feature_dict:
        return {
            'error': 'Body is empty.'
        }, 500

    try:
        response = get_model_response(feature_dict)
    except ValueError as e:
        return {'error': str(e).split('\n')[-1].strip()}, 500

    return response, 200


#predictmodel
@app.route('/predictmodel',methods=["POST"])
def predictmodel():
    uploaded_file = request.files['file']
    json_bytes = uploaded_file.read()
    my_json = json_bytes.decode('utf8').replace("'",'"')
    print(f"my_json--->"+my_json)
    jsondata = json.loads(my_json)
    print(jsondata)
    if not jsondata:
        return {
            'error': 'Error with file.'
        }, 500

    try:
        response = get_model_response(jsondata)
    except ValueError as e:
        return {'error': str(e).split('\n')[-1].strip()}, 500

    return response, 200



if __name__ == '__main__':
    #app.run(host='10.0.2.15')
    app.run()
