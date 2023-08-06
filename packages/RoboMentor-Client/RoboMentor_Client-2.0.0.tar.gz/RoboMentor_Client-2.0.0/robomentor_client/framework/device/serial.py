import serial
from ..log import Log

class Serial:

    def __init__(self, port, baudrate, size):
        self.conn = serial.Serial()
        self.conn.port = port
        self.conn.baudrate = baudrate
        self.conn.bytesize = size
        self.conn.stopbits = serial.STOPBITS_ONE
        self.conn.parity = serial.PARITY_NONE
        self.conn.timeout = 0.2
        self.conn.open()

    def write(self, command):
        try:
            self.conn.write(command)
        except Exception as e:
            Log.error(e)

    def read(self):
        read_data = self.conn.readall()
        return read_data.decode('utf-8')

    def close(self):
        self.conn.close()