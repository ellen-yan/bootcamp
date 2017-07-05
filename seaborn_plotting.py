import numpy as np
import pandas as pd

from bootcamp_utils import ecdf

# Plotting modules and settings.
import matplotlib.pyplot as plt
import seaborn as sns
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
          '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
          '#bcbd22', '#17becf']
sns.set(style='whitegrid', palette=colors, rc={'axes.labelsize': 16})

df = pd.read_csv('data/frog_tongue_adhesion.csv', comment='#')

def bar_plots():
    ## First use Matplotlib to try making a bar graph of the mean impact
    ## force for each frog with standard error of mean error bars

    # First method: using a for loop
    mean_impf = np.empty(4)
    sem_impf = np.empty(4)
    for i, frog in enumerate(df['ID'].unique()):
        mean_impf[i] = np.mean(df.loc[df['ID']==frog, 'impact force (mN)'])
        n = np.sum(df['ID']==frog)
        sem_impf[i] = np.std(df.loc[df['ID']==frog,
                                    'impact force (mN)']) / np.sqrt(n)

    print(mean_impf)
    print(sem_impf)

    # Better method: using groupby
    gb_frog = df.groupby('ID')
    mean_impf = gb_frog['impact force (mN)'].mean()
    sem_impf = gb_frog['impact force (mN)'].sem() # population sem calculation

    print(mean_impf)
    print(sem_impf)

    # Plot a bar graph using Matplotlib. We need to specify left edges of the
    # bars and their heights. Have to pass two kwargs to get error bars and
    # labels
    fig, ax = plt.subplots(1, 1)
    _ = ax.set_ylabel('impact force (mN)')

    # Turn off grid-lines for x-axis
    _ = ax.grid(False, axis='x')
    _ = ax.bar(np.arange(4), mean_impf, yerr=sem_impf,
               tick_label=['I', 'II', 'III', 'IV'])
    plt.show()

    ## Bar graphs with Seaborn
    # Plotting is much easier. We don't need for loops or groupbys, just
    # specify the x and y values and the DataFrame that is the source of our
    # data and Seaborn does the rest, as long as DataFrame is tidy
    ax = sns.barplot(data=df, x='ID', y='impact force (mN)', ci=68)
    _ = ax.set_xlabel('')
    _ = ax.set_ylabel('impact force (mN)')
    plt.show()
    # Note: the confidence interval kwarg is default at 95% (ci=95), so the
    # error bars look bigger than the first plot we made. Looked it up: for
    # std error of mean we should set ci=68

def bee_swarm_plots():
    # Useful to visualize the spread of data by plotting all the points
    ax = sns.swarmplot(data=df, x='ID', y='impact force (mN)')
    _ = ax.set_xlabel('')
    _ = ax.set_ylabel('impact force (mN)')
    plt.show()

    # We can shade the days with the hue kwarg (or shade based on any
    # other feature)
    ax = sns.swarmplot(data=df, x='ID', y='impact force (mN)', hue='date')
    _ = ax.set_xlabel('')
    _ = ax.set_ylabel('impact force (mN)')
    # Remove the legend
    _ = ax.legend_.remove()
    plt.show()

def box_plots():
    # A good alternative to a bee swarm plot if we have too many points
    ax = sns.boxplot(data=df, x='ID', y='impact force (mN)')
    _ = ax.set_xlabel('')
    _ = ax.set_ylabel('impact force (mN)')
    plt.show()

def ecdf_plots():
    # Justin: generally prefers plotting ECDFs to make comparisons
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
    ax = ecdf_plot(df, 'impact force (mN)', hue='ID', formal=True)
    plt.show()

#bar_plots()
#bee_swarm_plots()
#box_plots()
ecdf_plots()
