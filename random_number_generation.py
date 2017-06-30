import numpy as np
import scipy.stats

# Plotting modules and settings.
import matplotlib.pyplot as plt
import seaborn as sns
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
          '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
          '#bcbd22', '#17becf']
sns.set(style='whitegrid', palette=colors, rc={'axes.labelsize': 16})

def ecdf(data):
    """Generate x and y values for plotting an ECDF."""
    return np.sort(data), np.arange(1, len(data)+1) / len(data)

# Generate random numbers
x = np.random.random(size=100000)

# Make ECDF
x, y = ecdf(x)

# Plot CDF from random numbers (for plotting purposes, only plot 1000 points)
fig, ax = plt.subplots(1, 1)
_ = ax.plot(x[::1000], y[::1000], marker='.', linestyle='none', markersize=10)

# Plot expected CDF (just a straight line from (0,0) to (1,1))
_ = ax.plot([0, 1], [0, 1], 'k-')

plt.show()

# Seeding random number generators shows the algorithm is deterministic
# USEFUL WHEN UNIT TESTING!
np.random.seed(42)
print(np.random.random(size=10))
# Re-seed the RNG
np.random.seed(42)
print(np.random.random(size=10))

# Seed with a different number
np.random.seed(43)
print(np.random.random(size=10))

## Drawing random numbers out of other distributions, e.g. normal distn
# Set parameters
mu = 10
sigma = 1

# Draw 10000 random samples
x = np.random.normal(mu, sigma, size=10000)

# Plot a histogram of our draws
fig, ax = plt.subplots(1, 1)
_ = ax.hist(x, bins=50)
plt.show()

## Comparing resulting ECDF is a better way to see if it's normal

# Compute theoretical CDF
x_theor = np.linspace(6, 14, 400)
y_theor = scipy.stats.norm.cdf(x_theor, mu, sigma)

# Compute ECDF
x, y = ecdf(x)

# Make plot
fig, ax = plt.subplots(1, 1)
_ = ax.set_xlabel('x')
_ = ax.set_ylabel('CDF')
_ = ax.plot(x, y, marker='.', linestyle='none')
_ = ax.plot(x_theor, y_theor, color='gray')
plt.show()

## We can also draw from different distributions: binomial, geometric, poisson
print(np.random.binomial(10, 0.5)) # 10 flips, 0.5 probability

## Choosing elements from an array: np.random.choice has useful keyword replace,
## which allows us to specify whether we want to replace elements we choose.
np.random.seed(42)
print(np.random.randint(0, 51, size=20)) # sample 10 selected twice, sample 23 thrice
print(np.random.choice(np.arange(51), size=20, replace=False)) # no repeats

## Shuffling an array:
np.random.permutation(np.arange(53)) # e.g. a deck of cards
