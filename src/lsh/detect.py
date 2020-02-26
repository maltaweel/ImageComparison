'''
This is a near duplicate detection Locality Sensitive Hashing implementation. 

Code modified from:  https://github.com/mendesk/image-ndd-lsh

This module adds comparability outputs (.csv file).


Created on Nov 15, 2019

'''

import argparse
import sys
import os
from os import listdir
from os.path import isfile, join
from typing import Dict, List, Optional, Tuple
import time

import imagehash
import numpy as np
from PIL import Image
import csv
from imageFileDataLoader import ImageFile

#for holding historical (i.e., more than one run) data to output
historical={}

"""
    Calculate the dhash signature of a given file
    
    Args:
        image_file: the image (path as string) to calculate the signature for
        hash_size: hash size to use, signatures will be of length hash_size^2
    
    Returns:
        Image signature as Numpy n-dimensional array or None if the file is not a PIL recognized image
"""
def calculate_signature(image_file: str, hash_size: int) -> np.ndarray:
   
    try:
        pil_image = Image.open(image_file).convert("L").resize(
                            (hash_size+1, hash_size), 
                            Image.ANTIALIAS)
        dhash = imagehash.dhash(pil_image, hash_size)
        signature = dhash.hash.flatten()
        pil_image.close()
        return signature
    except IOError as e:
        raise e

'''
    Find near-duplicate images
    
    Args:
        input_dir: Directory with images to check
        threshold: Images with a similarity ratio >= threshold will be considered near-duplicates
        hash_size: Hash size to use, signatures will be of length hash_size^2
        bands: The number of bands to use in the locality sensitve hashing process
        
    Returns:
        A list of near-duplicates found. Near duplicates are encoded as a triple: (filename_A, filename_B, similarity)
'''  
def find_near_duplicates(input_dir: str, threshold: float, hash_size: int, bands: int) -> List[Tuple[str, str, float]]:
   
    #int
    rows  = int(hash_size**2/bands)
    
    signatures = dict()
    
    #:  List[Dict[str, List[str]]]
    
    hash_buckets_list = [dict() for _ in range(bands)]
    
    # Build a list of candidate files in given input_dir
    try:
        file_list = [join(input_dir, f) for f in listdir(input_dir) if isfile(join(input_dir, f))]
    except OSError as e:
        raise e
    
    # Iterate through all files in input directory
    for fh in file_list:
        try:
            signature = calculate_signature(fh, hash_size)
        except IOError:
            # Not a PIL image, skip this file
            continue

        # Keep track of each image's signature
        signatures[fh] = np.packbits(signature)
        
        # Locality Sensitive Hashing
        for i in range(bands):
            signature_band = signature[i*rows:(i+1)*rows]
            signature_band_bytes = signature_band.tostring()
            if signature_band_bytes not in hash_buckets_list[i]:
                hash_buckets_list[i][signature_band_bytes] = list()
            hash_buckets_list[i][signature_band_bytes].append(fh)

    # Build candidate pairs based on bucket membership
    candidate_pairs = set()
    for hash_buckets in hash_buckets_list:
        for hash_bucket in hash_buckets.values():
            if len(hash_bucket) > 1:
                hash_bucket = sorted(hash_bucket)
                for i in range(len(hash_bucket)):
                    for j in range(i+1, len(hash_bucket)):
                        candidate_pairs.add(
                            tuple([hash_bucket[i],hash_bucket[j]])
                        )

    # Check candidate pairs for similarity
    near_duplicates = list()
    for cpa, cpb in candidate_pairs:
        hd = sum(np.bitwise_xor(
                np.unpackbits(signatures[cpa]), 
                np.unpackbits(signatures[cpb])
        ))
        similarity = (hash_size**2 - hd) / hash_size**2
       
        if similarity > threshold:
            near_duplicates.append((cpa, cpb, similarity))
        else:
            print(similarity)
            near_duplicates.append((cpa, cpb, similarity))
            
    # Sort near-duplicates by descending similarity and return
    near_duplicates.sort(key=lambda x:x[2], reverse=True)
    return near_duplicates

