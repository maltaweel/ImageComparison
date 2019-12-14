'''
Module to create shapefile data.

Created on Dec 14, 2019

@author: mark
'''
import shapefile
import geopandas as gpd
import os

pn=os.path.abspath(__file__)
pn=pn.split("src")[0]     
countries={}

def makePoint(x,y,number):
    w = shapefile.Writer(shapefile.POINT)
    w.point(x,y)
    w.record(number,'Point')
   
   
def makeLine(x1,y1,x2,y2,number):
    w = shapefile.Writer(shapefile.POLYLINE)
    w.line(parts=[[[x1,y1],[x2,y2]]])
    w.record(number,'Line')
    

def writePoint(w,file):
    w.save(os.path.join(pn,'output',file))
     
    return w

def readInputShape():
    path=os.path.join(pn,'shp',"TM_WORLD_BORDERS-0.3.shp")
    poly = gpd.read_file(path)
    points = poly.copy()
    geometry = points['geometry'].centroid
    names=points['NAME']
    points.crs =poly.crs
    points.head()
    
    for i in range(0,len(geometry)):
        countries[names[i]]=geometry[i]
        
    
    
def runData():
    
    print('points finished')

def run():
    readInputShape()
    
    runData()
    
    print('finished')

if __name__ == '__main__':
    run()

