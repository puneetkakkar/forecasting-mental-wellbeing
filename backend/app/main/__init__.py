from flask import Blueprint

# Here we are defining our main route, which is just for 
# checking whether our application is up and running or not.

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/index')
def index():
    return "<h1>Forecasting mental health application is running...</h1>"
