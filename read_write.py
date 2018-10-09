import numpy as np
import struct
from evtk.hl import pointsToVTK
from evtk.hl import unstructuredGridToVTK
from evtk.vtk import VtkTriangle
from evtk.vtk import VtkTetra

###########################################################################
# functions
###########################################################################

###########################################################################
def read_lumen(fname):
  f1 = open(fname, 'r') # open the lumen file

  nlverts = int(f1.next().split()[0]) 
  lverts = np.empty([nlverts, 3])
  for i in range(nlverts): # get the lumen verts
    lverts[i] = map(float, f1.next().split()[0:3])

  nlines = int(f1.next().split()[0])
  lines = np.empty([nlines, 2], dtype=int)
  for i in range(nlines): # get the lumen line segments
    lines[i] = map(int, f1.next().split()[0:2])

  lsegs = np.empty([nlines, 2, 3])
  for i in range(nlines): # get the lumen line segments
    v1 = map(float, lverts[lines[i,0]-1])
    v2 = map(float, lverts[lines[i,1]-1])
    lsegs[i] = np.array([v1, v2])

  f1.close()
  return lsegs

###########################################################################
# read binary mesh
def read_bin(fname):
  f1 = open(fname, 'rb') # open the binary file

  # get the vertices
  nverts = struct.unpack('i', f1.read(4))[0]
  verts = np.empty([nverts, 3])
  for i in range(nverts):
    verts[i] = struct.unpack('fff', f1.read(12))

  # get the tris
  ntris = struct.unpack('i', f1.read(4))[0]
  tris = np.empty([ntris, 3], dtype=int)
  for i in range(ntris):
    tris[i] = struct.unpack('iii', f1.read(12))

  # get the tets, dfa, dfb
  ntets = struct.unpack('i', f1.read(4))[0]
  tets = np.empty([ntets, 4], dtype=int)
  dfa = np.empty([ntets])
  dfb = np.empty([ntets])
  for i in range(ntets):
    tets[i] = struct.unpack('iiii', f1.read(16))
    dfa[i] = struct.unpack('f', f1.read(4))[0]
    dfb[i] = struct.unpack('f', f1.read(4))[0]

  # get apical 
  napical = struct.unpack('i', f1.read(4))[0]
  apical = np.empty([napical], dtype=int)
  for i in range(napical):
    apical[i] = struct.unpack('i', f1.read(4))[0]

  # get basal 
  nbasal = struct.unpack('i', f1.read(4))[0]
  basal = np.empty([nbasal], dtype=int)
  for i in range(nbasal):
    basal[i] = struct.unpack('i', f1.read(4))[0]

  # get common
  ncommon = struct.unpack('i', f1.read(4))[0]
  common = np.empty([ncommon, 3], dtype=int)
  for i in range(ncommon):
    common[i] = struct.unpack('iii', f1.read(12))

  f1.close # close the binary file 
  return verts, tris, tets, dfa, dfb, apical, basal, common

###########################################################################
# write paraview points
def write_points(fname, verts, pdata=None):
  nverts = verts.shape[0]
  xyz = np.empty([3, nverts]) # needs re-ordering
  for i in range(nverts):
    for j in range(3):
      xyz[j,i] = verts[i,j]  
  pointsToVTK(fname, \
    xyz[0,:], xyz[1,:], xyz[2,:], \
    data=pdata)  # write out vtu file
  return

###########################################################################
# write paraview triangles
def write_tris(fname, verts, tris, data=None):
  nverts = verts.shape[0]
  xyz = np.empty([3, nverts]) # because it needs re-ordering
  for i in range(nverts):
    for j in range(3):
      xyz[j,i] = verts[i,j]  
  ntris = tris.shape[0]
  conn = np.empty(3*ntris)
  for i in range(ntris):
    conn[3*i] = tris[i,0]-1 # index from zero
    conn[3*i+1] = tris[i,1]-1
    conn[3*i+2] = tris[i,2]-1
  offset = np.zeros(ntris, dtype=int)
  for i in range(ntris):
    offset[i] = 3*(i+1) 
  ctype = np.zeros(ntris)
  for i in range(ntris):
    ctype[i] = VtkTriangle.tid 
  unstructuredGridToVTK(fname, \
    xyz[0,:], xyz[1,:], xyz[2,:], \
    connectivity=conn, offsets=offset, cell_types=ctype, \
    cellData=data, pointData=None)  # write out vtu file
  return

###########################################################################
# write paraview tetrahedrons
def write_tets(fname, verts, tets, data=None):
  nverts = verts.shape[0]
  xyz = np.empty([3, nverts]) # because it needs re-ordering
  for i in range(nverts):
    for j in range(3):
      xyz[j,i] = verts[i,j]  
  ntets = tets.shape[0]
  conn = np.empty(4*ntets)
  for i in range(ntets):
    conn[4*i] = tets[i,0]-1 # index from zero
    conn[4*i+1] = tets[i,1]-1
    conn[4*i+2] = tets[i,2]-1
    conn[4*i+3] = tets[i,3]-1
  offset = np.zeros(ntets, dtype=int)
  for i in range(ntets):
    offset[i] = 4*(i+1) 
  ctype = np.zeros(ntets)
  for i in range(ntets):
    ctype[i] = VtkTetra.tid 
  unstructuredGridToVTK(fname, \
    xyz[0,:], xyz[1,:], xyz[2,:], \
    connectivity=conn, offsets=offset, cell_types=ctype, \
    cellData=data, pointData=None)  # write out vtu file
  return

###########################################################################


