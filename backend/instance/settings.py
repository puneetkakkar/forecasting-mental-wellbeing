import os

# Here we assign all the environment variables to a 
# python file which is recognised by flask to perform 
# various configurable operations throughout our flask 
# backend application.

SECRET_KEY=os.environ['SECRET_KEY']
DB_USERNAME=os.environ['DB_USERNAME']
DB_PASSWORD=os.environ['DB_PASSWORD']
DB_HOST=os.environ['DB_HOST']
DATABASE_NAME=os.environ['DATABASE_NAME']
DB_URI = "mysql+pymysql://%s:%s@%s:3306/%s" % (DB_USERNAME, DB_PASSWORD, DB_HOST, DATABASE_NAME)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True
MYSQL_ROOT_PASSWORD=os.environ['MYSQL_ROOT_PASSWORD']
