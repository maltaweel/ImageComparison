'''
Created on Nov 8, 2018

@author: mark
'''
import networkx as nx
import os
import pysal
import geopandas as gpd


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
    
    poly = gpd.read_file(filename)
    geometry = poly['geometry']
    values=poly['value']
    
    
    node1=0
    node2=0
    i = 0
    
    for p in range(0,len(geometry)):
      
        string1=geometry[p]
        value=values[i]
        b=string1.bounds
        node1=(b[0],b[1])
        node2=(b[2],b[3])
        line=(node1,node2,value)
       # weight=string1['value']
           
            
        links.append(line)
        i+=1
                
  
           
           
    
    
    G=addWeightedEdges(links)
    
    return G

def run():
    load()
    
if __name__ == '__main__':
    run()
