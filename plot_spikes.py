import numpy as np
import matplotlib.pyplot as plt

import seaborn as sns

# Based on personal preference, can alter the seaborn settings
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
          '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
          '#bcbd22', '#17becf']

sns.set(style='whitegrid', palette=colors, rc={'axes.labelsize': 16}) # overrides matplotlib settings for plots

# Load the data
data = np.loadtxt('data/retina_spikes.csv', skiprows=2, delimiter=',')

# Slice out the time and voltage
t = data[:, 0]
v = data[:, 1]

# Build the figure
fig, ax = plt.subplots(1, 1, figsize=(10, 3)) # figsize sets window size in inches
_ = ax.set_xlabel('t (ms)')
_ = ax.set_ylabel('V (µV)')

# Paint the plot
_ = ax.plot(t, v)

plt.show()
