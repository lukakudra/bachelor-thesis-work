import sys
import serial
from time import sleep
import time
import datetime

"""
This program reads data from serial interface and writes it to txt file that is 
named after the current time timestamp. It accepts two arguments from the command
line and they are: serial USB interface (it is necessary) and w (it is not necessary)
if you want to write the data from USB serial to a file.

example usage: python3 ./read_serial.py /dev/ttyUSB0 w
               or
               python3 ./read_serial.py /dev/ttyUSB0
"""

"""
This method returns current timestamp in certain format that is used to name the
file and adds extension .txt at the end of that timestamp
"""
def get_time_in_nice_format():
    time_stamp = time.time()
    nice_format = datetime.datetime.fromtimestamp(time_stamp).strftime('%d-%m-%Y_%H-%M-%S')
    return nice_format + ".txt"


def main():

    if len(sys.argv) > 1:
        port = sys.argv[1]
        if len(sys.argv) > 2:
            filename = sys.argv[2]
            if sys.argv[2] == "w":
                filename = get_time_in_nice_format()
                try:
                    f = open(filename, "w")
                except Exception as err:
                    print("Could not open file: ", filename)
                    print ("{!r}".format(err))
                    return
        else:
            f = None

        try:
            ser = serial.Serial(port, 57600)
            sleep(3)
            ser.reset_input_buffer()
        except Exception as err:
            print("Could not connect: {!r}".format(err))
            return

        print("Data connection at: ", port)

        while True:

            try:
                line = ser.readline().decode().rstrip("\r\n")
                if line != '':
                    print(line)
                    if f is not None:

                        f.write(line + "\r\n")
                else:
                    continue
            except Exception as err:
                print("".format(err))

        if f is not None:
            f.close()
    else:
        print("Usage: portName [w?]")


if __name__ == "__main__":
    main()
