from time import sleep, time
from mybluetooth import BluetoothRSSI
import socket
import pickle

server_ip = '127.0.0.1'
server_port = 5000
mac = '88:75:98:A6:33:C7'

b = BluetoothRSSI(addr=mac)
server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_sock.connect((server_ip, server_port))

while True:
	rssi = b.request_rssi()
	timestamp = time()
	print(rssi)
	msg = pickle.dumps({"mac_adr": mac, "timestamp": timestamp, "rssi": rssi})
	server_sock.send(msg)
	print ("---")
	print ("addr: {}, rssi: {}".format(mac, rssi))
    # Sleep and then skip to next iteration if device not found