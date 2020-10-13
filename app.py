from flask import Flask, jsonify
from flask_cors import CORS
from flask_restful import reqparse

from ocr_center.paddle_ocr import get_ocr_answer
from ocr_center.utils import get_logger

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
CORS(app)

logger = get_logger(__name__)


@app.route('/api/v1/ocr', methods=['POST'])
def do_search_api():
    output = {"nothing": "nothing"}
    args = reqparse.RequestParser(). \
        add_argument("urls", type=str). \
        parse_args()
    if "urls" in args.keys():
        urls = args['urls']
        output = get_ocr_answer(urls=urls)

    return jsonify({"output": output})


@app.route('/api/base64/ocr', methods=['POST'])
def do_search_api():
    output = {"nothing": "nothing"}
    args = reqparse.RequestParser(). \
        add_argument("base64", type=str). \
        parse_args()
    if "base64" in args.keys():
        urls = args['base64']
        output = get_ocr_answer(urls=urls)

    return jsonify({"output": output})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2020)
