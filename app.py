from flask import Flask, jsonify
from flask_cors import CORS
from flask_restful import reqparse

from ocr_center.paddle_ocr import get_ocr_answer, get_logger

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
CORS(app)

logger = get_logger(__name__)


@app.route('/api/v1/ocr', methods=['POST'])
def do_search_api():
    output = {"nothing": "nothing"}
    args = reqparse.RequestParser(). \
        add_argument("urls", type=str). \
        add_argument("base64", type=str). \
        parse_args()
    if "urls" in args.keys():
        urls = args['urls']
        output = get_ocr_answer(urls=urls)
    if "base64" in args.keys():
        base64 = args['base64']
        output = get_ocr_answer(image_base64=base64)

    return jsonify({"output": output})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2020)
