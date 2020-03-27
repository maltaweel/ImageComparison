**ImageComparison**

ImageComparison is a small Python 3 application used to compare different images, of any size, using locality sensitive hashing (LSH). Other algorithms, including mean square error and structural similarity. The following describes the key modules, packages, and data utilised in this work.

_Python Libraries Used_

scikit-image 0.16.2  
matplotlib 3.1.1  
numpy 1.17.4  
networkx 2.4  
geopandas 0.6.2  
ImageHash 4.0 \n
opencv-python 4.2.0.32  
Pillow 6.2.1  
pysal 2.1.0  
pyshp 2.1.0

_Description_

The following describes the key functions of the modules incorporated. This includes key data and data folders. All code can be found in the /src folder included within ImageComparsion. The code in the /src folder also contains comments about individuals methods and variables used to create the output. The code in scr/lsh/detect.py runs the LSH algorithm and can be launched to run on images. Users can change the folder for data or move images to the /input folder. The code in scr/network/shapefileMaker.py creates the network_output results, including the network.shp, network.csv and points.shp outputs. All relevant outputs discussed in the paper can be found in either the period-relevant folders with the image data (e.g., 9-4/) or the output/ and network-output/ folders for the overall image analysis. 

9-4/:

This is a data folder that contains images and descriptor file about the images (imageLink.csv) that indicates regions and periods that images date to. All of the images date between the 9th-4th centuries BCE. The images are .jpg files. The folder also contains a network_output sub-folder, which includes network.shp output that contains the network output for image comparisons. The other files in this sub-folder are network.csv, a .csv version of the .shp output, and points.shp, which is the summed centrality output. The network data indicates link similarity scores based on median values. The raw data for each image comparison is in a output_lsh file. 

doc/: 

Folder contains documentation about the src/ folder, that is the Python code, used for the package. The doc/ folder is organised by having an html/ sub-folder, with sub-folders under this that correspond to the sub-folder of the src/. These sub-folders contain .html files that discuss the relevant modules with the same name except without the .py extension. For example, in the /lsh sub-folder, detect.html discusses the detect.py module in /src/lsh/.

image_data/:

This folder contains imageLink.csv, which is the imageLink file for all sculpture images (found in the input/ folder). The information in the file includes the periods and regions the images in the input/ folder belong to.

input/:

This is a folder that contains all of the sculpture images. These same images can be found in the period folders (e..g, 9-4).

network_output/:

This contains the network output files, mainly network.shp and the point.shp files. This also contains the network.csv file, a csv version. The files are for link simiarlity value for all the images (231) compared (network files) and also the nodes summed centrality values (points.shp).

output/:

This contains a output_lsh file that shows the raw comparisons between images in similarity. This is the output of the Locality Sensitive Hashing algorithm.

post4th/:

This folder contains the same structure and output file types as 9-4/, except the sculptures (images) date to the post-4th century BCE. The network_output folder contains the relevant files for networks for this period. The imageLink.csv file describes the sculptures for this folder.

pre9th/:

This folder contains the same structure and output file types as 9-4/, except the sculptures (images) date to the pre-9th century BCE. The network_output folder contains the relevant files for networks for this period. The imageLink.csv file describes the sculptures for this folder.

shp/:

This folder contains a shapefile (TM_WORLD_BORDERS-0.3) of countries that are used for nodes in the network files for sculpture comparisons. The nodes represent countries that are within archaeological/ancient regions (e.g, Mesopotamia equated with Iraq). The shapefile is used to help build the network and map it to a geographic location.
 
src/: 

This is the folder that contains the code. The following are the sub-folders with the Python code.

     img/:
   
     The img/ folder contains the comparison.py module. This module deploys structural similarity and mean squared error.          This module is not currently used. It was tested to compare to the LSH method. The module uses the images folder, but        this folder is empty. The module would work if images are of the same size.
     
     lsh/:
     
     This sub-folder contains the main module for the LSH, or local sensitive hashing, method. The detect.py module applies        the LSH algorithm that compares similarity of images. THe other module is imageFileDataLoader.py, which loads images and      applies comparisons between multiple images.Data in the imageLink.csv files allow images to be referenced and matched to      given regions, which are then used for comparisons.
     
     network/:
     
     This folder contains the modules for network construction. The shapefileMaker.py enables the network to be created using      the nodes for each country and images associated with given countries (i.e., representing regions in the past). The          graph.py module creates a degree centrality network, but this is not currently used. The output files created are            centrality.csv and points.shp.


_imageLink.csv_

This file is used as a descriptor for the data. The file contains the following columns:  file, time, period, culture, region, and modern country. In the image_data/ folder, the imageLink.csv file also has the category 'source.' The other imageLink.csv files do not have the category source, as the data are found in the imageLink.csv in /image_data. The file is the name of the file. The time column reflects the time range in which the data falls. Negative values are used for BCE dates, while positive values are CE dates. The range of time is given using a colon between the end dates of the range. The period is the local period scheme used for the time range. The culture is the ancient culture in reference. The region is the ancient region, as indicated by common archaeological literature, that the sculpture relates to. The modern country is the approximate or actual country an object is found within. The modern country could simply represent the ancient region, even if the ancient region may extend into other countries. This is mostly used so the image can be mapped to a node in the network analysis. The source is the source of the object, such as museum or if unknown from Google Images.

