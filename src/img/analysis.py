'''
Created on Apr 6, 2020

@author: mark
'''
import os
import csv

#field names for output .csv file to show comparison lsh values
fieldnames = ['Similarity','File 1','File 2',"Region 1",'Region 2']
keep=[]

#path to src
pn=os.path.abspath(__file__)
pn=pn.split("src")[0]
    
    
def read_data():
    
    pway=os.path.join(pn,'images')
    
    try:
        
        for f in os.listdir(pway):
            with open(os.path.join(pway,f), 'rU',encoding='utf8',errors='replace') as csvf:
                reader = csv.DictReader((l.replace('\0', '') for l in csvf))
            
                for row in reader:
                    
                    
                    r1=row['Region 1']
                    r2=row['Region 2']
                    
                    if r1!=r2:
                        keep.append(row)
                        
                    else:
                        continue
                    
    except IOError:
        print ("Could not read file:", IOError) 
        
def printResults():
    
    path=os.path.join(pn,'output','lsh6.csv')
    
    
    with open(path, 'w') as csvf:
             
            writer = csv.DictWriter(csvf, fieldnames=fieldnames)
            writer.writeheader()
            
            for k in keep:
                
                writer.writerow({'Similarity': str(k['Similarity']),
                                 'File 1':str(k['File 1']),
                                 'File 2':str(k['File 2']),
                                 'Region 1':str(k['Region 1']),
                                 'Region 2':str(k['Region 2']),
                                 })
    
read_data()
printResults()