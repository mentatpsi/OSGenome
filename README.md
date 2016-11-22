# OSGenome
An Open Source Library and ToolKit of Genetic Data (SNP) using 23AndMe and Data Crawling Technologies

##Description
OS Genome is an attempt to allow for users to gather the information they need to make sense of their own genome without needing to rely on outside services with unknown privacy policies. OS Genome's goal is to crawl various sources and give meaning to an individual's genome. It creates a front end Grid of the user's specific genome. This allows for everything from filtering to excel exporting. All of which using Flask. 

##What are SNPs?
From Bioinformatics - A Practical Approach by Shui Qing Ye (pg 108):

>SNP, pronounced “snip,” stands for single-nucleotide polymorphism, which represents a substitution of one base for another, e.g., C to T or A to G. SNP is the most common variation in the human genome and occurs approximately once every 100 to 300 bases. SNP is terminologically distinguished from mutation based on an arbitrary population frequency cutoff value: 1%, with SNP [greater than] 1% and mutation [less than] 1%. A key aspect of research in genetics is associating sequence variations with heritable phenotypes. Because SNPs are expected to facilitate large-scale association genetics studies, there has been an increasing interest in SNP discovery and detection.

23andMe gathers hundreds of thousands of SNPs that give you everything from your genetic ancestry (haplogroups) to whether you are more likely to think Cilantro tastes like soap, or how quickly you likely digest coffee. Unfortunately, and fortunately, there is a lot of information out there on each specific SNP and what associations they might have. Much like Phrenology of the late 18th and early 19th century, where personality was attempted to be associated to facial features, there can be a lot of attempts to draw conclusions in noise. Enter OS Genome, where you can discover links and research at your own pace with the information you gather. It will highlight what specific Genotype is yours, and what that means in the context of discovery. From there you can google the relevant SNP id at your own intrigue.

##Where is my information stored?
All of your genetic data (your raw data) is stored and used locally on your computer. At no point does this software send your data anywhere. It is used in personalizing OS Genome to you.


##How do I grab my raw SNP Data?
Since it's quite possible 23AndMe will change the way you download the raw data... this might change from time to time. Just look up how to download 23AndMe raw data in Google, and you might just find a link to 23AndMe to download the raw data. It'll be in a comma separated format. 

##Installation:

In order to set up the requirements. Make sure you have [python pip](https://packaging.python.org/installing/). The necessary dependencies can therein be added by pip install -r requirements.txt. This will install everything you need to use the script. It is written using Python 3. So make sure to use that when running the script.

Step 0:
```
pip install -r requirements.txt
```
This sets up the necessary dependencies (such as Flask, used to create a Python based web server and BeautifulSoup used to crawl through SNPedia).


Step 1:
```
python3 SNPedia/Datacrawler.py -f [Absolute path of your downloaded raw 23andMe data]
```
This sets up the datacrawler using your data as a means to highlight what SNPs are relevant to you. 


Step 2:
```
python3 SNPedia/SnpApi.py
```
This sets us the Flask server


Step 3:
Access http://127.0.0.1:5000 (the ip address also known as localhost, it's all hosted on your local machine) to look at your Genome

##Example
![Example of Kendo Grid](https://github.com/mentatpsi/OSGenome/blob/master/images/OSGenome_mp2.png)
