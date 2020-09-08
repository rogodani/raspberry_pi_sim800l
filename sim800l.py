import codecs

import serial


class Sim800L:

    def __init__(self, connection='/dev/ttyAMA0'):
        self.serial_connection = serial.Serial(connection, baudrate=9600, timeout=1)
        self.initialization()

    def initialization(self):
        self.command('AT\n')
        self.command('ATE0\n')
        self.command('AT+CLIP=1\n')

    def command(self, cmd):
        self.serial_connection.write(codecs.encode(cmd))
        rcv = self.serial_connection.readline()
        print(f'{cmd}:{codecs.decode(rcv)}')


if __name__ == '__main__':
    gsm_con = Sim800L()
