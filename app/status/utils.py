import json
import argparse
import subprocess
import datetime
import platform
from urllib.request import urlopen
import socket 
from collections import namedtuple
import time
import psutil


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

def local_ip():
    cmd = "ip route get 1 | awk '{print $NF;exit}'"
    df = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
    output = df.stdout.read().decode('utf-8').strip()
    return output

def external_ip():
    cmd = "dig +short myip.opendns.com @resolver1.opendns.com"
    df = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
    output = df.stdout.read().decode('utf-8').strip()
    return output


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


def get_who():
    Who = namedtuple('Who', ['user', 'tty', 'from_', 'login', 'idle', 'what'])
    cmd = ['w', '-i']

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    output = proc.stdout.read().decode('utf-8').strip()
    output = [line.split(maxsplit=8) for line in output.split('\n')[1:]]

    who_list = []
    for line in output:
        temp = Who(
                user=line[0],
                tty=line[1],
                from_=line[2],
                login=line[3],
                idle=line[4],
                what=line[-1])
        who_list.append(temp)

    return who_list
