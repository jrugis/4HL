#
# Convert parotid simulation output 
#    to hololens visualisation (cell node) data files 
#

import matplotlib.cm as mp
import numpy as np
import os
import struct
import subprocess
import sys

import read_write as rw

##################################################################
# functions
##################################################################

# create a colormap binary file 
def create_cm(ncolors):
  cmap = mp.get_cmap("coolwarm",ncolors) # get a matplotlib color map
  cm = np.zeros([ncolors, 4])
  for i in range(ncolors): # convert colormap to numpy array
    cm[i] = cmap(i)
  return cm[:,0:3] # don't need alpha

# reduced nodes for hololens
def reduce_nodes(verts, tris):
  rvertsi = np.array([range(1, verts.shape[0]+1)], dtype=int) # all vert indices
  rvertsi = np.setdiff1d(rvertsi, tris) # remove surface tri indices
  rvertsi -= 1; # change to zero indexed
  nverts = 0.6 * verts # node reduction factor

  nverts = nverts - np.min(nverts, axis=0) # normalise all verts to non-negative 
  max = (np.max(nverts, axis=0)) # get the range of vertex values

  # create a 4D grid (as an array) for extracting a uniform spatial vertex subset
  # - stores distance to nearest vertex (dnv) and the associated vertex index at each grid point
  # - the integer parts of every vertex coordinate are used to index the grid 
  vgrid = np.zeros((np.concatenate((np.floor(max+1),[2])).astype(int)))
  toohigh = 1000000 # high dummy values for dnv and index
  vgrid.fill(toohigh) 

  ifverts = np.modf(nverts) # get the integer and fractional part of all nverts

  # iterate through rvertsi and store the vert that is closest to each (integer) grid point
  for i in rvertsi:
    dist = np.linalg.norm(ifverts[0][i])
    vgridi = (ifverts[1][i]).astype(int) # grid index is simply the vertex location integer part
    if dist > 0.5: # don't bother with grid points that have no close vertex
      continue
    noise = 0.3 * np.random.ranf() # some spatial dithering to break up an aligned visual
    dist += noise

    # is this vertex closest to the grid point?
    if dist < vgrid[vgridi[0]][vgridi[1]][vgridi[2]][0]: 
      vgrid[vgridi[0]][vgridi[1]][vgridi[2]][0] = dist # store the new closer distance
      vgrid[vgridi[0]][vgridi[1]][vgridi[2]][1] = i # update the associated vertex index

  # extract the close vertex indices
  cvi = vgrid[:,:,:,1]
  cvi = np.extract(cvi < toohigh, cvi)
  return cvi.astype(int)

# write hololens vis data file
def write_4HL(fname, verts, rni, c_data, min, max):
  f1 = open(fname, 'wb')
  f1.write(struct.pack('i', rni.shape[0]))
  rverts = verts[rni]
  for x in rverts:
    f1.write(struct.pack('fff', x[0], x[1], x[2]))
  f1.write(struct.pack('i', c_data.shape[1]))
  for r in c_data:
    for c in r:
      f1.write(struct.pack('f', c))
  f1.close
  return

# get calcium data for reduced nodes
def get_c_data(verts, rni):
  nodes = rni.shape[0]
  steps = 600
  c_data = np.zeros([nodes, steps])
  for i in range(steps):
    c_data[:, i] = (1.0 + np.sin(i/12.0)) / 2.0
  return c_data

##################################################################
# main program
##################################################################

mdir = "../meshes/" # mesh directory
hldir = "./4HL/"      # output data for hololens

# create hololens data file per cell
mesh_names = subprocess.check_output("ls " + mdir + "4sim*.bin", shell=True).split()
for i,fname in enumerate(mesh_names):
  print "Cell", i
  verts, tris, tets, dfa, dfb, apical, basal, common = rw.read_bin(fname)
  rni = reduce_nodes(verts, tris)
  print "Vertex count reduction:", verts.shape[0], "->", rni.shape[0]

  ## paraview files
  #rw.write_points(hldir + "reduced-nodes_" + str(i+1), verts[rni])
  #rw.write_tris(hldir + "surface_" + str(i+1), verts, tris)

  # hololens binary data files
  c_data = get_c_data(verts, rni)
  fname = hldir + "4HL_Cell" + str(i+1) + ".bin" 
  min = 0.0
  max = 0.5
  write_4HL(fname, verts, rni, c_data, min, max) # binary file for hololens


