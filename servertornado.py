#! /usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket
import json
import datetime
'''
This is a simple Websocket Echo server that uses the Tornado websocket handler.
Please run `pip install tornado` with python of version 2.7.9 or greater to install tornado.
This program will echo back the reverse of whatever it recieves.
Messages are output to the terminal for debuggin purposes. 

({axis: '0', velocityvektor:"-1", button: 'bty', action: 'buttondown',
 VM: velocity.value, step: step.value}
##########################################################################
##########################################################################
#   Переписать в соответсвии с новым форматом сообщений
#
##########################################################################
##########################################################################


##########################################################################
##########################################################################
#   Класс Command отвечает за парсинг сообщений от клиента.
#   Метод parse() вызывает парсер параметров для конкретного режима(JOG,MDI,AUTO)
#   Нужно подумать как это сделать лучше: 
#       1 - оставить так и множество условий выбора для каждого отдельного режима
#       2 - организовать вызов с помощью хеш-таблиц (dict), в которых будут лежать
#           функции
#   Вынести класс Command в отдельный модуль.
#   Подумать про отправку сообщений от сервера клиенту
#   Составить единый формат сообщений для передачи клиент-сервер и сервер-клиент
#   В уже реализованный парсинг JOG режима добавить  зависимость от параметров(maxVelocity, Step)
#   В JOG проверить соответствие кнопок и направлений движения при нажатии
##########################################################################
##########################################################################
''' 



#import linuxcnc


class Command :

    #c = linuxcnc.command()

    def parseJog(self,mes):
        print (mes)
        print(mes["action"])
        if mes["action"] == "buttondown":
            if mes['axis'] !='stop':
                print('отработал')
                #c.jog(linuxcnc.JOG_CONTINUOUS, int(mes['axis']), int(mes['velocityvektor'])*int(mes['VM']))
            else:
                print('отработал')
                #c.jog(linuxcnc.JOG_CONTINUOUS,0,0)
                #c.jog(linuxcnc.JOG_CONTINUOUS,1,0)
                #c.jog(linuxcnc.JOG_CONTINUOUS,2,0)
        if mes['action'] == 'buttonup':
            if mes['axis'] != 'stop':
                print('отработал')
                #c.jog(linuxcnc.JOG_CONTINUOUS,int(mes['axis']),0)
            else:
                print('отработал')
                #c.jog(linuxcnc.JOG_CONTINUOUS,0,0)
                #c.jog(linuxcnc.JOG_CONTINUOUS,1,0)
                #c.jog(linuxcnc.JOG_CONTINUOUS,2,0)

    def parseHome(self,mes):
        if mes['axis'] == 'all':
            print('отработал')
            #c.home(0)
		    #c.home(1)
		    #c.home(2)
    
    def parse(self,message):
        js = json.loads(message)
        mes = dict(js)   
        if mes['typeCommand'] == "jog":
            self.parseJog(mes)
        if mes['typeCommand'] == "home":
            self.parseHome(mes)

#c =linuxcnc.command()
#c.mode(linuxcnc.MODE_MANUAL)


class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print ('new connection')
    def on_message(self, message):
        print(message)
        parser = Command()
        begin = datetime.datetime.now() 
        parser.parse(message)
        end = datetime.datetime.now()
        #print(end)               # измерение времени на парсинг
        time = end.microsecond - begin.microsecond  #
        print('DELTA', time, '\n')
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
    http_server.listen(8000, address= '127.0.0.1')
    myIP = socket.gethostbyname(socket.gethostname())
    print( '*** Websocket Server Started at %s***' % myIP)
    tornado.ioloop.IOLoop.instance().start()
