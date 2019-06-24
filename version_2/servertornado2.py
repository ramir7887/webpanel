# -*- coding: utf-8 -*-
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket
import json
import datetime
import time
# import linuxcnc

##########################################
##########################################
##      КОММЕНТАРИИ НЕ УДАЛЯТЬ!!!       ##
##########################################
##########################################

# !!!! Заменить русский текст в консоли на английский !!!!

# КЛАСС СБОРА ИНФОРМАЦИИ СО СТАНКА, УПАКОВКИ И ОТПРАКИ ДАННЫХ КЛИЕНТУ
class Information:
    # s = linuxcnc.stat()

    # возможно две функции и не нужны, сможет все делать одна.
    # этот класс может использоваться как основа для диагностической составляющей
    # (смотреть в сторону АИС Диспетчер, его функций и возможностей)
    # 

    def get_info(self):  # Функция, получающая информацию со станка
        # s.poll()
        pass
    
    def build_message(self): # Функция строит сообщение для отправки 
        self.get_info()
        

# КЛАСС ПАРСИНГА КОМАНД ОТ КЛИЕНТА
class Command:
    # c = linuxcnc.coommand()
    # s = linuxcnc.stat()
    def parse_message(self, message):  # Парсит пришедшее от клиента сообщение и вызывает соответствующую функциюs
        mes = eval(message)
        parameters = mes['parameters']
        self.dict_command[mes['action']](self,parameters)

    def move_axis(self, parameters):
        axis = int(parameters['axis'])
        velocity = int(parameters['jog_speed']) * int(parameters['velocity_vector'])
        
        if parameters['step'] == 'Continuous':
            print('Axis movement: '+ str(axis) + '\nSpeed: ' + str(velocity))
            # self.c.jog(linuxcnc.JOG_CONTINUOUS, axis, velocity)
        else:
            distance = float(parameters['step'])
            print('Axis movement: ' + str(axis) + '\nSpeed: ' + str(velocity) + '\nIncrement: ' + str(distance))
            # self.c.jog(linuxcnc.JOG_INCREMENT, parameters['axis'], velocity, distance)

    def home_all(self, parameters):
        # сдедать так что бы сначала Z в ноль приезжала, затем Y, затем X
        # self.c.home(2)
        # self.c.home(1)
        # self.c.home(0)
        if not parameters:
            print('Axis Z (2) goes home.')
            time.sleep(1)     # заменить на условие если Z  дома, то хомить Y
            print('Axis Y (1) goes home.')
            time.sleep(1)     # заменить на условие если Y  дома, то хомить X
            print('Axis X (0) goes home.')

    def home_axis(self, parameters):
        # сделать такое, что можно отдельную ось хомить
        # self.c.home(parameters['axis'])
        print('Axis {0} goes home.'.format(parameters['axis']))

    def stop_axis(self, parameters):
        # вызывается при поднятии кнопки мыши отвечающей за ось
        # self.c.jog(linuxcnc.JOG_STOP, parameters['axis'])
        print('Axis {0} stopped'.format(parameters['axis']))



    def jog_on(self, parameters):
        # включает JOG режим
        # self.c.mode()  # посмотреть, что нужно передавать в качестве аргумента
        pass

    def spindle(self, parameters):
        pass

    def mdi_on(self, parameters):
        # вставить из примера MDI
        pass

    def send_command(self, parameters):
        pass

    def auto_on(self, parameters):
        pass

    def send_file(self, parameters):
        pass

    dict_command = {'move_axis': move_axis,
                    'home_all': home_all,
                    'home_axis': home_axis,
                    'stop_axis': stop_axis,
                    'jog_on': jog_on,
                    'spindle': spindle,
                    'mdi_on': mdi_on,
                    'send_command': send_command,
                    'auto_on': auto_on,
                    'send_file': send_file
                    }

clients = [] # Список для клиентов подключающихся к серверу
command = Command()
# КЛАСС ВЕБ-СОКЕТА
class WebSocketHandler(tornado.websocket.WebSocketHandler):

    command = Command()  # Создание обработчика команд

    def open(self):
        clients.append(self)
        self.write_message('connected')
        print('===============\nnew conection\n===============')
        # tornado.ioloop.IOLoop.instance().add_timeout(datetime.timedelta(seconds=0),self.send_info) # старый способ

    def on_message(self, message):
        begin = datetime.datetime.now()             # измерение времени на парсинг
        # print(begin)

        command.parse_message(message)

        end = datetime.datetime.now()
        # print(end)               # измерение времени на парсинг
        time = end.microsecond - begin.microsecond  #
        print('DELTA', time, '\n')

    def on_close(self):
        clients.remove(self)
        print ('===============\nconnection closed\n===============')

    def check_origin(self, origin):
        return True

    def send_info(self):
        self.write_message('Отправляю информации о работе станка клиенту!')
        
        # tornado.ioloop.IOLoop.instance().add_timeout(datetime.timedelta(seconds=0.01), self.send_info) # старый способ



application = tornado.web.Application([
        (r"/ws", WebSocketHandler),
])

####################################
count = 0                          #
def counter():                     #
    global count                   #
    count = count + 1              #
    return count                   #
#################################### для счетчика отправленных с сервера сообщений, чисто для наглядности (Используется в отправке сообщений send_info() )

def send_info():
    """
    send_info() пробегается по массиву подключенных клиентов и отправляет информацию о работе оборудования
    """
    if clients:
        
        for client in clients:
            client.write_message('Отправляю информации о работе станка клиенту! Уже в {0} раз!'.format(counter()))
        
        
        
        

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8001, address="127.0.0.1")  # задается адрес и порт сервера
    print('*** Websocket Server Started ***')
    loop = tornado.ioloop.IOLoop.instance()
    period = tornado.ioloop.PeriodicCallback(send_info, 2000)
    period.start()
    loop.start()
