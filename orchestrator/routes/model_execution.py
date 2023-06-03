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


model_execution = Blueprint("model_execution", __name__)


@model_execution.route("/model/infer")
def get_models():
    ml_models_in_db = Models.query.all()
    ml_models_in_db = [sql_query_to_dict(i) for i in ml_models_in_db]
    return {'ml_models_in_db': ml_models_in_db}