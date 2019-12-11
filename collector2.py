from time import sleep, time
from mybluetooth import BluetoothRSSI
import socket
import pickle
import time
import random
from itertools import count
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from threading import Thread, RLock

server_ip = '127.0.0.1'
server_port = 5000
# mac = '88:75:98:A6:33:C7'
mac = '9C:E3:3F:D3:9D:CA'

b = BluetoothRSSI(addr=mac)

# server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# server_sock.connect((server_ip, server_port))

from scipy.signal import savgol_filter


def noise_reducing(x, y, window_length=101, polyorder=2):
    w = savgol_filter(y, window_length, polyorder)
    return w
    # plt.plot(x, w, 'b')  # high frequency noise removed


class Data:
    def __init__(self, rssi, timestamp):
        self.rssi = rssi
        self.timestamp = timestamp


def info_gathering():
    rssi = b.request_rssi()
    if rssi is None:
        return None

    timestamp = time.time()

    # print(rssi)
    msg = pickle.dumps({"mac_adr": mac, "timestamp": timestamp, "rssi": rssi})
    # server_sock.send(msg)
    # print("---")
    # print("addr: {}, rssi: {}".format(mac, rssi))
    # print("rssi: {}".format(rssi[0]))
    return Data(rssi=rssi[0], timestamp=timestamp)


def batch_gathering(batch_size=5):
    info = []
    for _ in range(batch_size):
        one_sample = info_gathering()

        if one_sample is None:
            # TODO:: need to understand how to act when it appears
            return None

        info.append(one_sample)
    return info


plt.style.use('fivethirtyeight')

index = count()
x_values = []
y_values = []
lock = RLock()
import csv

class DataCollector(Thread):
    def __init__(self,x, y, lock):
        super().__init__()
        self.rlock = lock
        self.x = x
        self.y =y

    def run(self):
        with open('employee_file.csv', mode='w') as employee_file:
            employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            while True:
                
                with self.rlock:
                    # print("LOCKING BY DATA")
                    data = info_gathering()
                    self.x.append(data.timestamp)
                    self.y.append(data.rssi)
                    employee_writer.writerow([data.rssi, data.timestamp])
                    # print("DATA RELEASED THE LOCK")

def animate(i):
    print("cal mee!!! ", i)
    global x_values, y_values, lock
    with lock:
        print("LOCKING BY ANIMATE")
        print(len(x_values))
        if len(x_values) > 1000:
            # x_values = x_values + list(info.timestamp for info in data)
            # y_values = y_values + list(info.rssi for info in data)
            y_reduced = noise_reducing(x_values, y_values, window_length=501)
            plt.plot(x_values, y_reduced, 'b')
            # x_values[:] = []
            # y_values[:] = []
        # print("ANIMATE RELASED THE LOCK")

# Sleep and then skip to next iteration if device not found

def trying():
    curr = time.time()

    data = []
    while time.time() - curr <5:
        data.append(info_gathering())
    # print(len(data))
    # print(data)
# trying()

if __name__ == "__main__":
    data_collector = DataCollector(x=x_values, y=y_values, lock=lock)
    data_collector.start()
    # while True:
    #     time.sleep(1)
    #     animate(1)
    # ani = FuncAnimation(plt.gcf(), animate, 1000)
    # plt.tight_layout()
    # plt.show()


    # data_collector.join()
