#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Link
# https://sqlitestudio.pl/index.rvt
# https://www.sqlitetutorial.net
# https://www.sqlitetutorial.net/sqlite-python
# https://www.w3schools.com/sql/default.asp

# Delete from Student

import os
import sqlite3

class DbData:
    def __init__(self, row=None):
        self.id = 0
        self.version = 0
        self.time = 0.0
        self.led = [[False for i in range(5)] for n in range(5)]
        self.button_a = False
        self.button_b = False
        self.acc_x = 0.0
        self.acc_y = 0.0
        self.acc_z = 0.0
        self.mag_x = 0.0
        self.mag_y = 0.0
        self.mag_z = 0.0
        self.version = 0

        if row is not None:
            self.row_to_value(row)

    def row_to_value(self, row):
        # data = [1, 1576502201.764887, '1000000001000000000000010', '0', -0.011, -0.299, -0.939, -397, -24, 510]
        #print(row)
        self.id = row[0]
        self.version = row[1]
        self.time = row[2]

        for i in range(0, 5, 1):
            for n in range(0, 5, 1):
                if row[3][i*5 + n] == '1':
                    self.led[i][n] = True
                else:
                    self.led[i][n] = False

        if row[4][0] == '1':
            self.button_a = True
        else:
            self.button_a = False

        if row[4][1] == '1':
            self.button_b = True
        else:
            self.button_b = False

        self.acc_x = row[5]
        self.acc_y = row[6]
        self.acc_z = row[7]

        self.mag_x = row[8]
        self.mag_y = row[9]
        self.mag_z = row[10]

    def __str__(self):
        """
        Klartextausgabe der Klasseneigenschaften.
        """
        class_str = ''
        class_str += f'| id: {self.id:01d} | '
        class_str += f'time: {self.time:0.04f} | '

        led_str = 'led: '
        for i in range(0, 5, 1):
            for n in range(0, 5, 1):
                if self.led[i][n]:
                    led_str += '1'
                else:
                    led_str += '0'
        class_str += led_str + ' | '
        class_str += f'btn AB: {self.button_a:b}{self.button_b:b} | '

        class_str += f'acc_x: {self.acc_x:0.03f} | '
        class_str += f'acc_y: {self.acc_y:0.03f} | '
        class_str += f'acc_z: {self.acc_z:0.03f} | '

        class_str += f'mag_x: {self.mag_x:0.03f} | '
        class_str += f'mag_y: {self.mag_y:0.03f} | '
        class_str += f'mag_z: {self.mag_z:0.03f} |'

        return class_str


class Db:
    """SqLite-Datenbankintegration für die Verwaltung der Uebersetzungen."""

    def __init__(self, file_path=None):
        if file_path is None:
            absolute_path = (os.path.dirname(os.path.abspath(__file__))).replace('\\', '/')
            self._file_path = absolute_path + '/db_microbit.sqlite'
        else:
            self._file_path = file_path

        self._db_connection = None
        self.connect()

    def connect(self):
        """Erstelle eine Verbindung zur SqLite-Datenbank."""
        try:
            self._db_connection = sqlite3.connect(self._file_path)
        except Exception as e:
            print('error microbit.connect:', e)

    def insert(self, value):
        """Einfügen von neuen Einträgen in die Datenbank."""
        try:
            sql = '''INSERT INTO microbit(version, time, leds, buttons, 
                     acc_x, acc_y, acc_z,
                     mag_x, mag_y, mag_z)
                     VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
            cursor = self._db_connection.cursor()
            cursor.execute(sql, value)
            self._db_connection.commit()
            # print(cursor.lastrowid)
            return cursor.lastrowid
        except Exception as e:
            print('error microbit.insert:', e)
            return -1

    def select_all(self):
        """Selektierung sämtlicher Einträge."""
        try:
            sql = '''SELECT * FROM microbit ORDER BY id ASC'''
            cursor = self._db_connection.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            return rows
        except Exception as e:
            print('error microbit.select_all:', e)
            return []

    def select_all_class(self):
        rows = []
        for row in self.select_all():
            rows.append(DbData(row))
        return rows

    def search(self, term):
        """Suche in der Datenbank nach Uebersetzungen mit dem Inhalt von term."""
        try:
            sql = '''SELECT * FROM microbit WHERE 
                     src LIKE '%{:s}%' OR dest LIKE '%{:s}%' ORDER BY id DESC'''.format(term, term)
            cursor = self._db_connection.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            return rows
        except Exception as e:
            print('error microbit.sarch:', e)
            return []

    def delete(self, id):
        """Lösche den Datensatz mit der id"""
        try:
            sql = '''DELETE FROM microbit WHERE id=?'''
            cursor = self._db_connection.cursor()
            cursor.execute(sql, [id])

            self._db_connection.commit()
        except Exception as e:
            print('error microbit.delete:', e)

    def delete_all(self):
        """Lösche sämtliche Datensätze in der Tabelle."""
        try:
            sql = '''DELETE FROM microbit'''
            cursor = self._db_connection.cursor()
            cursor.execute(sql, [])

            self._db_connection.commit()
        except Exception as e:
            print('error microbit.delete:', e)


if __name__ == '__main__':
    db = Db()
    db.connect()
    for row in db.select_all_class():
        print(row)

