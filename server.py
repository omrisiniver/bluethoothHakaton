from bt_proximity import BluetoothRSSI
from time import sleep
import bluetooth
import sys
import struct
import bluetooth._bluetooth as bluez  # low level bluetooth wrappers
import socket
import pickle
from threading import Thread, RLock


class DataCollector(Thread):
    def __init__(self, data, lock):
        super().__init__()
        self.rlock = lock
        self.data = data

    def run(self):
        while True:
            with self.rlock:
                packet = sock.recv(100)
                info = pickle.loads(packet)
                mac = info["location"]
                if mac in data:
                    data[mac].append(info['rssi'])
                else:
                    data[mac] = [info['rssi']]


SERVER_IP = '127.0.0.1'
SERVER_PORT = 5000
THRESHOLD = 25

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
sock.bind((SERVER_IP, SERVER_PORT))

data = {}
enemy = False
lock = RLock()
close_location = 'close_from_door'
far_location = 'far_from_door'


if __name__ == "__main__":
    data_collector = DataCollector(data=data, lock=lock)
    data_collector.start()
    counter = 0

    while True:

        if data['close_from_door'][counter] + THRESHOLD < 0