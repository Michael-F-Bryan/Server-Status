=============
Status Server
=============

Description
-----------

A simple flask HTTP server that will tell you the status of your box.

It's simple, but I've found this small web app to be incredibly useful when I'm
using a headless computer to host websites, databases, backups, dns servers or
any other services I might use around the place. There's nothing like the
convenience of being able to see a brief overview of how a computer is going
without needing to SSH or remote desktop in.

Features
--------
It incorporates the following:
  * Authentication (so not just *anyone* can check out your box)
  * General overview (basically a bunch of random stats on a page)
  * Processes (think windows task manager)
  * Current users and what they're doing
  * A file sharing section to upload and download files from a specific
    directory.

Installation
------------
No installation is really required in order to start using the status server.
Simply clone the repository, install the dependencies (may require sudo), then 
run the server using the `manage.py` file.

::

    git clone https://github.com/Michael-F-Bryan/status_server.git
    python3 setup.py install
    python3 manage.py runserver --host 0.0.0.0 --port 8080

In order to run the server in the background as a daemon, it is recommended to
use a proper WSGI server like gunicorn. Run gunicorn with::

    gunicorn --bind 0.0.0.0:8080 --daemon manage:app

You can add extra parameters to gunicorn to activate extra features. For the
full configuration details, consult the `gunicorn documentation
<http://gunicorn-docs.readthedocs.org/en/latest/settings.html>`_.
