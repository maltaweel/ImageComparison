'''
Created on Nov 8, 2018

@author: mark
'''
import networkx as nx
import shapefile
import csv
import os
import pysal
import geopandas as gpd
import network.shapefileMaker as shapefileMaker

pn=os.path.abspath(__file__)
pn=pn.split("src")[0]  

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
        #weight=string1['value']
           
            
        links.append(line)
        i+=1
                
  
           
    G=addWeightedEdges(links)
    
    centrality = nx.betweenness_centrality(G,weight='value') 
   
    return centrality
 #   print(['%s %0.2f'%(node,centrality[node]) for node in centrality])
    
 #   return G

def runPoints(centrality):
    path=os.path.join(pn,'network_output','centrality.csv')
    fieldnames = ['Point 1','Point 2','Value']
    
    with open(path, 'w') as csvf:
        writer = csv.DictWriter(csvf, fieldnames=fieldnames)
        writer.writeheader()
        
        for node in centrality:
            v=centrality[node]
            x=node[0]
            y=node[1]
            
            if v>0:
                writer.writerow({'Point 1': str(x),'Point 2':str(y),'Value':str(str(v))})
        
        
def run():
    centrality=load()
    runPoints(centrality)
    
    print('Finished')
    
if __name__ == '__main__':
    run()
