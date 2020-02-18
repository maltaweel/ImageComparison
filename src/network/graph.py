'''
Created on Nov 8, 2018

@author: mark
'''
import networkx as nx
import os
import pysal

def createNetwork():
    G=nx.Graph()
    
    
    return G

def addWeightedEdges(x):
    G=nx.Graph()
    G.add_weighted_edges_from(x)
    
    return G



'''
Load the data and creating the links for the network from street segment file.
@param fileName the shapefile name to assess.
'''
def load():
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
    links=[]
      
    #The data file path is now created where the data folder and dataFile.csv is referenced
    filename=os.path.join(pn,'network_output','network.shp')
        
    shp = pysal.open(filename)
    node1=0
    node2=0
    i = 0
    
    for s in shp:
      
        for p in s._vertices:
           
            node1=p[0]
            weight=p['value']
           
            #print(node1)
            
            link=(node1,node2,weight)
            
            
            
            links.append(link)
            i+=1
                
  
           
           
    
    
    G=addWeightedEdges(links)
    
    return G

load()
