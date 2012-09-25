#!/usr/bin/env python

from sys import argv
from math import sqrt

import numpy as np
import scipy.stats
import matplotlib
import matplotlib.pyplot as plt

from statepoint import StatePoint

# Create StatePoint object
sp1 = StatePoint('without-ufs.state')
sp2 = StatePoint('with-ufs.state')

sp1._get_int()
sp2._get_int()

# Calculate t-value for 95% two-sided CI
n = sp1.current_batch - sp1.n_inactive
t_value = scipy.stats.t.ppf(0.975, n - 1)

################################ WITHOUT UFS ###################################
for t in sp1.tallies:
    n_bins = t.n_score_bins * t.n_filter_bins
    i_mesh = [f.type for f in t.filters].index('mesh')

    # Get Mesh object
    m = sp1.meshes[t.filters[i_mesh].bins[0] - 1]
    nx, ny, nz = m.dimension
    ns = t.n_score_bins * t.n_filter_bins / (nx*ny*nz)

    # Create lists for tallies
    mean = np.zeros((nx,ny))
    error = np.zeros((nx,ny))
    criteria = np.zeros((nx,ny))

    # Determine starting position for data
    start = sp1._f.tell()

    for x in range(nx):
        for y in range(ny):
            # Seek to position of data
            sp1._f.seek(start + x*ny*nz*ns*16 + y*nz*ns*16)

            # Read sum and sum-squared
            s, s2 = sp1._get_double(2)
            s /= n
            mean[x,y] = s
            if s != 0.0:
                error[x,y] = t_value*sqrt((s2/n - s*s)/(n-1))/s

    # Make figure
    plt.imshow(error, interpolation="nearest", vmin=0.0, vmax=0.03)
    cb = plt.colorbar()
    [t.set_fontsize(16) for t in cb.ax.get_yticklabels()]
    plt.xlim((0,nx))
    plt.ylim((0,ny))
    plt.xticks(range(1), (''))
    plt.yticks(range(1), (''))
    plt.savefig('opr-without-ufs.pdf', bbox_inches='tight')
    plt.close()

################################# WITH UFS #####################################
for t in sp2.tallies:
    n_bins = t.n_score_bins * t.n_filter_bins
    i_mesh = [f.type for f in t.filters].index('mesh')

    # Get Mesh object
    m = sp2.meshes[t.filters[i_mesh].bins[0] - 1]
    nx, ny, nz = m.dimension
    ns = t.n_score_bins * t.n_filter_bins / (nx*ny*nz)

    # Create lists for tallies
    mean = np.zeros((nx,ny))
    error = np.zeros((nx,ny))
    criteria = np.zeros((nx,ny))

    # Determine starting position for data
    start = sp2._f.tell()

    for x in range(nx):
        for y in range(ny):
            # Seek to position of data
            sp2._f.seek(start + x*ny*nz*ns*16 + y*nz*ns*16)

            # Read sum and sum-squared
            s, s2 = sp2._get_double(2)
            s /= n
            mean[x,y] = s
            if s != 0.0:
                error[x,y] = t_value*sqrt((s2/n - s*s)/(n-1))/s

    # Make figure
    plt.imshow(error, interpolation="nearest", vmin=0.0, vmax=0.03)
    cb = plt.colorbar()
    [t.set_fontsize(16) for t in cb.ax.get_yticklabels()]
    plt.xlim((0,nx))
    plt.ylim((0,ny))
    plt.xticks(range(1), (''))
    plt.yticks(range(1), (''))
    plt.savefig('opr-with-ufs.pdf', bbox_inches='tight')
    plt.close()
