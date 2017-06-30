import numpy as np
import pandas as pd

df = pd.read_csv('data/frog_tongue_adhesion.csv', comment='#')

def practice1():
    """Practice using .loc method."""
    # Extract the impact time of all impacts that had adhesive strength of
    # magnitude greater than 2000 Pa
    df_high_adhesive = df.loc[np.abs(df['adhesive strength (Pa)']) > 2000, 'impact time (ms)']
    print(df_high_adhesive)

    # Extract the impact force and adhesive force for all of Frog II's strikes
    df_frog_II = df.loc[df['ID'] == 'II', ['impact force (mN)', 'adhesive force (mN)']]
    print(df_frog_II)

    # Extract the adhesive force and the time the frog pulls on the target
    # for juvenile frogs (Frogs III and IV)
    df_juvenile = df.loc[df['ID'].isin(['III', 'IV']),
                         ['adhesive force (mN)', 'time frog pulls on target (ms)']]
    print(df_juvenile)

def intro_to_groupby():
    """Using groupby() to implement the split-apply-combine idea."""
    ## Computing the mean impact force of each frog the "long way"
    means = []
    frog_id = ['I', 'II', 'III', 'IV']
    for i in range(4):
        means.append(np.mean(df.loc[df['ID'] == frog_id[i], 'impact force (mN)']))

    # Alternative to the above, using list comprehension and including frog IDs
    [(frog_id, np.mean(df.loc[df['ID']==frog_id, 'impact force (mN)'])) for frog_id in df['ID'].unique()]

    ## Using grouby eliminates the hassle
    # Make a groupby object
    gb = df.groupby('ID')

    # Apply the np.mean function to the grouped object
    df_mean = gb.apply(np.mean)
    print(df_mean)

    # We can now pull the mean impact force for a frog of interest using loc
    print(df_mean.loc['III', 'impact force (mN)'])

    # If we want more information, like both the mean and the median, we can
    # apply multiple functions to a GroupBy object using agg(); argument is a
    # list of functions you want to apply
    df_mean_median = gb.agg([np.mean, np.median])
    print(df_mean_median)

    # We now have a MultiIndex for the column headers; index with tuples
    print(df_mean_median.loc[:, ('impact force (mN)', 'median')])

def practice2():
    """Practice with groupby()."""
    # Compute the standard deviations of the impact forces for each frog
    gb = df.groupby('ID')
    df_stdev = gb.apply(np.std)
    print(df_stdev)

    # Compute the coefficient of variation of the impact forces and the
    # adhesive forces for each frog
    gb_impact_adhesive = df.loc[:, ['ID', 'impact force (mN)',
                                    'adhesive force (mN)']].groupby('ID')
    df_coeff_of_var = gb_impact_adhesive.apply(coeff_of_var)
    print(df_coeff_of_var)

    # Compute a DataFrame that has the mean, median, standard deviation, and
    # coefficient of variation of the impact forces and adhesive forces for
    # each frog
    df_mean_med_std_coeff = gb_impact_adhesive.agg([np.mean,
                                                    np.median,
                                                    np.std,
                                                    coeff_of_var])
    print(df_mean_med_std_coeff)

    # Tidy up by using pd.melt()
    # First make the index (frog ID) column of DataFrame (otherwise cannot
    # refer to column 'ID')
    df_mean_med_std_coeff['ID'] = df_mean_med_std_coeff.index
    df_mean_med_std_coeff = pd.melt(df_mean_med_std_coeff,
                                    var_name=['quantity', 'statistic'],
                                    id_vars='ID')
    print(df_mean_med_std_coeff)

def coeff_of_var(data):
    """Computes the coefficient of variation of a data set. This is the
    standard deviation divided by the absolute value of the mean."""
    return np.std(data) / np.abs(np.mean(data))




#practice1()
#intro_to_groupby()
practice2()
