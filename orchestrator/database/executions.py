from database.flask_database import db
from sqlalchemy_utils import UUIDType
import uuid


class Executions(db.Model):

    __tablename__ = "executions"

    id = db.Column(db.String(50), primary_key=True)
    model_id = db.Column(db.String(50))
    state = db.Column(db.String(50))
    user = db.Column(db.String(50))
    datetime = db.Column(db.String(50))
    log = db.Column(db.String(50))
    type = db.Column(db.String(50))
