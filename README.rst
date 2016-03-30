=============
Status Server
=============

A simple flask HTTP server that will tell you the status of your box.

It incorporates the following:
  * Authentication (so not just *anyone* can check out your box)
  * General overview (basically a bunch of random stats on a page)
  * Processes (think windows task manager)
  * Current users and what they're doing
  * A file sharing section to upload and download files from a specific
    directory.

It's simple, but I've found this small web app to be incredibly useful when I'm
using a headless computer to host websites, databases, backups, dns servers or
any other services I might use around the place. There's nothing like the
convenience of being able to see a brief overview of how a computer is going
without needing to SSH or remote desktop in.

