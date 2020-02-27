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


results={}

def createNetwork():
    G=nx.Graph()
    
    
    return G

def addWeightedEdges(x):
    G=nx.Graph()
    G.add_weighted_edges_from(x,weight='value')
    
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
    filename=os.path.join(pn,'network_output','network2.shp')
    
    
    poly = gpd.read_file(filename)
    
    
    geometry = poly['geometry']
    
    
    values=poly['value']
    
    
    node1=0
    node2=0
  
    
    G = nx.Graph(weight='weight').to_undirected()
    
    for p in range(0,len(geometry)):
        
        string1=geometry[p]
        
        value=values[p]
        b=string1.bounds
        node1=(b[0],b[1])
        node2=(b[2],b[3])
        
            
        G.add_edge(node1, node2, weight=value, length=0.0)
        #line=(node1,node2,value)
        #weight=string1['value']
        
        if b[0] in results: 
            r=results[b[0]]+value
            
            results[b[0]]=r
        else:
            results[b[0]]=value
        
        if b[2]==b[0]:
            continue
        
        if b[2] in results:
            r=results[b[2]]+value
            
            results[b[2]]=r
        else:
            results[b[2]]=value
            
        #links.append(line)
      
  
           
 #   G=addWeightedEdges(links)
    
    centrality = nx.eigenvector_centrality(G,weight='weight') 
   
    return centrality
 #   print(['%s %0.2f'%(node,centrality[node]) for node in centrality])
    
 #   return G

def runPoints(centrality):
    path=os.path.join(pn,'network_output','centrality.csv')
    filename2=os.path.join(pn,'network_output','points.shp')
    
    poly2 = gpd.read_file(filename2)
    geometry2 = poly2['geometry']
    
    fieldnames = ['Point 1','Point 2','Value']
    
    contains={}
    with open(path, 'w') as csvf:
        writer = csv.DictWriter(csvf, fieldnames=fieldnames)
        writer.writeheader()
        
        for node in centrality:
            
            printt=False
        #   v=centrality[node]
            x=node[0]
            y=node[1]
            
            v=results[x]
            for q in range(0,len(geometry2)):
                qq=geometry2[q].bounds
                   
                if x==qq[0] and y==qq[1]:
                    printt=True
                        
                    contains[x]=y
                    
            
            
            
            if printt is True:
                writer.writerow({'Point 1': str(x),'Point 2':str(y),'Value':str(str(v))})
        
        
def run():
    centrality=load()
    runPoints(centrality)
    
    print('Finished')
    
if __name__ == '__main__':
    run()
