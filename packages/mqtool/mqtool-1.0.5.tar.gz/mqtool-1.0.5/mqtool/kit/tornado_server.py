#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : tornado_server.py
# @Desc  :  tornado  service
import json

import tornado.web
import tornado.ioloop

from mqtool.utils import logger


class Tornado_http:

    def __init__(self, port=8888):

        self.port = port
        self.handlers = []
        # self.executor = ThreadPoolExecutor(max_workers=1)

    def set_port(self, port):
        self.port = port

    # 添加路由
    def add_handler(self, handler_addr, re_fun, *args, json_type=False, post=True, get=True):
        """
        :param handler_addr: 路由地址
        :param re_fun: 视图函数
        :param args: 路由参数
        :return:
          """

        class handlername(tornado.web.RequestHandler):
            def get(self):
                if not get:
                    raise tornado.web.HTTPError(500)
                argsl = []
                for arg in args:
                    argsl.append(self.get_query_argument(arg))
                try:
                    res = re_fun(*argsl)
                    logger.info("res:" + str(res))
                    if res is None:
                        self.write({"algorithm":"nodata"})
                    elif isinstance(res, list):
                        self.set_header("Content-Type", "application/json; charset=UTF-8")
                        self.write(json.dumps(res,ensure_ascii=False))
                    elif isinstance(res, dict):
                        self.set_header("Content-Type", "application/json; charset=UTF-8")
                        self.write(json.dumps(res, ensure_ascii=False))
                    else:
                        self.write(res)
                except:
                    logger.exception("algorithm error")
                    self.write({"algorithm":"error"})

            def post(self):
                if not post:
                    raise tornado.web.HTTPError(500)
                try:
                    if json_type:
                        data = json.loads(self.request.body.decode('utf-8'))
                        res = re_fun(data)
                    else:
                        argsl = []
                        for arg in args:
                            argsl.append(self.get_argument(arg))
                        res = re_fun(*argsl)
                    logger.info("res:" + str(res))
                    if res is None:
                        self.write({"algorithm":"nodata"})
                    elif isinstance(res, list):
                        self.set_header("Content-Type", "application/json; charset=UTF-8")
                        self.write(json.dumps(res, ensure_ascii=False))
                    elif isinstance(res, dict):
                        self.set_header("Content-Type", "application/json; charset=UTF-8")
                        self.write(json.dumps(res, ensure_ascii=False))
                    else:
                        self.write(res)
                except:
                    logger.exception("algorithm error")
                    self.write({"algorithm":"error"})
        self.handlers.append((handler_addr, handlername))

    # 开启 tornado 服务
    def start_http_server(self):
        app = tornado.web.Application(self.handlers)
        app.listen(port=self.port, address="0.0.0.0")
        # 启动web程序，开始监听端口的连接
        # self.executor.submit(tornado.ioloop.IOLoop.current().start)
        logger.info("service start")
        tornado.ioloop.IOLoop.current().start()
