import time
import serial
from .config import Config
from .toolbox import hex_to_signed


class Microbit:
    def __init__(self, port=''):
        self.__port = port
        self.__serial = serial.Serial()
        self.__read_msg = ''
        self.__write_msg = ''

        self.leds = [[False for i in range(5)] for n in range(5)]
        self.button_a = False
        self.button_b = False
        self.button_event_a = False
        self.button_event_b = False
        self.__button_a_old = False
        self.__button_b_old = False
        self.acc_x = 0.0
        self.acc_y = 0.0
        self.acc_z = 0.0
        self.acc_x_lim_p1_m1 = 0.0
        self.acc_y_lim_p1_m1 = 0.0
        self.acc_z_lim_p1_m1 = 0.0
        self.version = 0

        self.config = Config()

        if port != '':
            self.open(self.port)

    def leds_clear_all(self):
        self.leds = [[False for i in range(5)] for n in range(5)]

    def leds_clear_all_update(self):
        self.leds_clear_all()
        self.update()

    def leds_update(self, leds):
        self.leds = leds
        self.update()

    def open(self, port='', update=True):
        if port == '':
            self.__port = self.config.uart_port
        else:
            self.__port = port

        if self.__port == '':
            raise ValueError('there must be a port declaration')
        
        self.__serial.baudrate = 115200
        self.__serial.bytesize = 8
        self.__serial.parity = 'N'
        self.__serial.timeout = 1.0
        self.__serial.rtscts = False
        self.__serial.port = self.__port
        # self.__serial.set_buffer_size(rx_size=256, tx_size=256)
        self.__serial.open()

        if update:
            self.update()

    def close(self, leds_clear=False):
        if leds_clear:
            self.leds_clear_all_update()
        self.__serial.close()

    def update(self):
        self.__write()
        self.__read()

    def get_version(self):
        self.__write_version()
        self.__read()
        return self.version

    def __write_version(self):
        self.__write_msg = '?\n'
        self.__serial.write(self.__write_msg.encode())

    def __write(self):
        # if not self.__serial.is_open:
        #     self.open(update=False)

        self.__write_msg = ''

        for i in range(5):
            mask = 0x00
            for n in range(5):
                if self.leds[i][n]:
                    mask += 2**n
            mask += 0x41
            self.__write_msg += chr(mask)  # ord('a'), chr(97)
        self.__write_msg += '\n'
        self.__serial.write(self.__write_msg.encode())


    def __read(self):
        self.__read_msg = ''
        read_done = False
        time_now = time.time()
        time_start_read = time.time()

        while not read_done:
            if (time.time() - time_start_read) > 1.0:
                self.close()
                raise ValueError('timeout read Microbit')
                # print('timeout read Microbit')
                # read_done = True
                # break

            if self.__serial.in_waiting > 0:
                reply = self.__serial.read(self.__serial.in_waiting)
            else:
                reply = ''

            if reply != '':
                self.__read_msg += reply.decode('utf-8')
                if self.__read_msg.find('\n') != -1 or len(self.__read_msg) == 17:

                    read_done = True
                    if self.__read_msg.find('?') == -1:
                        self.version = hex_to_signed(self.__read_msg[0:2])

                        if self.__read_msg[2] == '1':
                            self.button_a = True
                        else:
                            self.button_a = False

                        if self.__read_msg[3] == '1':
                            self.button_b = True
                        else:
                            self.button_b = False

                        # Eventauswertung der Taster
                        if not self.__button_a_old  and self.button_a:
                            self.button_event_a = True
                        else:
                            self.button_event_a = False
                        self.__button_a_old = self.button_a

                        if not self.__button_b_old and self.button_b:
                            self.button_event_b = True
                        else:
                            self.button_event_b = False
                        self.__button_b_old = self.button_b

                        self.acc_x = hex_to_signed(self.__read_msg[4:8]) / 1000
                        self.acc_y = hex_to_signed(self.__read_msg[8:12]) / 1000
                        self.acc_z = hex_to_signed(self.__read_msg[12:16]) / 1000

                        self.acc_x_lim_p1_m1 = self.acc_x
                        if self.acc_x_lim_p1_m1 > 1.0:
                            self.acc_x_lim_p1_m1 = 1.0
                        elif self.acc_x_lim_p1_m1 < -1.0:
                            self.acc_x_lim_p1_m1 = -1.0

                        self.acc_y_lim_p1_m1 = self.acc_y
                        if self.acc_y_lim_p1_m1 > 1.0:
                            self.acc_y_lim_p1_m1 = 1.0
                        elif self.acc_y_lim_p1_m1 < -1.0:
                            self.acc_y_lim_p1_m1 = -1.0

                        self.acc_z_lim_p1_m1 = self.acc_z
                        if self.acc_z_lim_p1_m1 > 1.0:
                            self.acc_z_lim_p1_m1 = 1.0
                        elif self.acc_z_lim_p1_m1 < -1.0:
                            self.acc_z_lim_p1_m1 = -1.0

                    else:
                        # Error oder Versionsabfrage
                        if len(self.__read_msg) == 4:
                            self.version = hex_to_signed(self.__read_msg[1:3])
                        else:
                            raise ValueError('microbit unknown uart command')
            else:
                if (time.time() - time_now) >= 1.0:
                    read_done = True
                    raise ValueError('microbit uart timeout')
                else:
                    time.sleep(0.010)

        self.__serial.flushInput()
