import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from bootcamp_utils import ecdf
from bootcamp_utils import ecdf_plot
#from bootstrap_exercises import draw_bs_reps

def ex4_1():

    df = pd.read_csv('data/frog_tongue_adhesion.csv', comment='#')
    df_frog = pd.DataFrame(index=['I', 'II', 'III', 'IV'],
                           data={'age': ['adult', 'adult', 'juvenile', 'juvenile'],
                                 'SVL (mm)': [63, 70, 28, 31],
                                 'weight (g)': [63.1, 72.7, 12.7, 12.7],
                                 'species': ['cross', 'cross', 'cranwelli', 'cranwelli']})

    df_frog['ID'] = df_frog.index

    # Merge DataFrames based on the column 'ID'
    df_combined = pd.DataFrame.merge(df, df_frog, on='ID')
    print(df_combined)

def ex4_2_wrangling():
    df_1973 = pd.read_csv('data/grant_1973.csv', comment='#')
    df_1975 = pd.read_csv('data/grant_1975.csv', comment='#')
    df_1987 = pd.read_csv('data/grant_1987.csv', comment='#')
    df_1991 = pd.read_csv('data/grant_1991.csv', comment='#')
    df_2012 = pd.read_csv('data/grant_2012.csv', comment='#')

    # Rename yearband column to year in 1973 data and replace with four digits
    df_1973.rename(columns={'yearband':'year'}, inplace=True)
    df_1973.loc[:, 'year'] = 1973

    # Add a year column to the other four dataframes
    df_1975['year'] = 1975
    df_1987['year'] = 1987
    df_1991['year'] = 1991
    df_2012['year'] = 2012

    # Rename columns in all data sets so they're consistent
    df_1973.rename(columns={'beak length': 'beak length (mm)',
                            'beak depth': 'beak depth (mm)'}, inplace=True)
    df_1975.rename(columns={'Beak length, mm': 'beak length (mm)',
                            'Beak depth, mm': 'beak depth (mm)'}, inplace=True)
    df_1987.rename(columns={'Beak length, mm': 'beak length (mm)',
                            'Beak depth, mm': 'beak depth (mm)'}, inplace=True)
    df_1991.rename(columns={'blength': 'beak length (mm)',
                            'bdepth': 'beak depth (mm)'}, inplace=True)
    df_2012.rename(columns={'blength': 'beak length (mm)',
                            'bdepth': 'beak depth (mm)'}, inplace=True)

    # Remove duplicate band numbers (i.e. birds) from each dataframe
    # Default keeps first occurrence, keep='first'
    df_1973.drop_duplicates(subset='band', inplace=True)
    df_1975.drop_duplicates(subset='band', inplace=True)
    df_1987.drop_duplicates(subset='band', inplace=True)
    df_1991.drop_duplicates(subset='band', inplace=True)
    df_2012.drop_duplicates(subset='band', inplace=True)

    # Concatenate the DataFrames
    df_combined = pd.concat([df_1973, df_1975, df_1987, df_1991, df_2012],
                            ignore_index=True)

    # Save the tidy DataFrame to a new csv file
    df_combined.to_csv(path_or_buf='data/grant_selfcombined.csv', index=False)

