from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()

class AppModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    create_datetime = db.Column(db.DateTime, default=func.now())
    update_datetime = db.Column(db.DateTime, default=func.now())

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        pass