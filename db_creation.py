import random
import struct
from BplusTree import tree

j=300

def add(i):
  global j
  merchants=[k for k in range(j-300,j)]
  j+=300
  byte_data=struct.pack('!{}I'.format(len(merchants)), *merchants)
  tree.insert(i,byte_data,replace=True)

list(map(add,range(0,30000)))
"Noice"

# Commented out IPython magic to ensure Python compatibility.
# %%timeit
# len(tree)

retrieved_list = struct.unpack('!{}I'.format(len(tree.get(2134))//4),tree.get(2134))

retrieved_list

tree.close()