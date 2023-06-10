from flask import Blueprint
from database.ml_model import Models
from database.executions import Executions
import requests

import sys
sys.path.append("..")


model_execution = Blueprint("model_execution", __name__)


@model_execution.route("/inference/<string:exec_id>")
def infer_execution(exec_id):
    exec_model_id = Executions.query.filter_by(id=exec_id).first().model_id
    exec_model_name = Models.query.filter_by(id=exec_model_id).first().tech_name
    inference_api_call = f"http://{exec_model_name}:5430/infer/{exec_id}"
    _ = requests.get(url=inference_api_call)
    return {"state": "success"}


@model_execution.route("/explanation/<string:exec_id>")
def explain_execution(exec_id):
    exec_model_id = Executions.query.filter_by(id=exec_id).first().model_id
    exec_model_name = Models.query.filter_by(id=exec_model_id).first().tech_name
    inference_api_call = f"http://{exec_model_name}:5430/explain/{exec_id}"
    _ = requests.get(url=inference_api_call)
    return {"state": "success"}
