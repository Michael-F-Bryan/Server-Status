from datetime import datetime
from flask import (render_template, session, redirect, url_for, request, 
        flash, request)
from flask.ext.login import current_user
import requests
from bs4 import BeautifulSoup

from . import main
# from .forms import NameForm
from .. import db
from ..models import User 


@main.route('/', methods=['GET'])
def homepage():
    if not current_user.is_authenticated:
        ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        troll = lookup_ip(ip)
    else:
        troll = dict(success=False)

    return render_template('homepage.html', troll=troll)



def lookup_ip(ip):
    if ip == '127.0.0.1':
        return dict(success=False)

    url = 'http://ip-api.com/json/{}'.format(ip)
    headers = {
        # 'User-Agent': 'Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405'
            }

    r = requests.get(url, headers=headers)
    return r.json()


