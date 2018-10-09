# -*- coding: utf-8 -*-
#
# mat2HLbin.py

import matplotlib.cm as mp
import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sc
import struct

import read_write as rw

##################################################################
# functions
##################################################################

# write lumen line segments to hololens file
def write_lsegs_4HL(f, lsegs):
  f.write(struct.pack('i', lsegs.shape[0]))                      # segment count
  for seg in lsegs:
    f.write(struct.pack('f', np.linalg.norm(seg[1] - seg[0])))   # length
    f.write(struct.pack('fff', seg[0][0], seg[0][1], seg[0][2])) # offset xyz
    f.write(struct.pack('fff', 0.0, 0.0, 0.0))                   # angle xyz
  return

# write lumen flow data to hololens file
def write_fdata_4HL(start, finish, stride, f, fdata):
  count = fdata[0][0][start:finish:stride].shape[0] # time step count     
  print 'time steps:', count
  f.write(struct.pack('i', count))
  for seg in fdata:
    trim = seg[0][start:finish:stride]
    for t in trim:
      f.write(struct.pack('f', t))                  # flow rate (per segment)
  return

##################################################################
# main program
##################################################################

hname = '4HL/4HL_Lumen.bin'
tname = 'lumen/tree.txt'
fname = 'lumen/Flow_Rate_Per_Line.mat'
dist_key = 'FF'

# create hololens file
f1 = open(hname, 'wb')

# write lumen tree data
print 'lumen tree file: ' + tname
write_lsegs_4HL(f1, rw.read_lumen(tname))

# write flow data
print 'matlab data file: ' + fname
dist = sc.loadmat(fname)
#print 'keys:', dist.keys()
write_fdata_4HL(11500, 31500, 30, f1, dist[dist_key])

# close hololens file
f1.close()