def ex4_2_analysis():
    YEARS = [1973, 1975, 1987, 1991, 2012]
    df = pd.read_csv('data/grant_selfcombined.csv')

    # Plot an ECDF of beak depths of Geospiza fortis specimens measured in
    # 1987. Plot an ECDF of the beak depths of Geospiza scandens from the
    # same year on the same plot.
    df_1987 = df.loc[df['year'] == 1987, :]
    ax1 = ecdf_plot(df_1987, 'beak depth (mm)', 'species')

    # On the same plot, plot an ECDF of the beak lengths of Geospiza fortis
    # and Geospiza scandens in 1987.
    ax2 = ecdf_plot(df_1987, 'beak length (mm)', 'species')
    plt.show()

    # Plot beak depth vs. beak width for 1987 data, Geospiza fortis as blue
    # dots and Geospiza scandens as red dots
    fig, ax = plt.subplots(1, 1)
    _ = ax.plot(df_1987.loc[df_1987['species'] == 'fortis',
                            'beak length (mm)'],
                df_1987.loc[df_1987['species'] == 'fortis',
                            'beak depth (mm)'],
                marker='.', color='#1f77b4', linestyle='none', label='fortis')
    _ = ax.plot(df_1987.loc[df_1987['species'] == 'scandens',
                            'beak length (mm)'],
                df_1987.loc[df_1987['species'] == 'scandens',
                            'beak depth (mm)'],
                marker='.', color='#d62728', linestyle='none', label='scandens')
    _ = ax.set_xlabel('beak length (mm)')
    _ = ax.set_ylabel('beak depth (mm)')

    _ = ax.legend(loc='lower right')
    plt.show()

    # Repeating the scatter plots for all the years
    fig, ax = plt.subplots(1, 5, sharex=True)
    for i in range(len(YEARS)):
        df_subset = df.loc[df['year'] == YEARS[i], :]
        _ = ax[i].plot(df_subset.loc[df_subset['species'] == 'fortis',
                                'beak length (mm)'],
                    df_subset.loc[df_subset['species'] == 'fortis',
                                'beak depth (mm)'],
                    marker='.', color='#1f77b4', linestyle='none',
                    label=('fortis' + str(YEARS[i])))
        _ = ax[i].plot(df_subset.loc[df_subset['species'] == 'scandens',
                                'beak length (mm)'],
                    df_subset.loc[df_subset['species'] == 'scandens',
                                'beak depth (mm)'],
                    marker='.', color='#d62728', linestyle='none',
                    label='scandens' + str(YEARS[i]))
        _ = ax[i].set_xlabel('beak length (mm)')
        _ = ax[i].set_ylabel('beak depth (mm)')

        _ = ax[i].legend(loc='lower right')
    plt.show()

def ex4_3():
    # Load files
    df_weight = pd.read_csv('data/bee_weight.csv', comment='#')
    df_sperm = pd.read_csv('data/bee_sperm.csv', comment='#')

    # Plot ECDFs of the drone weight for control and also for those
    # exposed to pesticide
    ax1 = ecdf_plot(df_weight, 'Weight', 'Treatment')

    bs_mean = draw_bs_reps(df_weight['Weight'], size=len(df_weight['Weight']))
    conf_interval = np.percentile(bs_mean, [2.5, 97.5])
    print("Confidence interval on bee weight:", conf_interval)

    # Plot ECDFs of the drone sperm quality for control and also for those
    # exposed to pesticide
    df_sperm.sort_values('Treatment', inplace=True)
    df_sperm.dropna(inplace=True)
    ax2 = ecdf_plot(df_sperm, 'Quality', 'Treatment')

    bs_mean = draw_bs_reps(df_sperm['Quality'], size=len(df_sperm['Quality']))
    conf_interval = np.percentile(bs_mean, [2.5, 97.5])
    print("Confidence interval on bee sperm quality:", conf_interval)

    # Repeat the bootstrap confidence intervals with median to
    # avoid the skew of the mean due to outliers
    bs_median = draw_bs_reps(df_sperm['Quality'], func=np.median,
                             size=len(df_sperm['Quality']))
    conf_interval = np.percentile(bs_median, [2.5, 97.5])
    print("Confidence interval on bee sperm quality with median:", conf_interval)

    plt.show()

def ex4_4():

    def backtrack_steps(pos):
        """
        The number of steps it takes for a random walker starting
        at position 0 to get to position=pos or greater.
        """
        # Current position; starts at 0
        x = 0

        # The number of steps
        n = 0

        # Randomly step left (-1) or right (+1) until position reached
        while (x < pos):
            step = int(np.round(np.random.rand()))
            if step == 0:
                step = -1
            x += step
            n += 1

        return n

    # Generate 10000 backtracks to position +1
    backtrack_times = []
    for i in range(0, 1000):
        backtrack_times.append(backtrack_steps(1))
        print(i)

    # Use plt.hist() to plot a histogram of the backtrack times
    plt.hist(backtrack_times, normed=True)
    plt.show()

    # Generate an ECDF of samples and plot the ECDF with x axis on
    # a logarithmic scale
    x, y = ecdf(backtrack_times)
    fig, ax = plt.subplots(1, 1)
    _ = ax.set_xscale('log')
    _ = ax.plot(x, y, marker='.')

    # Plot the complementary cumulative distribution function on a
    # log-log plot
    y_ccdf = 1 - y
    fig, ax1 = plt.subplots(1, 1)
    _ = ax1.set_xscale('log')
    _ = ax1.set_yscale('log')
    _ = ax1.plot(x, y_ccdf, marker='.')

    plt.show()


#ex4_1()
#ex4_2_wrangling()
#ex4_2_analysis()
#ex4_3()
ex4_4()
