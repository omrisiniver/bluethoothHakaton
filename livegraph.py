import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter

# mu, sigma = 0, 500
# x = np.arange(1, 5, 0.1)  # x axis
# z = np.random.normal(mu, sigma, len(x))  # noise
# print(len(x))
# y = x ** 2 + z  # data
# print(len(y))
# # plt.plot(x, y, linewidth=2, linestyle="-", c="b")  # it include some noise

import matplotlib.pyplot as plt
import numpy as np

import csv

with open('employee_file.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    x_values = []
    y_values =[]
    for row in csv_reader:
    	x_values.append(row[1])
    	y_values.append(row[0])

print(len(x_values))
mu, sigma = 0, 500
plt.plot(x_values, y_values, linewidth=2, linestyle="-", c="b")  # it include some noise

# w = savgol_filter(y, 501, 2)
# plt.plot(x, w, 'b')  # high frequency noise removed
plt.show()
