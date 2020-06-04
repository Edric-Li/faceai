#!/usr/bin/python
# -*- coding: utf-8 -*-
# 项目入口

from flask import Flask
from routes import PostRouter, GETRouter
from config.index import Config
from gevent.pywsgi import WSGIServer
from utils.logs import logger


app = Flask(__name__)


@app.route("/")
def welcome():
    return app.send_static_file('index.html')


@app.route('/<url>', methods=['GET'])
def get_router(url):
    return GETRouter.redirect(url=url)


@app.route('/<url>', methods=['POST'])
def post_router(url):
    return PostRouter.redirect(url=url)


if __name__ == '__main__':
    if Config().env_name == 'production':
        logger.info('Service starting......')
        http_server = WSGIServer(('', 6013), app)
        http_server.serve_forever()
        logger.info('Service started successfully.')
    else:
        app.run(
            host='0.0.0.0',
            port=6013,
        )
