#!/usr/bin/env python
#-*- coding: utf-8 -*-

import tornado.web
import tornado.escape

class BaseHandler(tornado.web.RequestHandler):
    def response_ok(self, data = {}):
        return self.response_json('OK', data, '200')

    def response_failed(self, error_code = 500, data = {}):
        return self.response_json('FAILED', data, error_code)

    def response_json(self, status, result, error_code):
        respon = {'status':status, 'result':result, 'error_code':error_code}
        respon_json = tornado.escape.json_encode(respon)
        self.write(respon_json)
