from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from main import app
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', dest='port', type=int,
            help='The port to serve on')

    args = parser.parse_args()

    if args.port:
        port = args.port
    else:
        port = 5000

    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(port)

    try:
        IOLoop.instance().start()
    except KeyboardInterrupt:
        IOLoop.instance().stop()

if __name__ == "__main__":
    main()
