import numpy as np
import matplotlib.pyplot as plt

import seaborn as sns

# Based on personal preference, can alter the seaborn settings
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
          '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
          '#bcbd22', '#17becf']

sns.set(style='whitegrid', palette=colors, rc={'axes.labelsize': 16}) # overrides matplotlib settings for plots

x = np.linspace(-2*np.pi, 2*np.pi, 100)
y = np.sin(x)

# Set up plot
fig, ax = plt.subplots(1, 1)

_ = ax.set_xlabel('x')
_ = ax.set_ylabel('sin(x)')
_ = ax.set_xticks(np.pi*np.array([-2, -1, 0, 1, 2]))
_ = ax.set_xticklabels(['-2π', '-π', '0', 'π', '2π'])
# pi sign: alt + p
# comment out a section of code: command + /
# "Paint" the data
_ = ax.plot(x, y, marker='.', linestyle='none')

plt.show()