'''
This method prints multiple runs (if used) as csv files.

Args: imageFile:  imagefile module used to find file and images
'''
def printHistorical(imageFile):
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
    
    pathway=os.path.join(pn,'output','output_historical_lsh.csv')
    
    fieldnames = ['Similarity','File 1','File 2',"Time 1",'Time 1 End','Period 1',"Culture 1","Region 1","Time 2",'Time 2 End',"Period 2","Culture 2",
                  "Region 2"]
     
    #print results out
    try:
        with open(pathway, 'w') as csvf:
             
            writer = csv.DictWriter(csvf, fieldnames=fieldnames)

            writer.writeheader()
            
            for k in historical:
                v=historical[k]
                s1=k.split(":")[0]
                s2=k.split(":")[1]
                
                v_mean=v/300.0
            
                time1, period1, culture1, region1, time2, period2, culture2, region2=imageFile.checkResults(s1,s2)
                
                st1=time1.split(':')[0]
                st2=time1.split(":")[1]
                
                et1=time2.split(":")[0]
                et2=time2.split(":")[1]
                
                writer.writerow({'Similarity': str(v_mean),'File 1':str(s1),
                            'File 2':str(s2),'Time 1':st1,'Time 1 End':st2,
                            'Period 1':period1,'Culture 1':culture1,'Region 1':region1,'Time 2':et1,'Time 2 End':et2,
                            'Period 2':period2,'Culture 2':culture2,'Region 2':region2})
            
    except IOError:
        print ("Could not read file:", IOError)        

'''
Method to print outputs from lsh algorith (one run).

Args: near_duplicates:  the comparison lsh results
      imageFile:  imagefile module used to find file and images
'''
def printResults(near_duplicates,imageFile):
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
    
    timeT=str(float(time.time()))
    pathway=os.path.join(pn,'output','output_lsh'+timeT+'.csv')
    
    fieldnames = ['Similarity','File 1','File 2',"Time 1",'Time 1 End','Period 1',"Culture 1","Region 1","Time 2",'Time 2 End',"Period 2","Culture 2",
                  "Region 2"]
    #print results out
    try:
        with open(pathway, 'w') as csvf:
             
            writer = csv.DictWriter(csvf, fieldnames=fieldnames)

            writer.writeheader()
            
            for a,b,s in near_duplicates:
                sp1=a.split(os.sep)
                f1=sp1[len(sp1)-1].split('.jp')[0]
                
                sp2=b.split(os.sep)
                f2=sp2[len(sp2)-1].split('.jp')[0]
                
                combined=f1.strip()+":"+f2.strip()
                cv_v=s
                if combined in historical:
                    v=historical[combined]
                    historical[combined]=v+s
                
                else:
                    historical[combined]=s
                
                time1, period1, culture1, region1, time2, period2, culture2, region2=imageFile.checkResults(f1,f2)
                
                print(f1+":"+f2)
                st1=time1.split(':')[0]
                st2=time1.split(":")[1]
                
                #print(time1+":"+time2)
                et1=time2.split(":")[0]
                et2=time2.split(":")[1]
                
                writer.writerow({'Similarity': str(cv_v),'File 1':str(f1),
                            'File 2':str(f2),'Time 1':st1,'Time 1 End':st2,
                            'Period 1':period1,'Culture 1':culture1,'Region 1':region1,'Time 2':et1,'Time 2 End':et2,
                            'Period 2':period2,'Culture 2':culture2,'Region 2':region2})
                
                print('Similarity: '+str(s)+ " File 1: "+str(f1)+" File 2: "+str(f2))
            
    except IOError:
        print ("Could not read file:", IOError)
    
'''
Main run metho to launch algorithm

Args:  argv:  the input from the run arguments. that includes threshold, hash_size, and bands
'''  
def run(argv):
    # Argument parser

    parser = argparse.ArgumentParser(description="Efficient detection of near-duplicate images using locality sensitive hashing")
    parser.add_argument("-i", "--inputdir", type=str, default="", help="directory containing images to check")
    parser.add_argument("-t", "--threshold", type=float, default=0.9, help="similarity threshold")
    parser.add_argument("-s", "--hash-size", type=int, default=16, help="hash size to use, signature length = hash_size^2", dest="hash_size")
    parser.add_argument("-b", "--bands", type=int, default=16, help="number of bands")

    args = parser.parse_args()
    
#    input_dir = args.inputdir
    threshold = args.threshold
    hash_size = args.hash_size
    bands = args.bands
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
    
    input_dir=os.path.join(pn,'input')
#    threshold=0.0
#    hash_size=20
#    bands=60
    
    imageFile=ImageFile()
    imageFile.readFile()
  
    try:
        near_duplicates = find_near_duplicates(input_dir, threshold, hash_size, bands)
        if near_duplicates:
            printResults(near_duplicates,imageFile)
            
        else:
            print("No near-duplicates found in " +str(input_dir) +" : "+ str(threshold))
    except OSError:
        print("Couldn't open input directory {input_dir}")
        
     
#   printHistorical(imageFile)               

if __name__ == "__main__":
    run(sys.argv)
