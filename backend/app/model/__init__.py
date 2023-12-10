from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

# Initializing the SQLAlchemy extension to perform MySQL 
# operations from within our flask application.
db = SQLAlchemy()

# Here, we have defined an abstract class for all of our 
# backend based models to include common fields within their schemas.
# Along with that a flexibility to add custom common methods for each model 
# class included in our flask backend application.
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