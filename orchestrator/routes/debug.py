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


debug = Blueprint("debug", __name__)


def sql_query_to_dict(model):
    return {k: v for k, v in model.__dict__.items() if not k.startswith("_")}


@debug.route("/debug/get_models")
def get_models():
    ml_models_in_db = Models.query.all()
    ml_models_in_db = [sql_query_to_dict(i) for i in ml_models_in_db]
    return {"ml_models_in_db": ml_models_in_db}


@debug.route("/debug/get_executions")
def get_executions():
    execs_in_db = Executions.query.all()
    execs_in_db = [sql_query_to_dict(i) for i in execs_in_db]
    return {"execs_in_db": execs_in_db}


@debug.route("/debug/get_environ")
def get_env_variables():
    return {"env": list(os.environ)}
