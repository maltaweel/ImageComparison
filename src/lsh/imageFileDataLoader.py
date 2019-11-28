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
        
        self.runFile()
        
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
        
        time1=''
        period1=''
        culture1=''
        
        time2=''
        period2=''
        culture2=''
        
        if file1 in self.cultureData:
            time1=self.timeData[file1], period1=self.periodDat[file1], culture1=self.cultureData[file1]
            
        
        if file2 in self.cultureData:
            time2=self.timeData[file2], period2=self.periodDat[file2], culture2=self.cultureData[file2]
             
        
        return time1, period1, culture1, time2, period2, culture2
    
        