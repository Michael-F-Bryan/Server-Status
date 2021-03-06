#!/usr/bin/env python3
import sys
import json
import argparse
import subprocess
import datetime
import platform
from urllib.request import urlopen
import socket
from collections import namedtuple
from threading import Thread
import time

from flask import Flask, render_template, request, make_response
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
import psutil

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)


class Cacher:
    def __init__(self, delay=5*60, resolution=0.25):
        self.delay = delay
        self.resolution = resolution
        self.active = False
        self.thread = None

        self.int_ip = None
        self.ext_ip = None
        self.country = 'Dunno Yet'

    def start(self):
        app.logger.info('Cacher started')

        self.active = True
        self.thread = Thread(target=self._run)
        self.thread.start()

    def _run(self):
        self.last_run = 0

        while self.active:
            if time.time() - self.last_run > self.delay:
                self.get_ip()
                self.last_run = time.time()
            else:
                time.sleep(1)

    def stop(self):
        app.logger.info('Cacher stopped')

        self.active = False

        if self.thread:
            self.thread.join()

    def get_ip(self):
        app.logger.info('Getting IP addresses')

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("gmail.com",80))
        self.int_ip = s.getsockname()[0]
        s.close()

        ip_data = urlopen('http://www.trackip.net/ip?json').read().decode('utf-8')
        ip_data = json.loads(ip_data)
        self.ext_ip = ip_data['ip']
        self.country = ip_data['country']



suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
def humansize(nbytes):
    if nbytes == 0: return '0 B'
    i = 0
    while nbytes >= 1024 and i < len(suffixes)-1:
        nbytes /= 1024.
        i += 1
    f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])


def get_uptime():
    uptime = subprocess.Popen(['uptime'], 
            stdout=subprocess.PIPE, shell=True).stdout.read().decode('utf-8')
    return uptime


def parse_processes():
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

        cmd = ' '.join(process.cmdline())
        cmd = cmd if len(cmd) < 60 else process.cmdline()[0]

        new_ps = Process(
                pid=process.pid,
                user=process.username(),
                command=cmd,
                number_of_threads=process.num_threads(),
                percent_cpu=process.cpu_percent(),
                percent_memory=str(round(process.memory_percent(), 2))+'%',
                start=create_time,
                name=process.name(),
        )
        ps.append(new_ps)

    # Sort by % memory usage, descending order
    ps.sort(key=lambda x: x.percent_memory, reverse=True)

    return ps

def filesystem_usage():
    df = subprocess.Popen(['df', '/'], stdout=subprocess.PIPE)
    output = df.stdout.read().decode('utf-8')
    output = output.split("\n")[1].split()
    size, used, available, percent, mountpoint = [int(x) for x in
    output[1:-2]] + output[-2:]

    Usage = namedtuple('Usage', ['used', 'available', 'percent'])
    usage = Usage('{:.1f}'.format(used/10e5), 
                  '{:.1f}'.format((used + available)/10e5), 
                  '{:.1f}'.format(100*used/(used + available)))
    return usage


@app.route('/')
def homepage():
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

    response = make_response(render_template('home.html',
        box_name=box_name,
        release=release,
        system=system,
        int_ip=cache.int_ip,
        ext_ip=cache.ext_ip,
        country=cache.country,
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


@app.route('/processes')
def processes():
    ps = parse_processes()

    response = make_response(render_template('processes.html',
        processes=ps,
    ))

    return response


cache = Cacher()
cache.start()


if __name__ == "__main__":
    manager.run()
