# -*- coding: utf-8 -*-
#
# mat2HLbin.py

#import h5py
import hdf5storage
import matplotlib.cm as mp
import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sc
import struct

##################################################################
# functions
##################################################################

def read_bin(fname):
  f1 = open(fname, 'rb') # open the binary file
  # get the vertices
  nverts = struct.unpack('i', f1.read(4))[0]
  verts = np.empty([nverts, 3])
  for i in range(nverts):
    verts[i] = struct.unpack('fff', f1.read(12))
  f1.close # close the binary file 
  return verts

# get the reduced indices (for hololens vis)
def get_reduced_indices(fname):
  f1 = open(fname, 'rb')
  nidx = struct.unpack('i', f1.read(4))[0]
  idx = np.zeros((nidx, 1), dtype=np.int32)
  for i in range(nidx):
    idx[i] = struct.unpack('i', f1.read(4))[0]
  f1.close
  return idx

# write for hololens vis data file
def write_4HL(fname, verts, c_data, min, max, cm):
  f1 = open(fname, 'wb')
  f1.write(struct.pack('i', verts.shape[0]))
  for x in verts:
    f1.write(struct.pack('fff', x[0], x[1], x[2]))
  f1.write(struct.pack('i', c_data.shape[1]))
  for x in c_data:
    f1.write(struct.pack('f', x[0]))
  f1.write(struct.pack('f', min))
  f1.write(struct.pack('f', max))
  f1.write(struct.pack('i', cm.shape[0]))
  for x in cm:
    f1.write(struct.pack('fff', x[0], x[1], x[2]))
  f1.close
  return

##################################################################
# main program
##################################################################


# read matlab data file

#dist_name = 'cell1_sol.mat'
#print 'matlab data file: ' + dist_name 
#dist = hdf5storage.loadmat(dist_name)
#print 'keys:', dist.keys()
#dist_key = 'c_tot'

dist_name = 'Ind_Cell_FFR.mat'
print 'matlab data file: ' + dist_name 
dist = sc.loadmat(dist_name)
print 'keys:', dist.keys()
dist_key = 'MAT_FFR'

flow_data = dist[dist_key]
dims = flow_data.shape
print dims
for row in range(dims[0]):
  for col in range(dims[1]):
    print '{:6d}'.format(flow_data[row, col].shape[0]),
  print

print flow_data[1, 0].min()
print flow_data[1, 0].max()


### create a colormap
##ncolors = 1000
##cmap = mp.get_cmap("coolwarm",ncolors) # get a matplotlib color map
##cm = np.zeros([ncolors, 4])
##for i in range(ncolors): # convert colormap lut to numpy array
##  cm[i] = cmap(i)
##cm = cm[:,0:3] # don't need alpha

### read cell data and write hololens files
##for cell_num in range(1,8):
##  print
##  print 'cell number: ', cell_num
##  fname = '4sim_out_N4_p3-p2-p4-' + str(cell_num) + 'tet.bin'
##  print 'mesh file: ' + fname
##  verts = read_bin(fname)

##  fname = 'reduced-indices_out_N4_p3-p2-p4-' + str(cell_num) + "tet.bin"
##  print 'reduced indices file: ' + fname
##  idx = get_reduced_indices(fname) # zero indexed
##  rverts = verts[idx[:,0]]
##  print 'vertex reduction:', verts.shape[0], '->', idx.shape[0]

##  c_data = node_data[0, cell_num-1]
##  c_data = c_data[idx[:,0]]
##  print 'min:', '{:0.3f}'.format(c_data.min()),
##  print 'max:', '{:0.3f}'.format(c_data.max())

##  fname = '4HL_Cell' + str(cell_num) + ".bin"
##  min = 0.0
##  max = 5.0
##  write_4HL(fname, rverts, c_data[:,500:1100], min, max, cm)
##  #plt.plot(np.transpose(c_data[0:10,:]))

#plt.show()

