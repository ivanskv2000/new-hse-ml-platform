from database.flask_database import db


class Models(db.Model):
    __tablename__ = "models"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_type = db.Column(db.String(50))
    task_class = db.Column(db.String(50))
    name = db.Column(db.String(50))
    tech_name = db.Column(db.String(50))
    data_type = db.Column(db.String(50))
    description = db.Column(db.String(50))
    has_explanation = db.Column(db.Boolean())
    port = db.Column(db.Integer())
