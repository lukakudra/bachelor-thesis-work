import sys
from collections import defaultdict

"""
This program reads txt file with written data from LoPy and calculates the success
rate every set of parameters. It accepts one command line argument and that is
the name of txt file with written data. This program only works with data from
09-06-2018_20-29-49.txt file.

example usage: python3 ./packet_success_zg_tr.py 09-06-2018_20-29-49.txt
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
        if ('70b3d5499aa0da7c', '13', '1', '8', '2') == key:
            success = value / 110
        elif ('70b3d5499616b59e', '13', '1', '8', '2') == key:
            success = value / 20
        elif ('70b3d5499aa0da7c', '6', '1', '8', '4') == key:
            success = value / 20
        elif ('70b3d5499616b59e', '6', '1', '8', '4') == key:
            success = value / 20
        elif ('70b3d5499aa0da7c', '6', '0', '8', '4') == key:
            success = value / 50
        elif ('70b3d5499aa0da7c', '8', '1', '11', '2') == key:
            success = value / 60
        elif ('70b3d5499aa0da7c', '11', '0', '11', '2') == key:
            success = value / 20
        elif ('70b3d5499aa0da7c', '14', '1', '12', '4') == key:
            success = value / 20
        elif ('70b3d5499aa0da7c', '5', '0', '12', '3') == key:
            success = value / 20
        elif ('70b3d5499aa0da7c', '11', '0', '12', '1') == key:
            success = value / 60
        elif ('70b3d5499aa0da7c', '3', '1', '12', '3') == key:
            success = value / 30
        elif ('70b3d5499aa0da7c', '6', '0', '10', '4') == key:
            success = value / 30
        elif ('70b3d5499aa0da7c', '8', '1', '7', '2') == key:
            success = value / 20
        elif ('70b3d5499aa0da7c', '8', '1', '11', '4') == key:
            success = value / 30
        elif ('70b3d5499aa0da7c', '4', '1', '12', '2') == key:
            success = value / 20
        elif ('70b3d5499aa0da7c', '11', '0', '11', '4') == key:
            success = value / 40
        elif ('70b3d5499aa0da7c', '13', '0', '12', '1') == key:
            success = value / 30
        elif ('70b3d5499aa0da7c', '11', '1', '11', '4') == key:
            success = value / 20
        elif ('70b3d5499aa0da7c', '8', '1', '10', '3') == key:
            success = value / 40
        elif ('70b3d5499aa0da7c', '13', '0', '12', '4') == key:
            success = value / 20
        elif ('70b3d5499aa0da7c', '11', '0', '12', '4') == key:
            success = value / 20
        else:
            success = value / 10

        packet_loss_dict[key] = success

    for key, value in packet_loss_dict.items():
        print("KEY: ", key, "SUCCESS: ", value)


if __name__ == '__main__':
    main()