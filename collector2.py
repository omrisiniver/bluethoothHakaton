from time import sleep, time
from mybluetooth import BluetoothRSSI
import socket
import pickle
import time
import random
from itertools import count
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

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
    plt.plot(x, w, 'b')  # high frequency noise removed


class Data:
    def __init__(self, rssi, timestamp):
        self.rssi = rssi
        self.timestamp = timestamp


def info_gathering():
    rssi = b.request_rssi()
    if rssi is None:
        return None

    timestamp = time.time()

    print(rssi)
    msg = pickle.dumps({"mac_adr": mac, "timestamp": timestamp, "rssi": rssi})
    # server_sock.send(msg)
    print("---")
    print("addr: {}, rssi: {}".format(mac, rssi))
    return Data(rssi=rssi[0], timestamp=timestamp)


def batch_gathering(batch_size=100):
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


def animate(i):
    global x_values, y_values, plt
    data = batch_gathering()

    if data is None:
        # TODO:: need to understand how to act when it appears
        return None

    x_values = x_values + list(info.timestamp for info in data)
    y_values = y_values + list(info.rssi for info in data)
    noise_reducing(x_values, y_values, window_length=91)
    # plt.plot(x_values, y_values, 'b')


ani = FuncAnimation(plt.gcf(), animate, 1000)

plt.tight_layout()
plt.show()

# Sleep and then skip to next iteration if device not found
