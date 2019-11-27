'''
Created on Nov 27, 2019

@author: mark
'''

import os
import csv

cultureData={}
periodData={}
timeData={}

def readFile(pathway):
    with open(pathway,'rU') as csvfile:
                reader = csv.DictReader(csvfile)
 
                for row in reader:
                    fileN=row['File']
                    timeD=row['Time'].split(":")
                    period=row['Period']
                    culture=row['Culture']
                    
                    cultureData[fileN]=culture
                    periodData=[fileN]=period
                    timeData[fileN]=timeD
                    

def runFile():
    
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
    
    input_dir=os.path.join(pn,'image_data','imageLink.csv')
    
    readFile()