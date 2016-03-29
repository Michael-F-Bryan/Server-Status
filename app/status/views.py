from flask import (render_template, redirect, request, url_for, flash,
        current_app, make_response)
from flask.ext.login import login_required, current_user

import psutil
import platform
import datetime

from .. import db
from . import status
from .utils import (humansize, parse_processes, get_uptime, filesystem_usage,
        local_ip, external_ip)


@status.route('/', methods=['GET'])
@login_required
def overview():
    box_name = platform.node()
    release = platform.release()
    system = platform.system()
    # int_ip, ext_ip, country =  get_ip()
    now = datetime.datetime.now()
    date = now.strftime('%A %B %e, %Y')
    time = now.strftime('%l:%M:%S %p')

    # Calculate CPU and memory usage
    percent_cpu = psutil.cpu_percent()
    pc_virtual_memory = psutil.virtual_memory().percent
    virtual_memory = [psutil.virtual_memory().available, 
            psutil.virtual_memory().total]
    virtual_memory[0] = virtual_memory[1] - virtual_memory[0]
    virtual_memory = list(map(humansize, virtual_memory))

    swap_memory = psutil.swap_memory().used, psutil.swap_memory().total
    swap_memory = list(map(humansize, swap_memory))
    pc_swap_memory = psutil.swap_memory().percent

    uptime= get_uptime()

    response = make_response(render_template('status/overview.html',
        box_name=box_name,
        release=release,
        system=system,
        int_ip=local_ip(),
        ext_ip=external_ip(),
        date=date,
        time=time,
        percent_virtual_memory=pc_virtual_memory,
        virtual_memory=virtual_memory,
        percent_cpu=percent_cpu,
        swap_memory=swap_memory,
        percent_swap_memory=pc_swap_memory,
        uptime=uptime,
        fs=filesystem_usage(),
    ))
    return response

