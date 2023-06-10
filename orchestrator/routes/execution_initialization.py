from flask import Blueprint, current_app, request
from database.flask_database import db
from database.executions import Executions
from coolname import generate_slug

import sys

sys.path.append("..")

session_name = generate_slug()
execution_initialization = Blueprint("execution_initialization", __name__)


@execution_initialization.route("/exec/init", methods=["GET", "POST"])
def init_exec():
    exec_id = request.args.get("exec_id", None)
    model_id = request.args.get("model_id", None)

    exec_db_object = Executions(
        id=str(exec_id), model_id=int(model_id), state="init", user=session_name
    )

    with current_app.app_context():
        db.session.add(exec_db_object)
        db.session.commit()

    return {"state": "success"}
