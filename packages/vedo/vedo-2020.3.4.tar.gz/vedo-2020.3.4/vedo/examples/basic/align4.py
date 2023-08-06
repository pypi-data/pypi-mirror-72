"""Align a set of curves in space
with Procrustes method
"""
import numpy as np
from vedo import *

splines = load(datadir+'splines.npy') # returns a list of Lines

procus = alignProcrustes(splines, rigid=0)
alignedsplines = procus.unpack() # unpack Assembly into a list
mean = procus.info['mean']
lmean = Line(mean, lw=4, c='b')

for l in alignedsplines:
    d = np.linalg.norm(l.points()-mean, axis=1)
    l.pointColors(d, cmap='hot_r', vmin=0, vmax=0.007)

alignedsplines.append(lmean.z(0.001)) # shift it to make it visible
alignedsplines.append(__doc__)

show([splines, alignedsplines], N=2, sharecam=False, axes=1)

        