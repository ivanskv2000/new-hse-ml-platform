from database.flask_database import db
from sqlalchemy_utils import UUIDType
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func
import uuid


class Executions(db.Model):
    __tablename__ = "executions"

    id = db.Column(db.String(50), primary_key=True)
    model_id = mapped_column(ForeignKey("models.id"))  # db.Column(db.String(50))
    state = db.Column(db.String(16))
    user = db.Column(db.String(256))
    datetime = db.Column(db.DateTime, nullable=False, server_default=func.now())
    log = db.Column(db.String(50))
    type = db.Column(db.String(50))
