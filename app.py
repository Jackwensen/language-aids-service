# from crypt import methods
import json
from flask import Flask, Response, jsonify, make_response
from flask_cors import cross_origin

import text2signl as text2sgl

app = Flask(__name__)

@app.route("/")
@cross_origin()
def home():
    return "Hello, Flask!"

@app.route("/text2signal/<message>", methods=['GET'])
@cross_origin()
def text2signal(message):
    # if not message: return make_response(jsonify({'error': 'Not found'}), 404)
    res = text2sgl.text2signal(message)
    # print(res)
    json_string = json.dumps(res,ensure_ascii = False)
    response = Response(json_string,content_type="application/json; charset=utf-8" )
    return response

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)

    