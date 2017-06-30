import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Based on personal preference, can alter the seaborn settings
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
          '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
          '#bcbd22', '#17becf']

sns.set(style='whitegrid', palette=colors, rc={'axes.labelsize': 16}) # overrides matplotlib settings for plots

def draw_bs_reps(data, func=np.mean, size=1):
    """
    Generates bootstrap replicates.

    Parameters
    ----------
    data : array_like
        Array of data from which to draw replicates.
    func : a function that takes in an array, default np.mean
        Function that takes in an array and returns a statistic.
        Examples: np.mean, np.std, np.median
    size : int, default 1
        The number of replicates to generate.

    Returns
    -------
    A Numpy array of replicates with func applied to each replicate.
    """

    n = len(data)
    return np.array([func(np.random.choice(data, replace=True, size=n)) for _ in range(size)])

def ecdf(data):
    """Generate x and y values for plotting an ECDF."""
    return np.sort(data), np.arange(1, len(data)+1) / len(data)

# Load data on the beak depths of finches on Galapagos island
bd_1975 = np.loadtxt('data/beak_depth_scandens_1975.csv')
bd_2012 = np.loadtxt('data/beak_depth_scandens_2012.csv')

x_1975, y_1975 = ecdf(bd_1975)
x_2012, y_2012 = ecdf(bd_2012)

# Build plot with ECDF of data
fig, ax = plt.subplots(1, 1)
_ = ax.set_xlabel('beak depth (mm)')
_ = ax.set_ylabel('ECDF')
_ = ax.plot(x_1975, y_1975, color='#1f77b4', label='1975', marker='.')
_ = ax.plot(x_2012, y_2012, color='#2ca02c', label='2012', marker='.')

# Add to plot the ECDF of repeated bootstrap replicates
for _ in range(100):
    sample = np.random.choice(bd_1975, replace=True, size=len(bd_1975))
    x, y = ecdf(sample)
    _ = ax.plot(x, y, color='#d62728', marker='.', alpha=0.01) # alpha=0 is transparent
    sample = np.random.choice(bd_2012, replace=True, size=len(bd_2012))
    x, y = ecdf(sample)
    _ = ax.plot(x, y, color='#d62728', marker='.', alpha=0.01)

_ = ax.legend(loc='lower right')

plt.show()
