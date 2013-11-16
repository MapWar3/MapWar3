import scipy as sp
import numpy as np
from scipy.spatial import *
import matplotlib.pyplot as plt
import random
import networkx as nx
import itertools
from collections import defaultdict
import cPickle
import time
start = time.time()
#enables pickling
kdtree.node = kdtree.KDTree.node
kdtree.leafnode = kdtree.KDTree.leafnode
kdtree.innernode = kdtree.KDTree.innernode

class World:
    def __init__(self, points):
        self.pdict = identify(points)
        self.tree = maketree(points)
        self.adj = adjacency(points)
        self.zones = {}
        for id in self.pdict[0].keys():
            self.zones[id] = Zone(id,self.adj[id])
        self.net = nx.Graph()
        for k in self.zones.keys():
            self.net.add_node(k, zone=self.zones[k])
            for adj in self.zones[k].adj:
                self.net.add_edge(k,adj)          
            
class Zone:
    def __init__(self,id,adj):
        self.id = id
        self.adj = adj
        #store values like structures, type, etc here

#poisson disk sampling
def pds(mp=100, i=0, rd=0.03):
    points = []
    while i<mp:
        x, y = random.random(), random.random()
        reject = False
        for j in xrange(0,i):
            d = (x-points[j][0])**2+(y-points[j][1])**2
            if d < (2*rd)**2:
                reject = True
        if not(reject):
            i+= 1
            points.append([x,y])
    points = np.array(points)
    return points

def identify(points):
    pdict = [{},{}] #double dictionary
    for p,i in enumerate(points):
        id = p
        i = tuple(i)
        pdict[0][i] = id
        pdict[1][id] = i
    return pdict

def maketree(points):
    tree = KDTree(points)
    return tree

def getzone(tree,point): #returns id 
    return tree.query(point)[1]

def adjacency(points):
    #define adjacent cells
    tri = Delaunay(points)
    adj = defaultdict(set)
    for p in tri.vertices:
        for i,j in itertools.combinations(p,2):
            adj[i].add(j)
            adj[j].add(i)
    return adj
            
def getadjacent(cell,adj):
    return adj[cell]

def render(points):
    #this is just a preview image and would never be used in the actual game of course.
    vor = Voronoi(points)
    voronoi_plot_2d(vor)
    plt.savefig('cells.png', bbox_inches = 'tight')
    return 0

###example
pl = pds()
Game1 = World(pl)

with open('world.dat', 'wb') as file:
    cPickle.dump(Game1,file)
print time.time()-start
print 'rendering'
render(pl)