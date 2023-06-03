import os
import json
import uuid

from flask import Blueprint

import sys
sys.path.append("..")

from database.flask_database import db
from database.ml_model import Models
from database.executions import Executions
from configs import PATH_TO_PROJ_ROOT
from sqlalchemy.sql import select

import requests


model_execution = Blueprint("model_execution", __name__)


@model_execution.route("/inference/<string:exec_id>")
def infer_execution(exec_id):
    exec_model_id = Executions.query.filter_by(id=exec_id).first().model_id
    exec_model_name = Models.query.filter_by(id=exec_model_id).first().tech_name
    inference_api_call = f"http://{exec_model_name}:5430/infer/{exec_id}"
    response = requests.get(url=inference_api_call)
    return {'state': 'success'}


@model_execution.route("/explanation/<string:exec_id>")
def explain_execution(exec_id):
    exec_model_id = Executions.query.filter_by(id=exec_id).first().model_id
    exec_model_name = Models.query.filter_by(id=exec_model_id).first().tech_name
    inference_api_call = f"http://{exec_model_name}:5430/explain/{exec_id}"
    response = requests.get(url=inference_api_call)
    return {'state': 'success'}
