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

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
sock.bind((SERVER_IP, SERVER_PORT))

while True:
	packet = sock.recv(100)
	info = pickle.loads(packet)
	print(info)