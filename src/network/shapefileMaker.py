'''
Module to create shapefile data.

Created on Dec 14, 2019

@author: mark
'''
import shapefile
import os

pn=os.path.abspath(__file__)
pn=pn.split("src")[0]     

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
    
def runData(points,lines):
    
    
    print('points finished')