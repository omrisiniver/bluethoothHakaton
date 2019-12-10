from bt_proximity import BluetoothRSSI
# from bluetooth import _bluetooth
from time import sleep
import bluetooth
import sys
import struct
import bluetooth._bluetooth as bluez  # low level bluetooth wrappers
import socket

# print("before discover_devices")
# nearby_devices = bluetooth.discover_devices(lookup_names=True)
# print("Found {} devices.".format(len(nearby_devices)))

# for addr, name in nearby_devices:
#     print("  {} - {}".format(addr, name))

# print(nearby_devices[0][0])
server_ip = '127.0.0.1'
server_port = 5000
mac = '88:75:98:A6:33:C7'
b = BluetoothRSSI(addr=mac)
server_sock = socket.socket(AF_INET, SOCK_DGRAM, 0)
server_sock.connect((server_ip, server_port))

while True:
	sleep(1)
	rssi = b.request_rssi()
	server_sock.send(bytearray(rssi[0]))
	print ("---")
	print ("addr: {}, rssi: {}".format(mac, rssi))
    # Sleep and then skip to next iteration if device not found