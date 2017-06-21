import numpy as np
import matplotlib.pyplot as plt
import scipy.stats

import seaborn as sns

# Based on personal preference, can alter the seaborn settings
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
          '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
          '#bcbd22', '#17becf']

sns.set(style='whitegrid', palette=colors, rc={'axes.labelsize': 16}) # overrides matplotlib settings for plots

def plot_log():
    # Load the data
    data = np.loadtxt('data/collins_switch.csv', skiprows=2, delimiter=',')

    x = data[:, 0] # IPTG mM
    y = data[:, 1] # normalized GFP expression
    sem = data[:, 2] # std error

    # Make and display the plot
    fig, ax = plt.subplots(1, 1)
    _ = ax.set_xscale('log')
    _ = ax.set_xlabel('[IPTG] (mM)')
    _ = ax.set_ylabel('normalized GFP intensity')
    #_ = ax.plot(x, y, marker='.', linestyle='none')

    # Set error bars
    _ = ax.errorbar(x, y, yerr=sem, marker='.', linestyle='none', markersize='10')
    plt.show()

def ecdf(data):
    x = sorted(data)
    y = np.arange(0, 1, 1/len(x))
    return x, y

def ecdf_plot():
    data = np.loadtxt('data/xa_low_food.csv', comments='#')
    x_low, y_low = ecdf(data)
    data = np.loadtxt('data/xa_high_food.csv', comments='#')
    x_high, y_high = ecdf(data)

    # Get theoretical CDF with means and std devs
    x = np.linspace(1600, 2500, 400)
    cdf_theor_low = scipy.stats.norm.cdf(x, loc=np.mean(x_low), scale=np.std(x_low))
    cdf_theor_high = scipy.stats.norm.cdf(x, loc=np.mean(x_high), scale=np.std(x_high))

    # Build figure and label axes
    fig, ax = plt.subplots(1, 1)
    _ = ax.set_xlabel('cross sectional area')
    _ = ax.set_ylabel('ECDF')

    _ = ax.plot(x, cdf_theor_low, color='gray', label='Theoretical low food')
    _ = ax.plot(x, cdf_theor_high, color='gray', label='Theoretical high food')
    _ = ax.plot(x_low, y_low, marker='.', label='Empirical low food')
    _ = ax.plot(x_high, y_high, marker='.', label='Empirical high food')

    _ = ax.legend(loc='lower right')

    plt.show()


#plot_log()
ecdf_plot()
