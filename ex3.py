import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate

import seaborn as sns

# Based on personal preference, can alter the seaborn settings
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
          '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
          '#bcbd22', '#17becf']

sns.set(style='whitegrid', palette=colors, rc={'axes.labelsize': 16}) # overrides matplotlib settings for plots

def fold_change(c, RK, KdA=0.017, KdI=0.002, Kswitch=5.8):
    """Takes in a given scalar/array concentration c and R/K scalar ratio RK,
    and computes the theoretical fold change."""
    return 1 / (1 + (RK * (1 + c/KdA)**2) / ((1 + c/KdA)**2 + Kswitch*(1 + c/KdI)**2))

def bohr_parameter(c, RK, KdA=0.017, KdI=0.002, Kswitch=5.8):
    """Given a concentration and ratio R/K, computes bohr parameter
    (array or scalar)."""
    return - np.log(RK) - np.log((1 + c/KdA)**2 / ((1 + c/KdA)**2 + Kswitch*(1 + c/KdI)**2))

def fold_change_bohr(bohr_parameter):
    """Given a bohr parameter, computes the fold change."""
    return 1 / (1 + np.exp(-bohr_parameter))

def ex3_2():
    """
    Exercise 3.2
    """
    # Load data into variables
    data = np.loadtxt('data/wt_lac.csv', comments='#', skiprows=3, delimiter=',')
    wt_x = data[:, 0] # IPTG mM
    wt_y = data[:, 1] # fold change
    data = np.loadtxt('data/q18m_lac.csv', comments='#', skiprows=3, delimiter=',')
    q18m_x = data[:, 0] # IPTG mM
    q18m_y = data[:, 1] # fold change
    data = np.loadtxt('data/q18a_lac.csv', comments='#', skiprows=3, delimiter=',')
    q18a_x = data[:, 0] # IPTG mM
    q18a_y = data[:, 1] # fold change

    # Build plot for fold change data (labels, legend, plot)
    fig, ax = plt.subplots(2, 1)
    _ = ax[0].set_xscale('log')
    _ = ax[0].set_xlabel('IPTG concentration (mM)')
    _ = ax[0].set_ylabel('Fold change in fluorescence')

    # Add experimental data to plot
    _ = ax[0].plot(q18a_x, q18a_y, label='q18a', marker='.', linestyle='none')
    _ = ax[0].plot(wt_x, wt_y, label='Wild Type', marker='.', linestyle='none')
    _ = ax[0].plot(q18m_x, q18m_y, label="q18m", marker='.', linestyle='none')

    # Calculate the theoretical fold change curves and add to plot
    RK_WT = 141.5
    RK_Q18A = 16.56
    RK_Q18M = 1332
    x = np.logspace(-5.2, 1.5)
    _ = ax[0].plot(x, fold_change(x, RK_Q18A), label='Theoretical q18a fold change')
    _ = ax[0].plot(x, fold_change(x, RK_WT), label='Theoretical wild type')
    _ = ax[0].plot(x, fold_change(x, RK_Q18M), label='Theoretical q18m fold change')

    _ = ax[0].legend(loc='upper left')

    # Build plot for data collapse with Bohr parameter
    _ = ax[1].set_xlabel('Bohr parameter')
    _ = ax[1].set_ylabel('Fold change')

    bohr_values = np.linspace(-6, 6, num=50)
    _ = ax[1].plot(bohr_values, fold_change_bohr(bohr_values), color='gray',
                   label='Universal Bohr Parameter')

    # Plot bohr parameter for experimental conditions
    wt_bohr = bohr_parameter(wt_x, RK_WT)
    q18a_bohr = bohr_parameter(q18a_x, RK_Q18A)
    q18m_bohr = bohr_parameter(q18m_x, RK_Q18M)

    _ = ax[1].plot(q18a_bohr, fold_change_bohr(q18a_bohr), marker='.',
                   label='q18a bohr parameters')
    _ = ax[1].plot(wt_bohr, fold_change_bohr(wt_bohr), marker='.',
                   label='wild type bohr parameters')
    _ = ax[1].plot(q18m_bohr, fold_change_bohr(q18m_bohr), marker='.',
                   label='q18m bohr parameters')

    _ = ax[1].legend(loc='upper left')

    plt.show()

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

def ex3_3():
    """Testing the ECDF function with some fake data and plotting
    the formal ECDF followed by the dot ECDF."""
    d = np.array([90, 103, 107, 130, 135, 138, 148, 205, 210])
    formalplot_x, formalplot_y = ecdf(d, formal=True)
    dotplot_x, dotplot_y = ecdf(d, formal=False)

    fig, ax = plt.subplots(1, 1)
    _ = ax.set_xlabel('time (years)')
    _ = ax.set_ylabel('ECDF')

    _ = ax.plot(formalplot_x, formalplot_y, label='Formal ECDF')
    _ = ax.plot(dotplot_x, dotplot_y, label='Dot ECDF', marker='.', linestyle='none')

    _ = ax.legend(loc='lower right')

    plt.show()

def ex3_4():
    """Simulating the Lotka-Volterra model numerically."""
    alpha = 1 # growth rate constant of rabbits
    beta = 0.2 # death rate constant of rabbits
    delta = 0.3 # growth rate constant of foxes
    gamma = 0.8 # death rate constant of foxes

    delta_t = 0.001
    t = np.arange(0, 60, delta_t)
    r = np.empty_like(t)
    f = np.empty_like(t)

    # Initial number of rabbits and foxes
    r[0] = 10
    f[0] = 1

    for i in range(1, len(t)):
        r[i] = r[i - 1] + delta_t * (alpha * r[i - 1] - beta * f[i - 1] * r[i - 1])
        f[i] = f[i - 1] + delta_t * (delta * f[i - 1] * r[i - 1] - gamma * f[i - 1])

    fig, ax = plt.subplots(1, 1)
    _ = ax.set_xlabel('time (units of $k^{-1}$)')
    _ = ax.set_ylabel('number of rabbits/foxes')
    _ = ax.plot(t, r, label='rabbit population')
    _ = ax.plot(t, f, label='fox population')

    _ = ax.legend(loc='upper right')

    plt.show()

def lotka_volterra_func(y, t, alpha, beta, gamma, delta):
    """Right hand side of Lotka-Volterra equation; y = (rabbits, foxes)"""
    # Unpack y
    r, f = y

    # Compute derivatives
    dr_dt = alpha * r - beta * f * r
    df_dt = delta * r * f - gamma * f

    return np.array([dr_dt, df_dt])

def ex3_4_extra():
    alpha = 1 # growth rate constant of rabbits
    beta = 0.2 # death rate constant of rabbits
    delta = 0.3 # growth rate constant of foxes
    gamma = 0.8 # death rate constant of foxes

    # Initial conditions
    y0 = np.array([10, 1])
    t = np.linspace(0, 60, 400)
    y = scipy.integrate.odeint(lotka_volterra_func, y0, t, args=(alpha, beta, gamma, delta))

    r = y[:, 0]
    f = y[:, 1]

    fig, ax = plt.subplots(1, 1)
    _ = ax.set_xlabel('Time (a.u.)')
    _ = ax.set_ylabel('population')
    _ = ax.plot(t, r, label='rabbit population')
    _ = ax.plot(t, f, label='fox population')
    _ = ax.legend(loc='upper right')

    plt.show()


#ex3_2()
#ex3_3()
#ex3_4()
ex3_4_extra()
