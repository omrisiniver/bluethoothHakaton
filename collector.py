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

server_ip = '192.168.4.51'
server_port = 5000
# mac = '88:75:98:A6:33:C7'
mac = '9C:E3:3F:D3:9D:CA'
location = 'in_door'
BUNCH_NUMBER = 150

b = BluetoothRSSI(addr=mac)

server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_sock.connect((server_ip, server_port))

from scipy.signal import savgol_filter


def noise_reducing(x, y, window_length=101, polyorder=2):
    w = savgol_filter(y, window_length, polyorder)
    return w


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
    # print("---")
    # print("addr: {}, rssi: {}".format(mac, rssi[0]))
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


class DataCollector(Thread):
    def __init__(self, x, y, lock):
        super().__init__()
        self.rlock = lock
        self.x = x
        self.y = y

    def run(self):
        while True:
            with self.rlock:
                # print("LOCKING BY DATA")
                data = info_gathering()
                self.x.append(data.timestamp)
                self.y.append(data.rssi)
                # print("data.timestamp: {}, rssi: {}".format(data.timestamp, data.rssi))
                # print("DATA RELEASED THE LOCK")

def noise_avarage(x, y):
    return sum(x) / len(x), sum(y) / len(y)


def animate():
    print("cal mee!!! ")
    global x_values, y_values, lock, server_sock
    with lock:
        print(len(x_values))
        if len(x_values) > BUNCH_NUMBER:
            # y_reduced = noise_reducing(x_values, y_values, window_length=75)
            x_reduced, y_reduced = noise_avarage(x_values[:BUNCH_NUMBER], y_values[:BUNCH_NUMBER])
            print(y_reduced)
            msg = pickle.dumps({"location": location, "timestamp": x_reduced, "rssi": y_reduced})
            server_sock.send(msg)
            # plt.plot(x_values, y_reduced, 'b')
            x_values[:] = x_values[BUNCH_NUMBER:]
            y_values[:] = y_values[BUNCH_NUMBER:]
        # print("ANIMATE RELASED THE LOCK")


if __name__ == "__main__":
    data_collector = DataCollector(x=x_values, y=y_values, lock=lock)
    data_collector.start()
    while True:
        animate()
    # ani = FuncAnimation(plt.gcf(), animate, 1)
    # plt.tight_layout()
    # plt.show()

    # data_collector.join()
