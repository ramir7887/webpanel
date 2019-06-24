# -*- coding: utf-8 -*-
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket
import json
import datetime

# import linuxcnc

# КЛАСС ПАРСИНГА КОМАНД
class Command:
    # c = linuxcnc.coomand()
    # s = linuxcnc.state()
    def parse_message(self, message):  # Парсит пришедшее от клиента сообщение и вызывает соответствующую функцию
        js = json.loads(message)
        mes = dict(js)
        self.dict_command[mes['action']](mes['parameters'])

    def move_axis(self, parameters):
        axis = int(parameters['axis'])
        velocity = int(parameters['jog_speed']) * int(parameters['velocity_vector'])
        if parameters['step'] == 'Continuous':
            print('Перемещение оси: ', axis, '\nСкорость:', velocity)
            # self.c.jog(linuxcnc.JOG_CONTINUOUS, axis, velocity)
        else:
            distance = float(parameters['step'])
            print('Перемещение оси: ', axis, '\nСкорость:', velocity, '\nИнеремент:', distance)
            # self.c.jog(linuxcnc.JOG_INCREMENT, parameters['axis'], velocity, distance)

    def home_all(self, parameters):
        # сдедать так что бы сначала Z в ноль приезжала, затем Y, затем X
        #self.c.home(2)
        #self.c.home(1)
        #self.c.home(0)
        print('Ось Z едет домой.')
        print('Ось Y едет домой.')
        print('Ось X едет домой.')

    def home_axis(self, parameters):
        # сделать такое, что можно отдельную ось хомить
        # self.c.home(parameters['axis'])
        print('Ось {0} едет домой'.format(parameters['axis']))

    def stop_axis(self, parameters):
        # вызывается при поднятии кнопки мыши отвечающей за ось
        # self.c.jog(linuxcnc.JOG_STOP, parameters['axis'])
        print('Ось {0} остановлена'.format(parameters['axis']))

    def jog_on(self, parameters):
        # включает JOG режим
        # self.c.mode()
        pass

    def spindle(self, parameters):
        pass

    def mdi_on(self, parameters):
        pass

    def send_command(self, parameters):
        pass

    def auto_on(self, parameters):
        pass

    dict_command = {'move_axis': move_axis,
                    'home_all': home_all,
                    'home_axis': home_axis,
                    'stop_axis': stop_axis,
                    'jog_on': jog_on,
                    'spindle': spindle,
                    'mdi_on': mdi_on,
                    'send_command': send_command,
                    'auto_on': auto_on
                    }

clients = [] # Список для клиентов подключающихся к серверу

# КЛАСС ВЕБ-СОКЕТА
class WebSocketHandler(tornado.websocket.WebSocketHandler):

    command = Command()  # Создание обработчика команд

    def open(self):
        clients.append(self)
        self.write_message('connected')
        print('===============\nnew conection\n===============')
        # tornado.ioloop.IOLoop.instance().add_timeout(datetime.timedelta(seconds=0),self.send_info) # старый способ

    def on_message(self, message):
        self.command.parse_message(message)
        print(message)

    def on_close(self):
        self.write_message('disconnected')
        clients.remove(self)
        print ('===============\nconnection closed\n===============')
        def check_origin(self, origin):
            return True

    def send_info(self):
        self.write_message('Отправляю информации о работе станка клиенту!')
        # tornado.ioloop.IOLoop.instance().add_timeout(datetime.timedelta(seconds=0.01), self.send_info) # старый способ


# application = tornado.web.Application([(r"/ws", WebSocketHandler),])
application = tornado.web.Application([
        (r"/ws", WebSocketHandler),
])


def send_info():
    """
    send_info() пробегается по массиву подключенных клиентов и отправляет информацию о работе оборудования
    """
    if clients:
        for client in clients:
            client.write_message("heelooo aa")


if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8001, address="127.0.0.1")  # задается адрес и порт сервера
    print('*** Websocket Server Started ***')
    loop = tornado.ioloop.IOLoop.instance()
    period = tornado.ioloop.PeriodicCallback(send_info, 10)
    period.start()
    loop.start()
