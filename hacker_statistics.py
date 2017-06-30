import numpy as np

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

# Load data on the beak depths of finches on Galapagos island
bd_1975 = np.loadtxt('data/beak_depth_scandens_1975.csv')
bd_2012 = np.loadtxt('data/beak_depth_scandens_2012.csv')

# Compute the ECDFs for 1975 and 2012
x_1975, y_1975 = ecdf(bd_1975)
x_2012, y_2012 = ecdf(bd_2012)

# Plot the ECDFs
fig, ax = plt.subplots(1, 1)
_ = ax.set_xlabel('beak depth (mm)')
_ = ax.set_ylabel('ECDF')
_ = ax.plot(x_1975, y_1975, marker='.', linestyle='none')
_ = ax.plot(x_2012, y_2012, marker='.', linestyle='none')
_ = ax.legend(('1975', '2012'), loc='lower right')
plt.show()

## Bootstrap confidence interval: simulate repeated experiments to obtain means
## from many simulations, and use that to get the 95% confidence interval
## The way it works: we draw data points out of the ORIGINAL data set
## WITH REPLACEMENT. This is called a bootstrap sample. Compute the mean to get
## a bootstrap mean.

def bs_replicate(data, func=np.mean):
    """Compute a boostrap replicate from data."""
    bs_sample = np.random.choice(data, size=len(data))
    return func(bs_sample)

# Number of replicas
n_reps = 100000

# Initialize bootstrap replicas array
bs_reps_1975 = np.empty(n_reps)

# Compyte replicates
for i in range(n_reps):
    bs_sample = np.random.choice(bd_1975, replace=True, size=len(bd_1975))
    bs_reps_1975[i] = np.mean(bs_sample)

# Compute ECDF of bootstrap sample
x_bs, y_bs = ecdf(bs_sample)
fig, ax = plt.subplots(1, 1)
_ = ax.set_xlabel('beak depth (mm)')
_ = ax.set_ylabel('ECDF')
_ = ax.plot(x_1975, y_1975, marker='.', linestyle='none')
_ = ax.plot(x_bs, y_bs, marker='.', linestyle='none')
_ = ax.legend(('1975', 'bootstrap'), loc='lower right')
plt.show()

# Compute ECDF of means
x, y = ecdf(bs_reps_1975)

# Plot the ECDF
fig, ax = plt.subplots(1, 1)
_ = ax.set_xlabel('mean beak depth (mm)')
_ = ax.set_ylabel('ECDF')
_ = ax.plot(x, y, marker='.', linestyle='none')
plt.show()

# Compyte the 95% confidence interval
conf_int_1975 = np.percentile(bs_reps_1975, [2.5, 97.5])
print('Confidence interval for 1975 mean:', conf_int_1975)

# Alternative way of computing confidence intervals using list comprehension
bs_reps_1975 = np.array([bs_replicate(bd_1975, func=np.mean) for _ in range(n_reps)])
bs_reps_2012 = np.array([bs_replicate(bd_2012, func=np.mean) for _ in range(n_reps)])
conf_int_2012 = np.percentile(bs_reps_2012, [2.5, 97.5])
print('Confidence interval for 2012 mean:', conf_int_2012)

# Computing standard error of the mean in two ways
bs_sem = np.std(bs_reps_1975)
print('Standard error of the mean (1975) directly from bootstrap means:', bs_sem)
sem = np.std(bd_1975, ddof=1) / np.sqrt(len(bd_1975))
print('Standard error of the mean (1975) from the mean of the data:', sem)

## Bootstrap confidence intervals for any statistic we like, e.g. std dev

# Compute replicates
bs_reps_1975 = np.array([bs_replicate(bd_1975, func=np.std) for _ in range(n_reps)])

# Compute confidence interval
conf_int_1975 = np.percentile(bs_reps_1975, [2.5, 97.5])
print('Confidence interval (1975) of bootstrap standard deviation', conf_int_1975)

# Compute ECDF
x, y = ecdf(bs_reps_1975)

# Plot the ECDF
fig, ax = plt.subplots(1, 1)
_ = ax.set_xlabel('st. dev. beak depth (mm)')
_ = ax.set_ylabel('ECDF')
_ = ax.plot(x, y, marker='.', linestyle='none')
plt.show()
