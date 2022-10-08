# OSGenome
An Open Source Web Application for Genetic Data (SNPs) using 23AndMe and Data Crawling Technologies

## Description
OS Genome is an open source web application that allows users to gather the information they need to make sense of their own genome without needing to rely on outside services with unknown privacy policies. OS Genome's goal is to crawl various sources and give meaning to an individual's genome. It creates a Responsive Grid of the user's specific genome. This allows for everything from filtering to excel exporting. All of which using Flask, Kendo, and Python programming.


## What are SNPs?
From Bioinformatics - A Practical Approach by Shui Qing Ye, M.D., Ph.D. (pg 108):

>SNP, pronounced “snip,” stands for single-nucleotide polymorphism, which represents a substitution of one base for another, e.g., C to T or A to G. SNP is the most common variation in the human genome and occurs approximately once every 100 to 300 bases. SNP is terminologically distinguished from mutation based on an arbitrary population frequency cutoff value: 1%, with SNP [greater than] 1% and mutation [less than] 1%. A key aspect of research in genetics is associating sequence variations with heritable phenotypes. Because SNPs are expected to facilitate large-scale association genetics studies, there has been an increasing interest in SNP discovery and detection.

23andMe gathers hundreds of thousands of SNPs that give you everything from your genetic ancestry (haplogroups) to whether you are more likely to think Cilantro tastes like soap, or how quickly you likely digest coffee. Unfortunately, and fortunately, there is a lot of information out there on each specific SNP and what associations they might have. Much like Phrenology of the late 18th and early 19th century, where personality was attempted to be associated to facial features, there can be a lot of attempts to draw conclusions in noise. Enter OS Genome, where you can discover links and research at your own pace with the information you gather. It will highlight what specific Genotype is yours, and what that means in the context of discovery. From there you can google the relevant SNP id at your own intrigue or use the Lookup on SNPedia button to discover more about that SNP on SNPedia.


## Where is my information stored?
All of your genetic data (your raw data) is stored and used locally on your computer. At no point does this software send your data anywhere. It is used in personalizing OS Genome to you.


## How do I grab my raw SNP Data?
Since it's quite possible 23AndMe will change the way you download the raw data... this might change from time to time. Just look up how to download 23AndMe raw data in Google, and you might just find a link to 23AndMe to download the raw data. It'll be in a comma separated format. 

