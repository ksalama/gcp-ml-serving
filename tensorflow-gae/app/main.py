from flask import Flask
from flask import jsonify
from flask import request

import inference

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/version/")
def get_version():
    return jsonify({"version": app.version})


@app.route("/predict/", methods=["POST"])
def predict():

    request_body = request.get_json()
    instance = request_body['instance']
    output = inference.estimate(instance)

    return jsonify(output)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)