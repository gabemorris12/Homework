import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

plt.style.use('maroon_py.mplstyle')

df = pd.read_csv('data/One.csv', index_col='index')
counts = np.array(df.index)
time = counts/30

z_interp = interp1d(time, df['z'], kind='cubic')
t = np.linspace(time[0], time[-1], 1000)
plt.plot(t, z_interp(t))
plt.xlabel('Time (s)')
plt.ylabel('Z Acceleration (G)')
plt.show()