## Orientation (Important)
SNPedia reports SNPs as Positive strands per tradition of public snp datasets and the initial build it was made out of [(More research here)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6099125/). While the latest algorithm might report them as negative or plus. What this means is that for Stabilized Orientations, you must flip the orientation to get the correct genotype as mapped by SNPedia if the Stabilize Orientation is equal to minus. OSGenome automatically relays the Stabilized Orientation, but to avoid confusion, does not map the corrected genotype and also does not highlight the correct variation. This is not done as builds might change one day and this fix might not be needed. [See here for more information by SNPedia authors](https://www.reddit.com/r/promethease/comments/3ayg64/orientation_confusion/). In best words, if the orientation is minus, add a layer of ambiguity to your test results for the SNP, flip the orientation (as of 2022) as this is a result of build differences across what SNPedia was built on, and what 23AndMe and others genome testing report. Currently, Human Genome testing uses [GRCh38](https://www.nature.com/articles/d41586-021-00462-9#:~:text=The%20most%20recent%20version%20of,has%20been%20repeatedly%20'patched), but it's unknown if and when it'll change. A tutorial on how to do the flip can be foun [here](https://www.snpedia.com/index.php/Orientation#:~:text=Orientation%20indicates%20the%20orientation%20reported,reference%20build%20is%20shown%20next) 


## Does OS Genome work through other SNP/Ancestry sites?
Currently, there is a script I can upload to convert the formats. MyFamilyTree.com, for instance, uses a comma to separate their data, while 23AndMe uses tabs, that's pretty much the main difference. If there's enough demand, I can easily include it to the workflow... so feel free to request the addition. As OS Genome improves, a lot of functionality is likely to arise.


## How much data will OS Genome grab?
Last checked, 23AndMe had over 610,000 SNPs that comes from their raw SNP file, while MyFamilyTree.com had over 700,000 SNPs. OS Genome crawls a couple hundred each time. Each time you run step 1, it'll add additional several hundred SNPs to your result for you to examine. This was done to reduce the amount of data that needs to be crawled before you have something to examine. OSGenome relies on the SNPs that SNPedia has covered. Last checked, there were 110402 SNPS. So it will keep growing as SNPedia adds more SNPs into their database.  Feel free to run step 1 as often as you'd like to gain additional data, and no worries... it keeps track of your progress. 

## It maxes out at 20,000 SNPs?
At current, if you cross reference a 23andMe report with SNPedia, it will have a valid set of 20,000 SNPs. I've created a modification to the application to only get the SNPs that SNPedia approves as requested in their terms (this prevents it from denying entry). Running this script on a sample 23andMe output has revealed that there are a maximum of around 20,000 SNPs in their encyclopedia for analysis of 23andMe reports. The modification is found within the GenomeImporter. It continously crawls the API endpoint for finding the approved SNPs and uses a dictionary to take advantage of the time complexity of the hash function. It then creates a JSON file within the data directory called approved.json. If after awhile you want to revisit this application. This is one of the files to delete.

## What are some additional features?
OS Genome also has Excel Exporting, SNPedia Lookup, and filtering. SNPedia Lookup works by selecting the row you're interested in looking into and pressing the Lookup on SNPedia button. It will open up a new window with the details of the SNP.

## Contributions
There have been three contributions so far.
- Daniel McNally [@sangaman](https://github.com/sangaman) | Python 3.10 Compatability through dependencies and ReadMe improvements
- Dan Grahn [@dgrahn](https://github.com/dgrahn) | Front End Improvements

## Disclaimer
Raw Data coming from Genetic tests done by Direct To Consumer companies such as 23andMe and Ancestry.com were found to have a false positive rate of 40% for genes with clinical significance in a March 2018 study [*False-positive results released by direct-to-consumer genetic tests highlight the importance of clinical confirmation testing for appropriate patient care*](https://www.nature.com/articles/gim201838). For this reason, it's important to confirm any at risk clinical SNPs with your doctor who can provide genetic tests and send them to a clinical laboratory.

## Installation:

In order to set up the requirements. Make sure you have [python pip](https://packaging.python.org/installing/). The necessary dependencies can therein be added by pip install -r requirements.txt. This will install everything you need to use the script. It is written using Python 3. So make sure to use that when running the script and make sure environmental variables of PATH were set during installation of Python for Windows.

Step 0:
```
pip install -r requirements.txt
```
This sets up the necessary dependencies (such as Flask, used to create a Python based web server and BeautifulSoup used to crawl through SNPedia).


Step 1 (option 1):
```
python3 SNPedia/DataCrawler.py -f [Absolute path of your downloaded raw 23andMe data]
```
This sets up the datacrawler using your data as a means to highlight what SNPs are relevant to you. 


Step 1 (option 2):
```
python3 SNPedia/DataCrawler_GUI.py
```
This sets up the datacrawler with a file dialog using your data as a means to highlight what SNPs are relevant to you.

Step 2:
```
python3 SNPedia/SnpApi.py
```
This sets us the Flask server


## Access the Local Server
Access http://127.0.0.1:5000 (the ip address also known as localhost, it's all hosted on your local machine) to look at your Genome

## arv support
There exists a library arv ([GitHub: cslarsen/arv - A fast 23andMe DNA parser and inferrer for Python](https://github.com/cslarsen/arv)) that allows for rule based matching of health and trait attributes using a hash table of the raw data of 23andMe. It is possible to alter the rsidDict.json to allow for automatically populating the rule matching conditions. I will be designing this functionality in a python script that will be able to be used to import the JSON as a dictionary that can be called within the rule matching. Please keep in mind its respective disclaimers before using the service. 

## Example
![Example of Kendo Grid](https://github.com/mentatpsi/OSGenome/blob/master/images/OSGenome6.PNG)
