import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter

mu, sigma = 0, 500
x = np.arange(1, 5, 0.1)  # x axis
z = np.random.normal(mu, sigma, len(x))  # noise
y = x ** 2 + z  # data
# plt.plot(x, y, linewidth=2, linestyle="-", c="b")  # it include some noise

w = savgol_filter(y, 3, 2)
plt.plot(x, w, 'b')  # high frequency noise removed
plt.show()
