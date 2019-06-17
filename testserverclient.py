#! /usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket
import json
import tornado.gen
import datetime


import time

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    
    def simple_init(self):
        self.last = time.time()
        self.stop = False

    def open(self):
        self.simple_init()
        print("New client connected")
        self.write_message("You are connected")
        
        tornado.ioloop.IOLoop.instance().add_timeout(datetime.timedelta(seconds=0), self.test)       

    def on_message(self, message):
        self.write_message(u"You said: " + message)
        self.last = time.time()

    def on_close(self):
        print("Client disconnected")
        
    def check_origin(self, origin):
        return True
    def test(self):
        self.write_message("heelooo aa")
        tornado.ioloop.IOLoop.instance().add_timeout(datetime.timedelta(seconds=0.05), self.test)
        
        


    def check_ten_seconds(self):
        print("Just checking")
        if (time.time() - self.last > 10):
            self.write_message("You sleeping mate?")
            self.last = time.time()

application = tornado.web.Application([
        (r"/ws", WebSocketHandler),
])




if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8000, address= '127.0.0.1')
    myIP = socket.gethostbyname(socket.gethostname())
    print( '*** Websocket Server Started at %s***' % myIP)

    tornado.ioloop.IOLoop.instance().start()
    #tornado.ioloop.IOLoop.run_in_executor(,application.write_message())
