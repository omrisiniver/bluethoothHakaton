from mybluetooth import BluetoothRSSI
from time import sleep
import mybluetooth
import sys
import struct
import socket

server_ip = '127.0.0.1'
server_port = 5000
mac = '88:75:98:A6:33:C7'

b = BluetoothRSSI(addr=mac)
server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_sock.connect((server_ip, server_port))

while True:
	rssi = b.request_rssi()
	print(rssi)
	# server_sock.send(bytearray(rssi[0]))
	# print ("---")
	# print ("addr: {}, rssi: {}".format(mac, rssi))
 #    # Sleep and then skip to next iteration if device not found