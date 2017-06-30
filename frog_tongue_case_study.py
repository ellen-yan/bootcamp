import numpy as np
import pandas as pd

# Plotting modules and settings.
import matplotlib.pyplot as plt
import seaborn as sns
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
          '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
          '#bcbd22', '#17becf']
sns.set(style='whitegrid', palette=colors, rc={'axes.labelsize': 16})

# Load the data
df = pd.read_csv('data/frog_tongue_adhesion.csv', comment='#')
# Take a look
print(df)

# Slice out rows with big forces
df_big_force = df.loc[df['impact force (mN)'] > 1000, :]
print(df_big_force)
# note that indices correspond to measurements and not ordering in array

# Select a single experiment
print(df.loc[42, :])

# Selecting multiple columns
print(df.loc[:, ['impact force (mN)', 'adhesive force (mN)']])
# Specific columns for Frog I with boolean indexing
print(df.loc[df['ID'] == 'I', ['impact force (mN)', 'adhesive force (mN)']])

## Finding Correlations
fig, ax = plt.subplots(1, 1)
_ = ax.set_xlabel('impact force (mN)')
_ = ax.set_ylabel('adhesive force (mN)')
_ = ax.plot(df['impact force (mN)'], df['adhesive force (mN)'], marker='.',
            linestyle='none')

plt.show()

# Alternatively, we can use the DataFrame's built-in plot() method
print(df.plot(x='total contact area (mm2)', y='adhesive force (mN)', kind='scatter')) # ??
print(df.corr())

# We can change the headings
df = df.rename(columns={'impact force (mN)': 'impf'})
