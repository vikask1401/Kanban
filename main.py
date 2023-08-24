import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


current_dir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(current_dir, "application/data/kanban.db")
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()
app.secret_key = "07-05-2003"

from application.controller.controllers import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

