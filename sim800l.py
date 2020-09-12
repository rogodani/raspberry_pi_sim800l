import codecs

import serial


class Sim800L:

    def __init__(self, connection='/dev/ttyAMA0'):
        self.serial_connection = serial.Serial(connection, baudrate=9600, timeout=1)
        self.initialization()

    def initialization(self):
        self.command('AT\n')
        self.command('ATE0\n')  # Set Command Echo Mode Off
        self.command('ATI\n')  # Display Product Identification Information
        self.command('AT&V\n')  # Display Current Configuration
        self.command('AT+GSN\n')  # Request TA Serial Number Identification(IMEI)
        # AT+CPBR=? Read Current Phonebook Entries
        self.command('AT+COPS?\n')  # Currently Selected Operator
        self.command('AT+CSQ\n')  # Signal Quality Report
        self.command('AT+CNUM\n')  # Subscriber Number
        self.command('AT+CMGF=1\n')  # Select SMS Message Format: Text mode

    def command(self, cmd):
        self.serial_connection.write(codecs.encode(cmd))
        rcv = self.serial_connection.readline()
        # print(f'{cmd}:{codecs.decode(rcv)}')
        print('{0}:{1}'.format(cmd, codecs.decode(rcv)))

    def check_incoming(self):
        if self.serial_connection.in_waiting:
            rcv = self.serial_connection.readline()
            print(rcv)
            # buf = convert_to_string(buf)
            rcv = codecs.decode(rcv)
            print(rcv)
            # params = buf.split(',')
            #
            # if params[0][0:5] == "+CMTI":
            #     self._msgid = int(params[1])
            #     if self.msg_action:
            #         self.msg_action()
            #
            # elif params[0] == "NO CARRIER":
            #     self.no_carrier_action()
            #
            # elif params[0] == "RING" or params[0][0:5] == "+CLIP":
            #     # @todo handle
            #     pass


if __name__ == '__main__':
    gsm_con = Sim800L()
    while True:
        gsm_con.check_incoming()
