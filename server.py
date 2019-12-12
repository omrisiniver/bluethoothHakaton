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
import collections
url = 'https://theroom-1df52.firebaseio.com/alarm.json'

SERVER_IP = '192.168.4.51'
SERVER_PORT = 5000
THRESHOLD = 10

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
sock.bind((SERVER_IP, SERVER_PORT))

data = {}
enemy = False
lock = RLock()
IN_DOOR = 'in door'
OUT_DOOR = 'out door'
is_started = False

class Packet:
    def __init__(self, rssi, timestamp):
        self.rssi = rssi
        self.timestamp = timestamp

class DataCollector(Thread):
    def __init__(self, data, is_started, lock, sock):
        super().__init__()
        self.rlock = lock
        self.data = data
        self.is_started = is_started
        self.far_packet_counter = 0
        self.close_packet_counter = 0
        self.sock = sock


    def get_started(self):
        return self.is_started

    def get_packet_counter(self):
        return self.far_packet_counter, self.close_packet_counter

    def run(self):
        count_sensors = 0
        while True:
            with self.rlock:
                print("recv")
                packet = sock.recv(100)
                info = pickle.loads(packet)
                print(info)
                mac = info["location"]
                packet = Packet(rssi=info['rssi'], timestamp=info['timestamp'])
                if mac in self.data:
                    if self.is_started:
                        if mac == IN_DOOR:
                            self.close_packet_counter += 1
                        else:
                            self.far_packet_counter += 1
                        
                else:
                    print('arrived {} {}'.format(mac, count_sensors))
                    count_sensors += 1
                    if count_sensors == 2:
                        self.is_started = True
                    self.data[mac] = collections.OrderedDict()
                self.data[mac][packet.timestamp] = packet.rssi

def calc_grad(data):
    first = data[0][0] 
    last = data[0][-1]
    grad = (data[1][-1] - data[1][0]) / (data[0][-1] - data[1][0])
    return grad

class Server(Thread):

    def run(self):
        global data

        counter = 0
        while True:
            if data_collector.get_started() is False:
                continue

            curr_far, curr_close = data_collector.get_packet_counter()
            if curr_close < counter or curr_far < counter:
                # print('stuck {} {}'.format(curr_close, curr_far))
                continue
            prev_check = enemy

            in_door = data[IN_DOOR][:-1]
            out_door = data[OUT_DOOR][:-1]

            delta = in_door - out_door

            # Graph change over time
            # in_gradient = calc_grad([data[IN_DOOR]])
            # out_gradient = calc_grad(data[OUT_DOOR])

            if in_door > out_door:
                enemy = False
                print("Enemy is outside")
            else:
                enemy = True
                print("Enemy is inside")

            # print('far: {}, close: {}'.format(data['far_from_door'][counter], data['close_from_door'][counter]))
            # if data['far_from_door'][counter] + THRESHOLD > 0:
            #     enemy = True
            # elif data['close_from_door'][counter] + THRESHOLD < 0 and \
            #      data['far_from_door'][counter] + THRESHOLD * 2 < 0:
            #     enemy = False
            # elif data['close_from_door'][counter] + THRESHOLD > 0 and \
            #      data['far_from_door'][counter] + THRESHOLD * 2 > 0:
            #     enemy = True
            # # elif data['close_from_door'][counter] + THRESHOLD > 0 and \
            #      data['far_from_door'][counter] + THRESHOLD * 2 > 0:
            #     enemy = True
            counter += 1
            if enemy is not prev_check:
                status = {'state': enemy}
                r = requests.put(url, data=json.dumps(status))
                print("Enemy is : {}".format(enemy))


if __name__ == "__main__":
    # global data
    print("START MAIN..")
    data_collector = DataCollector(data=data, is_started=is_started, lock=lock, sock=sock)
    data_collector.start()
    
    server = Server()
    server.start()