'''
Created on Nov 27, 2019

@author: mark
'''

import os
import csv

class ImageFile():
    
    def readFile(self):
        
        self.cultureData={}
        self.periodData={}
        self.timeData={}
        
        with open(self.input_dir,'rU') as csvfile:
                reader = csv.DictReader(csvfile)
 
                for row in reader:
                    fileN=row['File']
                    timeD=row['Time'].split(":")
                    period=row['Period']
                    culture=row['Culture']
                    
                    self.cultureData[fileN]=culture
                    self.periodData=[fileN]=period
                    self.timeData[fileN]=timeD
                    

    def runFile(self):
        
        pn=os.path.abspath(__file__)
        pn=pn.split("src")[0]
    
        self.input_dir=os.path.join(pn,'image_data','imageLink.csv')
        
    
    def checkResults(self,file1,file2):
        
        print('results')
    
        