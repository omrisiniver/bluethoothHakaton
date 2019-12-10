from bt_proximity import BluetoothRSSI
# from bluetooth import _bluetooth
import bluetooth
import sys
import struct
import bluetooth._bluetooth as bluez  # low level bluetooth wrappers

print("before discover_devices")
nearby_devices = bluetooth.discover_devices(lookup_names=True)
print("Found {} devices.".format(len(nearby_devices)))

for addr, name in nearby_devices:
    print("  {} - {}".format(addr, name))

print(nearby_devices[0][0])
b = BluetoothRSSI(addr=str(nearby_devices[0][0]))

while True:
    rssi = b.request_rssi()
    print ("---")
    print ("addr: {}, rssi: {}".format(addr, rssi))
    # Sleep and then skip to next iteration if device not found