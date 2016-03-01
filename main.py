import json
import subprocess
import datetime
import platform
from urllib.request import urlopen
import socket
from collections import namedtuple

from flask import Flask, render_template, request, make_response
import psutil

app = Flask(__name__)


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("gmail.com",80))
    int_ip = s.getsockname()[0]
    s.close()

    ip_data = urlopen('http://www.trackip.net/ip?json').read().decode('utf-8')
    ip_data = json.loads(ip_data)
    ext_ip = ip_data['ip']
    country = ip_data['country']

    return int_ip, ext_ip, country


def processes():
    Process = namedtuple('Process', [
        'pid', 
        'user', 
        'number_of_threads',
        'percent_cpu', 
        'percent_memory', 
        'start',
        'name',
        'command', 
        ]
    )
    processes = psutil.process_iter()

    ps = []

    for process in processes:
        if process.username() == 'root':
            continue

        create_time = datetime.datetime.fromtimestamp(process.create_time()).strftime(
                "%Y-%m-%d %H:%M:%S")

        new_ps = Process(
                pid=process.pid,
                user=process.username(),
                command=' '.join(process.cmdline()),
                number_of_threads=process.num_threads(),
                percent_cpu=process.cpu_percent(),
                percent_memory=round(100*process.memory_percent(),2),
                start=create_time,
                name=process.name(),
        )
        ps.append(new_ps)

    # Sort by % memory usage, descending order
    ps.sort(key=lambda x: x.percent_memory, reverse=True)

    return ps



@app.route('/')
def root():
    box_name = platform.node()
    release = platform.release()
    system = platform.system()
    int_ip, ext_ip, country =  get_ip()
    ps = processes()

    response = make_response(render_template('status.html',
        box_name=box_name,
        release=release,
        system=system,
        int_ip=int_ip,
        ext_ip=ext_ip,
        country=country,
        now=datetime.datetime.now().strftime('%X %x'),
        processes=ps,
    ))
    return response


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
