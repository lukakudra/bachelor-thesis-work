import socket
import struct
from network import LoRa
import time
from machine import UART
import utime
import sys
import os
import pycom
import machine

uart = UART(0, 57600)
uart.init(57600, bits=8, parity=None, stop=1)

tx_p = 14
bw = LoRa.BW_125KHZ
s_f = 12
c_r = LoRa.CODING_4_5

pycom.heartbeat(False)

"""
Methods that emulate random module in python
"""

"""
Returns the bit length of an integer
"""


def bit_len(n):
    length = 0
    while n:
        n >>= 1
        length += 1
    return length


def last_bit(f):
    return struct.pack('!f', f)[-1] & 1


"""
Returns k random bits using a relative drift of two clocks,
based on the assumption that they are different
"""


def get_random_bits(k):
    result = 0
    for _ in range(k):
        time.sleep(0)
        result <<= 1
        result = result | last_bit(utime.ticks_cpu())
    return result


def random_bits_using_os_urandom(k):
    return int.from_bytes(os.urandom(k), sys.byteorder)


"""
Returns a random int in the range [0,n)
"""


def random_below(n):
    if n <= 0:
        raise ValueError
    k = bit_len(n)
    r = get_random_bits(k)
    while r >= n:
        r = get_random_bits(k)
    return r


def random_integer(a, b):
    return a + random_below(b - a + 1)


"""
Methods for generating random values of LoRa channel parameters
"""


def randomize_tx_power():
    return random_integer(2, 14)


def randomize_bandwith():
    list_of_bandwith_values = [LoRa.BW_125KHZ, LoRa.BW_250KHZ]
    rand_index = random_integer(0, 1)
    return list_of_bandwith_values[rand_index]


def randomize_sf():
    return random_integer(7, 12)


def randomize_coding_rate():
    list_of_coding_rate_values = [
        LoRa.CODING_4_5, LoRa.CODING_4_6, LoRa.CODING_4_7, LoRa.CODING_4_8]
    rand_index = random_integer(0, 3)
    return list_of_coding_rate_values[rand_index]


# LoRa setup
lora = LoRa(mode=LoRa.LORA, rx_iq=True)
#lora.init(mode=LoRa.LORA, tx_power=14, bandwidth=LoRa.BW_125KHZ, sf=12, coding_rate=LoRa.CODING_4_5)
lora_sock = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
lora_sock.setblocking(False)

while True:

    lora.init(mode=LoRa.LORA, tx_power=14, bandwidth=LoRa.BW_125KHZ,
              sf=12, coding_rate=LoRa.CODING_4_7)

    tx_p = randomize_tx_power()
    bw = randomize_bandwith()
    s_f = randomize_sf()
    c_r = randomize_coding_rate()
    # time.sleep(1)

    """
    Broadcast new parameters to nodes
    """
    for i in range(0, 5):
        lora_params = str(5-i) + "|" + str(tx_p) + "|" + str(bw) + "|" + \
            str(s_f) + "|" + str(c_r)
        # print("NEW PARAMETERS: ", lora_params)
        lora_sock.send(lora_params)
        pycom.rgbled(0x0000ff) # blue = transmit new channel parameters
        time.sleep(1)

    """
    Get into receive mode to receive data from nodes
    """
    lora.init(mode=LoRa.LORA, tx_power=tx_p,
              bandwidth=bw, sf=s_f, coding_rate=c_r)
    time.sleep(1)

    """
    Receive data for 30 seconds and write it to UART
    """
    timeout = time.time() + 30*1
    while True:
        pycom.rgbled(0xffff00) # yellow = in receive mode
        test = 0
        if test == 1 or time.time() > timeout:
            break

        recv_pkg = lora_sock.recv(512)
        data = recv_pkg.decode('UTF-8')

        if data:

            stats = lora.stats()
            rssi = stats[1]
            signal_to_noise = stats[2]

            line = (str(data) + "|" + str(rssi) + "|" + str(signal_to_noise) +
                    "|" + str(tx_p) + "|" + str(bw) + "|" +
                    str(s_f) + "|" + str(c_r) + "\r\n")
            uart.write(line)
            # print(line)
            test = test - 1
            pycom.rgbled(0x00ff00) # package has been received
            time.sleep(1)

    time.sleep(1)
