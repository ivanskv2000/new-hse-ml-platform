from flask import Flask

import os
import yaml
import sqlite3
from sqlite3 import Error

from database.flask_database import db
from database.ml_model import Models
from database.executions import Executions
from configs.config import PATH_TO_MODELS_DIR, PATH_TO_EXEC_DIR, PATH_TO_PROJ_ROOT
from routes import model_execution
from routes import execution_initialization
from routes import debug

DB_FILE = os.path.join(PATH_TO_PROJ_ROOT, "sqlite.db")


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + DB_FILE
    db.init_app(app)

    with app.app_context():
        db.drop_all()
        db.create_all()

    app.register_blueprint(model_execution)
    app.register_blueprint(execution_initialization)
    app.register_blueprint(debug)

    return app


def populate_models(models_directory):
    model_dirs = [i for i in os.listdir(models_directory) if not i.startswith(".")]

    for md in model_dirs:
        config_path = os.path.join(models_directory, md, "config.yaml")
        print(md)
        with open(config_path, "r") as file:
            model_config = yaml.safe_load(file)
        model_db_object = Models(
            name=model_config["name"],
            tech_name=model_config["tech_name"],
            description=model_config["description"],
            task_type=model_config["task_type"],
            task_class=model_config["task_class"],
            data_type=model_config["data_type"],
            has_explanation=model_config["has_explanation"],
            port=5430,
        )
        with app.app_context():
            db.session.add(model_db_object)
            db.session.commit()


if __name__ == "__main__":
    # create_connection(DB_FILE)
    app = create_app()
    populate_models(PATH_TO_MODELS_DIR)
    app.run(host="0.0.0.0", port=os.environ["PORT"], debug=False)
