from flask import Blueprint

from app.model.mental_health_dataset import MentalHealthDataset

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/index')
def index():
    data = MentalHealthDataset.query.first_or_404()
    return "<h1>Mental Health Data: " + data.country + "</h1>"
