import codecs

import serial


class Sim800L:

    def __init__(self, connection='/dev/ttyAMA0'):
        self.serial_connection = serial.Serial(connection, baudrate=9600, timeout=1)
        self.intialization()

    def intialization(self):
        self.command('AT\n')

    def command(self, cmd):
        self.serial_connection.write(codecs.encode(cmd))
        rcv = self.serial_connection.readline()
        print(codecs.decode(rcv))


if __name__ == '__main__':
    gsm_con = Sim800L()
