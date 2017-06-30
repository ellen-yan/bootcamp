import numpy as np

# Pandas, conventionally imported as pd
import pandas as pd

# Plotting modules and settings.
import matplotlib.pyplot as plt
import seaborn as sns
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
          '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
          '#bcbd22', '#17becf']
sns.set(style='whitegrid', palette=colors, rc={'axes.labelsize': 16})

# Read in data file with pandas
df_high = pd.read_csv('data/xa_high_food.csv', comment='#', header=None)
df_low = pd.read_csv('data/xa_low_food.csv', comment='#', header=None)

# df_high is a DataFrame, and a single column, df_high[0], is a Series
# A Pandas Series is a generalized NumPy array. NumPy arrays are indexed with
# integers, but a Pandas Series may be indexed with anything.

def examples():
    # Dictionary of top men's World Cup scorers and how many goals
    wc_dict = {'Klose': 16,
               'Ronaldo': 15,
               'Müller': 14,
               'Fontaine': 13,
               'Pelé': 12,
               'Kocsis': 11,
               'Klinsmann': 11}

    # Create a Series from the Dictionary
    s_goals = pd.Series(wc_dict)

    # Take a look
    print(s_goals)

    # What if we wanted to add another Series?
    # Dictionary of nations
    nation_dict = {'Klose': 'Germany',
                   'Ronaldo': 'Brazil',
                   'Müller': 'Germany',
                   'Fontaine': 'France',
                   'Pelé': 'Brazil',
                   'Kocsis': 'Hungary',
                   'Klinsmann': 'Germany'}

    # Series with nations
    s_nation = pd.Series(nation_dict)

    # Look at it
    print(s_nation)

    # Combine two Series into a DataFrame,
    # keys are column headers and values are the series
    df_wc = pd.DataFrame({'nation': s_nation, 'goals': s_goals})
    print(df_wc)

    # Can't do this: df_wc['Fontaine']
    # Must use loc if we want the row with a specific 'index'
    print(df_wc.loc['Fontaine', :])
    # We can index by column directly
    print(df_wc['goals'])

    # Boolean indexing
    df_wc.loc[df_wc['nation'] == 'Germany', :]

examples()

# Change column headings
df_low.columns = ['low']
df_high.columns = ['high']

# Take a look
print(df_high)

## Tidy DataFrame rules (by Hadley Wickham):
## 1. Each variable is a column
## 2. Each observation is a row
## 3. Each type of observation has its own separate DataFrame

# Concatenate DataFrames
df = pd.concat((df_low, df_high), axis=1)
# See the result
print(df)

# Tidy the data (headers are their own variable)
df = pd.melt(df, var_name='food density',
             value_name='cross-sectional area (sq micron)').dropna()
print(df)

## Pulling out indices (rows) of data through boolean indexing
inds = (df['food density'] == 'high') & (df['cross-sectional area (sq micron)'] > 2000)
print(inds) # column of True and False
# Pull out areas
print(df.loc[inds, 'cross-sectional area (sq micron)'])

## Outputting a new CSV file
# Write out DataFrame (headers included)
df.to_csv('xa_combined.csv', index=False)
