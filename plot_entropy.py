#!/usr/bin/env python

import matplotlib.pyplot as plt

entropy = []
entropy_cmfd = []

for line in open('entropy', 'r'):
    entropy.append(float(line))
for line in open('entropy_cmfd', 'r'):
    entropy_cmfd.append(float(line))

batch = range(len(entropy))

plt.plot(batch, entropy, label='No CMFD')
plt.plot(batch, entropy_cmfd, label='CMFD')
plt.ticklabel_format(style='plain')
plt.ylim(15.29, 15.32)
locs,labels = plt.yticks()
plt.yticks(locs, map(lambda x: "{0:.3f}".format(x), locs))
plt.xlabel('Batch', fontsize=16)
plt.ylabel('Shannon Entropy', fontsize=16)
plt.grid(True, which='both')
plt.legend()
plt.savefig('entropy.pdf', bbox_inches='tight')
