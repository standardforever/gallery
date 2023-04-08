#!/usr/bin/env python3

from flask import Flask
from decouple import config
from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class
import os
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SECRET_KEY'] = config("SECRET_KEY")
bcrypt = Bcrypt(app)

# configure for app upload
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)




# configure the SQLite database, relative to the app instance folder
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'

# create the extension
db = SQLAlchemy(app)
# db.init_app(app)

from app.home.routes import *
from app.admin.routes import *
