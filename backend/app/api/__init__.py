from flask import Blueprint

__package__ = "api"

# Here, we initiate the registering of our /api blueprint within our flask backend application.
api = Blueprint("api", __name__, url_prefix="/api")