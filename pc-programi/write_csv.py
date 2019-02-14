import sys
import csv

"""
This program accepts three arguments through commandline. The arguments are
filename, csv_name and area.

example usage: python3 ./write_csv.py 09-06-2018_20-29-49.txt zg_tr_data.csv zg_tr
"""


"""
This method processes a line from txt file that contains data written from 
LoPy gateway
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
    if len(sys.argv) > 3:
        filename = sys.argv[1]
        csv_name = sys.argv[2]
        area = sys.argv[3]
    else:
        print("You need to enter filename, csv_name and area")
        return

    # 70b3d5499aa0da7c -- mac address of node1
    # 70b3d5499616b59e -- mac address of node2

    # area ng -- gateway_lat = 45.22851, gateway_long = 17.35531
    # area zg_tr -- gateway_lat = 45.805630, gateway_long = 15.957969

    # Depending on given area, this section determines coordinates of a gateway
    if area == 'ng':
        gateway_lat = '45.22851'
        gateway_long = '17.35531'
    elif area == 'zg_tr':
        gateway_lat = '45.805630'
        gateway_long = '15.957969'
    elif area == 'zg_fer':
        gateway_lat = ''
        gateway_long = ''

    with open(csv_name, 'w', newline='') as c:

        field_names = ['n_id', 'mac_address', 'package_number', 'node_lat',
                       'node_long', 'x', 'y', 'z', 'rssi', 'snr', 'tx_power',
                       'bandwith', 'spreading_factor', 'coding_rate', 'gateway_lat',
                       'gateway_long']
        the_writer = csv.DictWriter(c, fieldnames=field_names)

        the_writer.writeheader()

        with open(filename) as f:
            for line in f:
                mac_address, package_number, node_lat, node_long, x, y, z, rssi, \
                    snr, tx_power, bandwith, spreading_factor, coding_rate = process(line)
                
                """
                This statement can be commented to include packets that
                didn't return their GPS coordinates in csv file
                """
                if node_lat == 'None' or node_long == 'None':
                    continue

                n_id = ''
                if mac_address == '70b3d5499aa0da7c':
                    n_id = 'Node1'
                elif mac_address == '70b3d5499616b59e':
                    n_id = 'Node2'

                the_writer.writerow({'n_id': n_id,
                                     'mac_address': mac_address,
                                     'package_number': package_number,
                                     'node_lat': node_lat,
                                     'node_long': node_long,
                                     'x': x,
                                     'y': y,
                                     'z': z,
                                     'rssi': rssi,
                                     'snr': snr,
                                     'tx_power': tx_power,
                                     'bandwith': bandwith,
                                     'spreading_factor': spreading_factor,
                                     'coding_rate': coding_rate,
                                     'gateway_lat': gateway_lat,
                                     'gateway_long': gateway_long})


if __name__ == '__main__':
    main()



