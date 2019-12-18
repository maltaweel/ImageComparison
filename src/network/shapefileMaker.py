'''
Module to create shapefile data.

Created on Dec 14, 2019

@author: mark
'''
import shapefile
import geopandas as gpd
import os
import csv


pn=os.path.abspath(__file__)
pn=pn.split("src")[0]     

countries={}
geoValues={}
country_file={}


def makePoint(w,x,y,number):    
    w.point(x,y)
    w.record(value=number)
   
   
def makeLine(w,points,number):
    
    w.line([[[points[0],points[1]],[points[2],points[3]]]])
#   w.record(ID=n)
    w.record(value=number)
    
    
    

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
    pway=os.path.join(pn,'image_data','imageLink.csv')
    
    try:
        with open(pway, 'rU') as csvf:
            reader = csv.DictReader(csvf)

            for row in reader:
                
                fileName=row['File']
                mCountry=row['Modern Country']
                
                fileName=fileName.split(".")[0]
                country_file[fileName]=mCountry
                
    except IOError:
        print ("Could not read file:", IOError)     

def matchOutput():
    pway=os.path.join(pn,'output')

    try:
        
        for f in os.listdir(pway):
            with open(os.path.join(pway,f), 'rU',encoding='utf8',errors='replace') as csvf:
                reader = csv.DictReader((l.replace('\0', '') for l in csvf))
            
                for row in reader:
                   
                    f1 = row['File 1'].split(".")[0]
                    f2 = row['File 2'].split(".")[0]

                    v=float(row['Similarity'])
                
                    cntry1=country_file[f1]
                    cntry2=country_file[f2]
                
                    key=cntry1+":"+cntry2
                
                    if key in geoValues:
                        vv=geoValues[key]
                        geoValues[key]=v+vv
                    else:
                        geoValues[key]=v
                

    except IOError:
        print ("Could not read file:", IOError) 
        
def createOutput():
    pointC={}
    
    path=os.path.join(pn,'network_output','network.shp')
    path2=os.path.join(pn,'network_output','points.shp')
    
    w = shapefile.Writer(path,shapefile.POLYLINE)
    w2 = shapefile.Writer(path2,shapefile.POINT)
    
    
    w.field('value','F',10,decimal=10)
 #  w.field('ID','N',10)
    w2.field('value','F',10,decimal=10)
    
    n=0
    for k in geoValues.keys():
        v=geoValues[k]
        
        sp1=k.split(":")[0]
        sp2=k.split(":")[1]
        
        
        if sp1 in countries:
            g1=countries[sp1]
            x1=g1.x
            y1=g1.y
            
            pc=str(x1)+":"+str(y1)
            
            if pc not in pointC:
                pointC[pc]=pc
                makePoint(w2,x1,y1,v)
                
        if sp2 in countries:
            g2=countries[sp2]
            x2=g2.x
            y2=g2.y
            
            pc=str(x2)+":"+str(y2)
            
            if pc not in pointC:
                pointC[pc]=pc
                makePoint(w2,x2,y2,v)
        
        points=[x1,y1,x2,y2]
        if x1 and y2 is not None:
            makeLine(w,points,v)
        
        n+=1
#      w.save(path)
#      w2.save(path2)
          
def run():
   
    readInputShape()
    runData()
    matchOutput()
    createOutput()
    
    print('finished')

if __name__ == '__main__':
    run()

