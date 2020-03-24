'''
Module to create shapefile data of image comparisons (network and node data) and an inverse closeness centrality network measure.

Created on Dec 14, 2019

@author: mark
'''
import shapefile
import geopandas as gpd
import os
import csv
import numpy as np

#path to src
pn=os.path.abspath(__file__)
pn=pn.split("src")[0]     

#containers for countries to match between images (.csv meta-data file) and shapefile countries
countries={}
geoValues={}
country_file={}

#point data to output
totalsPoint={}

#field names for output .csv file to show comparison lsh values
fieldnames = ['Point 1','Point 2','Median Value',"Standard Deviation"]


'''
Method to make a point shapefile.

Args: w: the shapefilewriter
      x: the x location
      y:  the y location
      number: the value to associate the point shapefile
'''
def makePoint(w,x,y,number):    
    w.point(x,y)
    w.record(value=number)
   
'''
Method to make a polyline shapefile.

@param w: the shapefilewriter
@param points: the points associated with the polyline (2 points)
@param number: the value to associate the polyline shapefile
'''  
def makeLine(w,points,number):
    
    w.line([[[points[0],points[1]],[points[2],points[3]]]])
 #  w.record(name1=str(n1+":"+n2))
    w.record(value=number)
   
   

'''
Method to read input (see /shp folder) shapefile that will match with the name of the region/country associated with given images.
This helps to then match image and country in the output shapefile.
'''
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
        
    
'''
Method to load imageLink and get countries from given file names.
'''   
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
'''
This matches the /output results with countries in input shapefile (in /shp folder).
'''
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
                    key2=cntry2+":"+cntry1
                    
                    if key in geoValues:
                        
                        values=geoValues[key]
                        values.append(v)
                        geoValues[key]=values
                    
                    elif key2 in geoValues:
                        values=geoValues[key2]
                        values.append(v)
                        geoValues[key]=values 
                        del geoValues[key2]
                       
                    else:
                       
                        values=[v]
                        geoValues[key]=values
                        
                    
                    if cntry1 in totalsPoint:
                        vs=totalsPoint[cntry1]
                        vs.append(v)
                        totalsPoint[cntry1]=vs
                    
                    else:
                        vs=[v]
                        totalsPoint[cntry1]=vs
                    
                    if cntry2 in totalsPoint:
                        vs1=totalsPoint[cntry2]
                        vs1.append(v)
                        totalsPoint[cntry2]=vs1
                    else:
                        vs1=[v]
                        totalsPoint[cntry2]=vs1
                

    except IOError:
        print ("Could not read file:", IOError) 

'''
Method to create network (network.shp output that has inverse closeness centrality using weight (similarity) measures ) and point shapefiles of the nodes.
'''       
def createOutput():
    pointC={}
    
    path=os.path.join(pn,'network_output','network.shp')
    path2=os.path.join(pn,'network_output','points.shp')
    path3=os.path.join(pn,'network_output','network.csv')
    
    w = shapefile.Writer(path,shapefile.POLYLINE)
    w2 = shapefile.Writer(path2,shapefile.POINT)
    
#   w.field('name1','C',40)
    w.field('value','F',10,decimal=3)

    w2.field('value','F',10,decimal=3)
    
    with open(path3, 'w') as csvf:
             
            writer = csv.DictWriter(csvf, fieldnames=fieldnames)
            writer.writeheader()
            
            for k in geoValues.keys():
                values=geoValues[k]
                
                #median values are calculated for a comparisons for a given link
                v=np.median(values)
        
                sp1=k.split(":")[0]
                sp2=k.split(":")[1]
        
        
        
                if sp1 in countries:
                
                    g1=countries[sp1]
                    x1=g1.x
                    y1=g1.y
            
                    pc=str(x1)+":"+str(y1)
            
                    #this will make the point if not already existing; sum the values of the link to the node
                    if pc not in pointC:
                        vs=totalsPoint[sp1]
                        makePoint(w2,x1,y1,float(np.sum(vs)))
                        pointC[pc]=pc
                
                if sp2 in countries:
                    g2=countries[sp2]
                    x2=g2.x
                    y2=g2.y
            
                    pc=str(x2)+":"+str(y2)
                    
                    #this makes the other point if not already existing; sum the values of the link to the node
                    if pc not in pointC:
                        vs=totalsPoint[sp2]
                        makePoint(w2,x2,y2,float(np.sum(vs)))
                        pointC[pc]=pc
        
                points=[x1,y1,x2,y2]
                if x1 and x2 and y1 and y2 is not None:
                    #make the line
                    makeLine(w,points,round(v,3))
                    
                    #write csv output as well
                    writeData(sp1,sp2,values,writer)

'''
Method writes data to .csv file (network point and line data) that shows regions and their (median and standard deviation) similarity values

@param p1: point 1 for the shapefile (country 1)
@param p2: point 2 for the shapefile (country 2)
@param v: the container with the values to run median and standard deviation
@param writer: the csv writer (see network_output folder for output (network.csv)
'''
def writeData(p1,p2,v,writer):
    writer.writerow({'Point 1': str(p1),'Point 2':str(p2),'Median Value':str(round(np.median(v),3)),'Standard Deviation':str(round(np.std(v),2))})
    
#      w.save(path)
#      w2.save(path2)

'''
Method to run the module
'''    
def run():
   
    readInputShape()
    runData()
    matchOutput()
    createOutput()
    
    print('finished')

#run the run method
if __name__ == '__main__':
    run()

