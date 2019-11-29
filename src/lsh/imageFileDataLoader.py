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
        self.region={}
        self.runFile()
        
        with open(self.input_dir,mode='rU') as csvfile:
                reader = csv.DictReader(csvfile)
 
                for row in reader:
                    fileN=row['File']
                    timeD=row['Time']
                    period=row['Period']
                    culture=row['Culture']
                    reg=row['Region']
                    
                    
                    self.cultureData[fileN]=culture
                    self.periodData[fileN]=period
                    self.timeData[fileN]=timeD
                    self.region[fileN]=reg
                    

    def runFile(self):
        
        pn=os.path.abspath(__file__)
        pn=pn.split("src")[0]
    
        self.input_dir=os.path.join(pn,'image_data','imageLink.csv')
        
    
    def checkResults(self,file1,file2):
        
        time1=''
        period1=''
        culture1=''
        
        time2=''
        period2=''
        culture2=''
        
        if file1 in self.cultureData:
            time1=self.timeData[file1]
            period1=self.periodData[file1] 
            culture1=self.cultureData[file1]
            region1=self.region[file1]
            
        
        if file2 in self.cultureData:
            time2=self.timeData[file2]
            period2=self.periodData[file2]
            culture2=self.cultureData[file2]
            region2=self.region[file2]
             
        
        return time1, period1, culture1, region1, time2, period2, culture2, region2
    
        