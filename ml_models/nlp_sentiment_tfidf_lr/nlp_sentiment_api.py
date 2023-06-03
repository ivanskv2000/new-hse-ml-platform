from flask import Flask
from flask_restx import Resource, Api
from artifacts.sentiment.sentiment import run_inference_pipeline, explain_lime
import os

MODEL_DIR = '.'
EXECUTIONS_DIR = '../executions'
supported_methods = ['infer', 'explain']

app = Flask(__name__)
api = Api(
    app,
    title="nlp_sentiment_tfidf_lr",
    version="1.0",
    description="TBC"
    )


@api.route('/methods')
class ApiMethods(Resource):
    def get(self):
        return {'methods': supported_methods}


@api.route('/infer/<string:exec_id>')
class ModelInference(Resource):
    def get(self, exec_id):
        path_to_model_dir = MODEL_DIR
        data_input_path = os.path.join(EXECUTIONS_DIR, exec_id)
        data_output_path = data_input_path

        run_inference_pipeline(data_input_path, data_output_path, path_to_model_dir)

        return {'exec_id': exec_id, 'status': 'finished', 'output': data_output_path}


@api.route('/explain/<string:exec_id>')
class InferenceExplanation(Resource):
    def get(self, exec_id):
        path_to_model_dir = MODEL_DIR
        data_input_path = os.path.join(EXECUTIONS_DIR, exec_id)
        explanation_output_path = os.path.join(data_input_path, 'explanation')

        explain_lime(data_input_path, explanation_output_path, path_to_model_dir, idx=None)

        return {'exec_id': exec_id, 'status': 'explained', 'output': explanation_output_path}


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5430, debug=False)
