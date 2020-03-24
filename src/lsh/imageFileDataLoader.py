'''
Class acting as loader and comparator to match image files with images referenced with data on periods, culture, region, etc. in image_data folder.

Created on Nov 27, 2019

@author: 
'''

import os
import csv

class ImageFile():
    
    ''''
    Method to read data from given input_dir. This reads the imageLink.csv file in image_data.
    '''
    def readFile(self):
        
        self.cultureData={}
        self.periodData={}
        self.timeData={}
        self.region={}
        self.runFile()
        
        with open(self.input_dir,mode='rU') as csvfile:
                reader = csv.DictReader(csvfile)
 
                for row in reader:
                    fileN=row['File'].split('.')[0]
                    timeD=row['Time']
                    period=row['Period']
                    culture=row['Culture']
                    reg=row['Region']
                    
                    
                    self.cultureData[fileN]=culture
                    self.periodData[fileN]=period
                    
                    self.timeData[fileN]=timeD
                    self.region[fileN]=reg
                    
    '''
    Method links imageLink.csv to image_data folder
    '''
    def runFile(self):
        
        pn=os.path.abspath(__file__)
        pn=pn.split("src")[0]
    
        self.input_dir=os.path.join(pn,'image_data','imageLink.csv')
        
    '''
    Method to compare and link imageLink.csv data with input images (i.e.,  the jpg files).
    
    @param file1: The first file (jpg) compared and searched for in imageLink.csv
    @param file2:  The second file (jpg) compared and searched for in imageLink.csv
    
    @return time1, period1, culture1, region1, time2, period2, culture2, region2: returns time, period, culture, and region for two images (i.e., a pair of these ressults)
    '''
    def checkResults(self,file1,file2):
        file1=file1.split('.')[0]
        file2=file2.split('.')[0]
        time1=''
        period1=''
        culture1=''
        region1=''
        
        time2=''
        period2=''
        culture2=''
        region2=''
        
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

        else:
            print('stop')   
             
    
        return time1, period1, culture1, region1, time2, period2, culture2, region2
    
        