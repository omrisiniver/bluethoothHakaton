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
mac = '88:75:98:A6:33:C7'

b = BluetoothRSSI(addr=mac)

# server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# server_sock.connect((server_ip, server_port))

from scipy.signal import savgol_filter


def noise_reducing(x, y, window_length=101, polyorder=2):
    w = savgol_filter(y, window_length, polyorder)
    plt.plot(x, w, 'b')  # high frequency noise removed


def info_gathering():
    rssi = b.request_rssi()
    timestamp = time.time()

    print(rssi)
    msg = pickle.dumps({"mac_adr": mac, "timestamp": timestamp, "rssi": rssi})
    # server_sock.send(msg)
    # print("---")
    # print("addr: {}, rssi: {}".format(mac, rssi))
    return rssi, timestamp


plt.style.use('fivethirtyeight')

index = count()
x_values = []
y_values = []


def animate(i):
    global x_values, y_values, plt
    info = info_gathering()
    x_values.append(info[1])
    y_values.append(info[0])
    # noise_reducing(x_values, y_values, window_length=5)
    plt.plot(x_values, y_values)


ani = FuncAnimation(plt.gcf(), animate, 1000)

plt.tight_layout()
plt.show()

# Sleep and then skip to next iteration if device not found
