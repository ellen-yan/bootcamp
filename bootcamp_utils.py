# Useful code snippets and functions from the bootcamp

# Plotting: seaborn settings
import numpy as np
import matplotlib.pyplot as plt

import seaborn as sns

# Based on personal preference, can alter the seaborn settings
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
          '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
          '#bcbd22', '#17becf']

sns.set(style='whitegrid', palette=colors, rc={'axes.labelsize': 16}) # overrides matplotlib settings for plots

# Empirical cumulative distribution function, to replace histograms without
# losing information (1D data)
def ecdf(data):
    x = sorted(data)
    y = np.arange(0, 1, 1/len(x))
    return x, y
