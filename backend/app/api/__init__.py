from flask import Blueprint

__package__ = "api"

api = Blueprint("api", __name__, url_prefix="/api")