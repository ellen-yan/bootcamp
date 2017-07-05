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
def ecdf_v1(data):
    x = sorted(data)
    y = np.arange(0, 1, 1/len(x))
    return x, y

def ecdf(data, formal=False, buff=0.1, min_x=None, max_x=None):
    """
    Generate `x` and `y` values for plotting an ECDF.

    Parameters
    ----------
    data : array_like
        Array of data to be plotted as an ECDF.
    formal : bool, default False
        If True, generate `x` and `y` values for formal ECDF.
        Otherwise, generate `x` and `y` values for "dot"
    buff : float, default 0.1
        How long the tails at y = 0 and y = 1 should extend as a
        fraction of the total range of the data. Ignored if
        `formal` is False.
    min_x : float, default None
        Minimum value of `x` to include on plot. Overrides `buff`.
        Ignored if `formal` is False.
    max_x : float, default None
        Maximum value of `x` to include on plot. Overrides `buff`.
        Ignored if `formal` is False.

    Returns
    -------
    x : array
        `x` values for plotting
    y : array
        `y` values for plotting
    """
    x = np.array(sorted(data))
    y = np.arange(1/len(x), 1 + 0.5 * 1/len(x), 1/len(x))

    if not formal:
        return x, y

    r = np.max(x) - np.min(x)
    if not min_x and not max_x:
        min_x = np.min(x) - buff*r
        max_x = np.max(x) + buff*r

    x = np.array([min_x] + sorted(np.append(x, x)) + [max_x])
    y = np.array([0, 0] + sorted(np.append(y, y)))

    return x, y

def ecdf_plot(data, value, hue=None, formal=False, buff=0.1, min_x=None,
              max_x=None, ax=None):
    """
    Generate `x` and `y` values for plotting an ECDF.

    Parameters
    ----------
    data : Pandas DataFrame
        Tidy DataFrame with data sets to be plotted.
    value : column name of DataFrame
        Name of column that contains data to make ECDF with.
    hue : column name of DataFrame
        Name of column that identifies labels of data. A separate
        ECDF is plotted for each unique entry.
    formal : bool, default False
        If True, generate `x` and `y` values for formal ECDF.
        Otherwise, generate `x` and `y` values for "dot" style ECDF.
    buff : float, default 0.1
        How long the tails at y = 0 and y = 1 should extend as a
        fraction of the total range of the data. Ignored if
        `formal` is False.
    min_x : float, default None
        Minimum value of `x` to include on plot. Overrides `buff`.
        Ignored if `formal` is False.
    max_x : float, default None
        Maximum value of `x` to include on plot. Overrides `buff`.
        Ignored if `formal` is False.
    ax : matplotlib Axes
        Axes object to draw the plot onto, otherwise makes a new figure/axes.

    Returns
    -------
    output : matplotlib Axes
        Axes object containing ECDFs.
    """

    # Set up axes
    if ax is None:
        fig, ax = plt.subplots(1, 1)
        _ = ax.set_xlabel(str(value))
        _ = ax.set_ylabel('ECDF')

    if hue is None:
        x, y = ecdf(data[value], formal=formal, buff=buff, min_x=min_x,
                    max_x=max_x)
        # Make plots
        if formal:
            _ = ax.plot(x, y)
        else:
            _ = ax.plot(x, y, marker='.', linestyle='none')
    else:
        gb = data.groupby(hue)
        ecdfs = gb[value].apply(ecdf, formal=formal, buff=buff, min_x=min_x,
                                max_x=max_x)

        # Make plots
        if formal:
            for i, xy in ecdfs.iteritems():
                _ = ax.plot(*xy)
        else:
            for i, xy in ecdfs.iteritems():
                _ = ax.plot(*xy, marker='.', linestyle='none')

        # Add legend
        _ = ax.legend(ecdfs.index, loc=0)

    return ax
