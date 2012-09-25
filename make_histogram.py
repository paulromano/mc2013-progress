#!/usr/bin/env python

from sys import argv
from math import sqrt

import scipy.stats
import matplotlib.pyplot as plt
import numpy as np

from statepoint import StatePoint

# Create StatePoint object
sp1 = StatePoint('without-ufs.state')
sp2 = StatePoint('with-ufs.state')

# Calculate t-value for 95% two-sided CI
n = sp1.current_batch - sp1.n_inactive
t_value = scipy.stats.t.ppf(0.975, n - 1)

# Get uncertainties for without UFS
sp1.read_values()
unc1 = []
for s, s2 in sp1.tallies[0].values[:,0,:]:
    s /= n
    if s != 0.0:
        relative_error = t_value*sqrt((s2/n - s*s)/(n-1))/s
        unc1.append(relative_error)

# Get uncertainties for with UFS
sp2.read_values()
unc2 = []
for s, s2 in sp2.tallies[0].values[:,0,:]:
    s /= n
    if s != 0.0:
        relative_error = t_value*sqrt((s2/n - s*s)/(n-1))/s
        unc2.append(relative_error)

# Plot histogram
plt.hist(unc1, bins=100, histtype='step', label='Without UFS')
plt.hist(unc2, bins=100, histtype='step', label='With UFS')
plt.xlabel('Relative error', fontsize=16)
plt.ylabel('Number of bins', fontsize=16)
plt.legend()
plt.grid(True)
plt.savefig('opr-histogram.pdf', bbox_inches='tight')
