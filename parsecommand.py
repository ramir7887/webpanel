import json
import linuxcnc

c = linuxcnc.command()
class Command :

    c = linuxcnc.command()

    def parseJog(self,mes):
        if mes['action'] == 'buttondown':
            if mes['axis'] != 'stop':
                    c.jog(linuxcnc.JOG_CONTINUOUS, int(mes['axis']), int(mes['velocityvektor'])*int(mes['VM']))
            else:
                c.jog(linuxcnc.JOG_CONTINUOUS,0,0)
                c.jog(linuxcnc.JOG_CONTINUOUS,1,0)
                c.jog(linuxcnc.JOG_CONTINUOUS,2,0)
        elif mes['action'] == 'buttonup':
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
            self.parseJog(message)
        
        #вызывает парсер команд JOG






    