from pytrack import Pytrack
from L76GNSS import L76GNSS
from LIS2HH12 import LIS2HH12

from network import LoRa

import time
import socket
import binascii
import pycom


py = Pytrack()
gps = L76GNSS(py, timeout=1)
acc = LIS2HH12(py)

tx_p = 14
bw = LoRa.BW_125KHZ
s_f = 12
c_r = LoRa.CODING_4_5

pycom.heartbeat(False)


"""
------------- LIS2HH12.acceleration() -------------
Read the acceleration from the LIS2HH12.
Returns a tuple with the 3 values of acceleration (G).
"""


def read_acceleration(acc):
    return acc.acceleration()


"""
------------- LIS2HH12.roll() -------------
Read the current roll from the LIS2HH12.
Returns a float in degrees in the range -180 to 180.
"""


def read_roll(acc):
    return acc.roll()


"""
------------- LIS2HH12.pitch() -------------
Read the current pitch from the LIS2HH12.
Returns a float in degrees in the range -90 to 90.
Once the board tilts beyond this range the values will repeat.
This is due to a lack of yaw measurement,
making it not possible to know the exact orientation of the board.
"""


def read_pitch(acc):
    return acc.pitch()


"""
------------- L76GNSS.coordinates() -------------
Read coordinates(latitude and longitude) from the L76GNSS.
"""


def read_coordinates(gps):
    return gps.coordinates()


"""
Method for sensor data formatting
"""


def get_sensor_data():
    latitude, longitude = read_coordinates(gps)
    gps_coordinates = str(latitude) + "," + str(longitude)
    x, y, z = read_acceleration(acc)
    x = "{0:.4f}".format(x)
    y = "{0:.4f}".format(y)
    z = "{0:.4f}".format(z)
    acceleration = str(x) + "," + str(y) + "," + str(z)

    data = str(gps_coordinates) + "|" + str(acceleration)

    return data


# LoRa setup
lora = LoRa(mode=LoRa.LORA, tx_iq=True)
#lora.init(mode=LoRa.LORA, tx_power=14, bandwidth=LoRa.BW_125KHZ, sf=12, coding_rate=LoRa.CODING_4_5)
lora_sock = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
lora_sock.setblocking(False)

device_id = lora.mac()
device_id = binascii.hexlify(device_id)
device_id = device_id.decode('UTF-8')

while True:

    lora.init(mode=LoRa.LORA, tx_power=14, bandwidth=LoRa.BW_125KHZ,
              sf=12, coding_rate=LoRa.CODING_4_7)

    """
    Wait for new channel parameters to arrive from gateway.
    When they arrive break the loop
    """
    while True:

        pycom.rgbled(0xffff00) # yellow = waiting for package to arrive
        recv_pkg = lora_sock.recv(512)
        data = recv_pkg.decode('UTF-8')
        tmp = data.split("|")
        if tmp[0] == '0' or tmp[0] == '1' or tmp[0] == '2' or tmp[0] == '3' or tmp[0] == '4' or tmp[0] == '5':
            break
        time.sleep(1)

    waiting_time = int(tmp[0])
    tx_p = int(tmp[1])
    bw = int(tmp[2])
    s_f = int(tmp[3])
    c_r = int(tmp[4])

    """
    Get into transmit mode to send data to gateway
    """
    lora.init(mode=LoRa.LORA, tx_power=tx_p,
              bandwidth=bw, sf=s_f, coding_rate=c_r)
    pycom.rgbled(0x00ff00) # green = new channel parameters are received
    time.sleep(waiting_time)

    """
    Send N packages to gateway
    """
    for i in range(0, 10):
        to_send = str(device_id) + "|" + str(i) + "|" + get_sensor_data()
        try:
            lora_sock.send(to_send)
            pycom.rgbled(0x0000ff) # blue = transmiting data
            time.sleep(1)
        except OSError as err:
            pycom.rgbled(0xff0000) # red = exception OSError has been caught
            continue
