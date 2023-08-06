import glob
import os
import sys

import serial


# https://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python
# https://pyserial.readthedocs.io/en/latest/tools.html#module-serial.tools.list_ports

def get_serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):  # Mac OS
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


def hex_to_signed(source):
    """Convert a string hex value to a signed hexidecimal value.
    This assumes that source is the proper length, and the sign bit
    is the first bit in the first byte of the correct length.
    hex_to_signed("F") should return -1.
    hex_to_signed("0F") should return 15.
    """
    if not isinstance(source, str):
        raise ValueError("string type required")
    # if 0 == len(source):
    #    raise valueError("string is empty")
    sign_bit_mask = 1 << (len(source)*4-1)
    other_bits_mask = sign_bit_mask - 1
    value = int(source, 16)
    return -(value & sign_bit_mask) | (value & other_bits_mask)


if __name__ == '__main__':
    print(get_serial_ports())
    print(hex_to_signed('7F'), hex_to_signed('FF'), )
