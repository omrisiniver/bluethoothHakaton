from bt_proximity import BluetoothRSSI
from time import sleep
import bluetooth
import sys
import struct
import bluetooth._bluetooth as bluez  # low level bluetooth wrappers
import socket
import pickle

SERVER_IP = '127.0.0.1'
SERVER_PORT = 5000

sock = socket.socket(AF_INET, SOCK_DGRAM)
sock.bind(SERVER_IP, SERVER_PORT)

while True:
	packet = sock.recv(len(Info))
	info = pickle.loads(packet)
	print(info)