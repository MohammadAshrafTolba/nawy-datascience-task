import secrets
from flask import Flask, request, jsonify
from flask_api.flask_utils import parse_objects_to_json
from core_modules.classifier import Classifier

classifier = Classifier()


# init flask app
app = Flask(__name__)

app.route('/classify_lead', methods=['POST'])
def func_2():
    body = request.json
    body = parse_objects_to_json(body)
    lead_info_dict = body['lead_info']
    # not finished yet
    # pred = classifier.classify_instance(lead_info_dict)
    # return jsonify({'prediction': pred})
    pass

if __name__ == '__main__':
    app.secret_key = secrets.token_urlsafe(24)
    app.run(debug=True, host='0.0.0.0', port=3000)
