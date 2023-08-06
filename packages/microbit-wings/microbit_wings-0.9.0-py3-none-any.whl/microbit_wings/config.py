#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from configparser import ConfigParser


class Config:
    """Konfigurationsklasse für den remanenten Datenzugriff von Parametern."""
    def __init__(self, file_path=None):

        if file_path is None:
            # path = (os.path.dirname(os.path.abspath(__file__))).replace('\\', '/')
            # self._file_path = path + '/config.ini'
            self._file_path = None

        else:
            self._file_path = file_path

        self._config = ConfigParser()

        self.dir_app_path = ''

        # [uart]
        self.uart_port = ''

        self.build_ini_file_path()
        self.check_if_file_exist()
        self.read()

    def build_ini_file_path(self):

        if sys.platform.startswith('win'):  # Windows
            # Windows: create folder in the user appdata space
            self.dir_app_path = os.getenv('APPDATA').replace('\\', '/') + '/microbit_wings'
            self._file_path = self.dir_app_path + '/config.ini'
        elif sys.platform.startswith('darwin'):  # Mac
            # Mac OS: create folder in the user library space
            self.dir_app_path = os.path.expanduser('~/Library/') + 'microbit_wings'
            self._file_path = self.dir_app_path + '/config.ini'
        else:
            raise EnvironmentError('Unsupported platform')

        # print(_dir_app_path)
        # print(self._file_path)

        if not os.path.exists(self.dir_app_path):
            os.mkdir(self.dir_app_path)

    def check_if_file_exist(self):
        try:
            f = open(self._file_path)
            self.read()
        except FileNotFoundError as e:
            f = open(self._file_path, 'x')
            f.write('[uart]\n')
            f.close()
        finally:
            f.close()

    def read(self):
        """Lesen der Parameter aus der Konfigurationsdatei."""
        try:
            f = open(self._file_path, 'r')
            self._config.read_file(f)
            f.close()

            # [uart]
            self.uart_port = self._config.get('uart', 'port')

        except Exception as e:
            print('Error config read:', str(e))

        finally:
            f.close()

    def write(self):
        """Schreiben der Parameter in die Konfigurationsdatei."""
        try:
            f = open(self._file_path, 'w')

            # [uart]
            if sys.platform.startswith('win'):  # Windows
                self._config.set('uart', 'port', self.uart_port)
            elif sys.platform.startswith('darwin'):  # Mac
                self._config.set('uart', 'port', ('/dev/tty.' + self.uart_port))
            else:
                raise EnvironmentError('Unsupported platform')

            self._config.write(f)

        except Exception as e:
            print('Error config write:', str(e))

        finally:
            f.close()

    @staticmethod
    def bool_to_string(value):
        """Hilfsmethode zur Speicherung von boolschen Datentypen. In Konfigurationsdateien
        sind die Werte True und False in true und false zu konvertieren."""
        if value:
            string = 'true'
        else:
            string = 'false'
        return string

    def write_uart_port(self, uart_port):
        self.uart_port = uart_port
        self.write()


if __name__ == '__main__':
    config = Config()

    print(config.dir_app_path)

    config.read()
    print('[uart]')
    print('port =', config.uart_port)

    # config.write_uart_port('COM1')
    # config.write_uart_port('/dev/tty.serial1')
    # config.read()
    # print('[uart]')
    # print('port =', config.uart_port)
