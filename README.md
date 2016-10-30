# OSGenome
An Open Source Library and ToolKit of Genetic Data (SNP) using 23AndMe and Data Crawling Technologies

OS Genome is an attempt to allow for users to gather the information they need to make sense of their own genome without needing to rely on outside services with unknown privacy policies. OS Genome's goal is to crawl various sources and give meaning to an individual's genome. It will create a front end Grid of the user's specific genome. 

In order to set up the requirements. Make sure you have python pip. The necessary dependencies can therein be added by pip install -r requirements.txt. This will install everything you need to use the script. It is written using Python 3. So make sure to use that when running the script.

Step 1:
python3 SNPedia/Datacrawler.py -f [Absolute path of your downloaded raw 23andMe data]

Step 2:
python3 SNPedia/SnpApi.py

Step 3:
Access http://127.0.0.1:5000 (hosted on your local machine) to look at your Genome

Examples:
![Example of Kendo Grid](https://github.com/mentatpsi/OSGenome/blob/master/OSGenome2.png)



![Example of Kendo Grid](https://github.com/mentatpsi/OSGenome/blob/master/OSGenome3.png)
