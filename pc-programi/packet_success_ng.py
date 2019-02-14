import sys
from collections import defaultdict

"""
This program reads txt file with written data from LoPy and calculates the success
rate every set of parameters. It accepts one command line argument and that is
the name of txt file with written data. This program only works with data from
03-06-2018_12-33-28.txt file.

example usage: python3 ./packet_success_ng.py 03-06-2018_12-33-28.txt
"""


def process(line):
    tmp = line.split("|")
    mac_address = tmp[0]
    package_number = tmp[1]
    node_coordinates = tmp[2]
    acc = tmp[3]
    rssi = tmp[4]
    snr = tmp[5]
    tx_power = tmp[6]
    bandwith = tmp[7]
    spreading_factor = tmp[8]
    coding_rate = tmp[9]

    n_c = node_coordinates.split(",")
    node_lat = n_c[0]
    node_long = n_c[1]

    a = acc.split(",")
    x = a[0]
    y = a[1]
    z = a[2]

    return mac_address, package_number, node_lat, node_long, x, y, z, rssi, \
        snr, tx_power, bandwith, spreading_factor, coding_rate


def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        print("You need to enter the filename")
        return

    data = defaultdict(int)

    with open(filename) as f:
        for line in f:
            mac_address, package_number, node_lat, node_long, x, y, z, rssi, \
                snr, tx_power, bandwith, spreading_factor, coding_rate = process(
                    line.rstrip("\r\n"))

            data[mac_address, tx_power, bandwith,
                 spreading_factor, coding_rate] += 1

    packet_loss_dict = {}
    success = 0.
    for key, value in data.items():
        if ('70b3d5499aa0da7c', '6', '1', '8', '4') == key:
            success = value / 100
        elif ('70b3d5499aa0da7c', '6', '1', '10', '4') == key:
            success = value / 100
        elif ('70b3d5499616b59e', '6', '1', '8', '4') == key:
            success = value / 100
        elif ('70b3d5499616b59e', '6', '1', '10', '4') == key:
            success = value / 100
        else:
            success = value / 50

        packet_loss_dict[key] = success

    for key, value in packet_loss_dict.items():
        print("KEY: ", key, "SUCCESS: ", value)


if __name__ == '__main__':
    main()
