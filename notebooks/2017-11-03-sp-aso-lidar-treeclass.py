
# coding: utf-8

# In[1]:


import numpy as np
from laspy.file import File
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter


# In[2]:



original = File("data/split0156.las", mode = "r") # load in a small las file for testing
ground = File("data/split0156_ground.las", mode = "r") # load in its complimentary ground points
                                                             # (produced using PDAL pipeline)


# In[3]:


# 3D Scatterplots of each file (original and ground)


fig = plt.figure(figsize=(12,8))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(original.X, original.Y, original.Z, c=original.Z, marker='.', s=.7, cmap='Reds')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.title("Original LAS 3D View")
plt.show()

fig2 = plt.figure(figsize=(12,8))
ax2 = fig2.add_subplot(111, projection='3d')
ax2.scatter(ground.X, ground.Y, ground.Z, c=ground.Z, marker='.', s=.7, cmap='Reds')
ax2.set_xlabel('X')
ax2.set_ylabel('Y')
ax2.set_zlabel('Z')
plt.title("Ground LAS 3D View")
plt.show()



# In[14]:


plt.figure(figsize=(15,8))
plt.scatter(original.X,             original.Z,             c=original.Y,             marker='.',             s=10,             cmap='Reds'           )
plt.show()

plt.figure(figsize=(15,8))
plt.scatter(ground.X,             ground.Z,             c=ground.Y,             marker='.',             s=10,             cmap='Reds'           )
plt.show()

#plt.hist(inFile.Y*inFile.header.scale[1],bins=bin_list_y,)
#plt.title("Histogram of the Y Dimension - 1m")
#plt.show()

