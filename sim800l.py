import codecs
from time import sleep

import serial


def decode_to_string(rcv):
    return codecs.decode(rcv)


class Sim800L:

    def __init__(self, connection='/dev/ttyAMA0'):
        self.serial_connection = serial.Serial(connection, baudrate=9600, timeout=1)
        self.initialization()

    def initialization(self):
        self.command('AT\n')
        self.command('ATE0\n')  # Set Command Echo Mode Off
        self.command('AT+CSCLK=0\n')  # Disabel Slow Clock
        self.command('ATI\n')  # Display Product Identification Information
        # self.command('AT&V\n')  # Display Current Configuration
        self.command('AT+GSN\n')  # Request TA Serial Number Identification(IMEI)
        # AT+CPBR=? Read Current Phonebook Entries
        self.command('AT+COPS?\n')  # Currently Selected Operator
        self.command('AT+CSQ\n')  # Signal Quality Report
        self.command('AT+CNUM\n')  # Subscriber Number
        self.command('AT+CMGF=1\n')  # Select SMS Message Format: Text mode

    def command(self, cmd):
        self.serial_connection.write(codecs.encode(cmd))
        rcv = self.serial_connection.readline()
        print('{0}:{1}'.format(cmd, decode_to_string(rcv)))
        sleep(1)

    def check_incoming(self):
        # self.serial_connection.reset_output_buffer()
        if self.serial_connection.in_waiting:
            print('-><-' * 30)
            rcv = self.serial_connection.readline()
            print(rcv)
            # buf = convert_to_string(buf)
            rcv = decode_to_string(rcv)
            print(rcv)
            params = rcv.split(',')
            print('PARAMS: ', params)

            if params[0] == "RING" or params[0][0:5] == "+CLIP":
                phone_number = params[0].strip().split(':')[1]
                sleep(1)
                self.command('ATH\n')
                sleep(1)
                return phone_number


if __name__ == '__main__':
    gsm_con = Sim800L()
    while True:
        incoming = gsm_con.check_incoming()

        if incoming and ('0743144113' in incoming):
            print('$' * 20, '\nCALL FROM {}\n'.format(incoming), '$' * 20)
