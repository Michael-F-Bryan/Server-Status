from datetime import datetime
from flask import render_template, session, redirect, url_for, request, flash
from flask.ext.login import current_user

from . import main
# from .forms import NameForm
from .. import db
from ..models import User 



@main.route('/', methods=['GET'])
def homepage():
    return render_template('homepage.html')

