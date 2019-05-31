#! /usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket
import json
'''
This is a simple Websocket Echo server that uses the Tornado websocket handler.
Please run `pip install tornado` with python of version 2.7.9 or greater to install tornado.
This program will echo back the reverse of whatever it recieves.
Messages are output to the terminal for debuggin purposes. 

({axis: '0', velocityvektor:"-1", button: 'bty', action: 'buttondown',
 VM: velocity.value, step: step.value}


''' 



import linuxcnc


class Command :

    c = linuxcnc.command()

    def parseJog(self,mes):
        print (mes)
        print(mes["action"])
        if mes["action"] == "buttondown":
            if mes['axis'] !='stop':
                c.jog(linuxcnc.JOG_CONTINUOUS, int(mes['axis']), int(mes['velocityvektor'])*int(mes['VM']))
            else:
                c.jog(linuxcnc.JOG_CONTINUOUS,0,0)
                c.jog(linuxcnc.JOG_CONTINUOUS,1,0)
                c.jog(linuxcnc.JOG_CONTINUOUS,2,0)
        if mes['action'] == 'buttonup':
            if mes['axis'] != 'stop':
                c.jog(linuxcnc.JOG_CONTINUOUS,int(mes['axis']),0)
            else:
                c.jog(linuxcnc.JOG_CONTINUOUS,0,0)
                c.jog(linuxcnc.JOG_CONTINUOUS,1,0)
                c.jog(linuxcnc.JOG_CONTINUOUS,2,0)

    def parse(self,message):
        js = json.loads(message)
        mes = dict(js)   #Словарь с сообщением(командами)
        if mes['typeCommand'] == "jog":
            self.parseJog(mes)
        
        #вызывает парсер команд JOG



c =linuxcnc.command()
c.mode(linuxcnc.MODE_MANUAL)


class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print ('new connection')
    def on_message(self, message):
        print(message)
        parser = Command()
        parser.parse(message)
        print ('message received:  %s' % message)

        
 
    def on_close(self):
        print ('connection closed')
 
    def check_origin(self, origin):
        return True
 
application = tornado.web.Application([
    (r'/ws', WSHandler),
])
print(application.default_host)
 
 
if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8889, address= '192.168.100.245')
    myIP = socket.gethostbyname(socket.gethostname())
    print( '*** Websocket Server Started at %s***' % myIP)
    tornado.ioloop.IOLoop.instance().start()
