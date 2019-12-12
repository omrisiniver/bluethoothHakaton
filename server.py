from bt_proximity import BluetoothRSSI
from time import sleep
import bluetooth
import sys
import struct
import bluetooth._bluetooth as bluez  # low level bluetooth wrappers
import socket
import pickle
from threading import Thread, RLock
import json
import requests
url = 'https://theroom-1df52.firebaseio.com/alarm.json'

SERVER_IP = '192.168.4.39'
SERVER_PORT = 5000
THRESHOLD = 10

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
sock.bind((SERVER_IP, SERVER_PORT))

data = {}
enemy = False
lock = RLock()
close_location = 'close_from_door'
far_location = 'far_from_door'
is_started = False

class DataCollector(Thread):
    def __init__(self, data, is_started, lock):
        super().__init__()
        self.rlock = lock
        self.data = data
        self.is_started = is_started
        self.far_packet_counter = 0
        self.close_packet_counter = 0


    def get_started(self):
        return self.is_started

    def get_packet_counter(self):
        return self.far_packet_counter, self.close_packet_counter

    def run(self):
        count_sensors = 0
        while True:
            with self.rlock:
                packet = sock.recv(100)
                info = pickle.loads(packet)
                mac = info["location"]
                if mac in self.data:
                    if self.is_started:
                        if mac == 'close_from_door':
                            self.close_packet_counter += 1
                        else:
                            self.far_packet_counter += 1
                        self.data[mac].append(info['rssi'])
                else:
                    print('arrived {} {}'.format(mac, count_sensors))
                    count_sensors += 1
                    if count_sensors == 2:
                        print('arrived True')
                        self.is_started = True
                    self.data[mac] = [info['rssi']]


if __name__ == "__main__":
    # global data
    data_collector = DataCollector(data=data, is_started=is_started, lock=lock)
    data_collector.start()
    counter = 0

    while True:
        if data_collector.get_started() is False:
            continue

        curr_far, curr_close = data_collector.get_packet_counter()
        if curr_close < counter or curr_far < counter:
            # print('stuck {} {}'.format(curr_close, curr_far))
            continue
        prev_check = enemy

        print('far: {}, close: {}'.format(data['far_from_door'][counter], data['close_from_door'][counter]))
        if data['far_from_door'][counter] + THRESHOLD > 0:
            enemy = True
        elif data['close_from_door'][counter] + THRESHOLD < 0 and \
             data['far_from_door'][counter] + THRESHOLD * 2 < 0:
            enemy = False
        elif data['close_from_door'][counter] + THRESHOLD > 0 and \
             data['far_from_door'][counter] + THRESHOLD * 2 > 0:
            enemy = True
        # elif data['close_from_door'][counter] + THRESHOLD > 0 and \
        #      data['far_from_door'][counter] + THRESHOLD * 2 > 0:
        #     enemy = True
        counter += 1
        if enemy is not prev_check:
            status = {'state': enemy}
            r = requests.put(url, data=json.dumps(status))
            print("Enemy is : {}".format(enemy))
