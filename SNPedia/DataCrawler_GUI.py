
import sys

    
from bs4 import BeautifulSoup
from random import shuffle

import urllib.request
import pprint
import json
import argparse
import os
import random

from tkinter import filedialog
from tkinter import *



from SNPGen import GrabSNPs
from GenomeImporter import PersonalData, Approved


class SNPCrawl:
    def __init__(self, rsids=[], filepath=None, snppath=None):
        if filepath and os.path.isfile(filepath):
            self.importDict(filepath)
            self.rsidList = []
        else:
            self.rsidDict = {}
            self.rsidList = []

        if snppath and os.path.isfile(snppath):
            self.importSNPs(snppath)
        else:
            self.snpdict = {}

        rsids = [item.lower() for item in rsids]
        if rsids:
            self.initcrawl(rsids)
        self.export()
        self.createList()

    def initcrawl(self, rsids):
        count = 0
        for rsid in rsids:
            print(rsid)
            self.grabTable(rsid)
            print("")
            count += 1
            if count % 100 == 0:
                print("%i out of %s completed" % (count, len(rsids)))
                self.export()
                print("exporting current results")
        pp = pprint.PrettyPrinter(indent=1)
        #pp.pprint(self.rsidDict)

    def grabTable(self, rsid):
        try:
            url = "https://bots.snpedia.com/index.php/" + rsid
            if rsid[0] == "r":
                x = 0
            if rsid not in self.rsidDict.keys():
                self.rsidDict[rsid.lower()] = {
                    "Description": "",
                    "Variations": [],
                    "StabilizedOrientation": ""
                }
                response = urllib.request.urlopen(url)
                html = response.read()
                bs = BeautifulSoup(html, "html.parser")
                table = bs.find("table", {"class": "sortable smwtable"})
                description = bs.find('table', {'style': 'border: 1px; background-color: #FFFFC0; border-style: solid; margin:1em; width:90%;'})
                
                #Orientation Finder
                orientation = bs.find("td", string="Rs_StabilizedOrientation")
                if orientation:
                    plus = orientation.parent.find("td",string="plus")
                    minus = orientation.parent.find("td",string="minus")
                    if plus:
                        self.rsidDict[rsid]["StabilizedOrientation"] = "plus"
                    if minus:
                        self.rsidDict[rsid]["StabilizedOrientation"] = "minus" 
                else:
                      link = bs.find("a",{"title":"StabilizedOrientation"})
                      if link:
                        table_row = link.parent.parent
                        plus = table_row.find("td",string="plus")
                        minus = table_row.find("td",string="minus")
                        if plus:
                            self.rsidDict[rsid]["StabilizedOrientation"] = "plus"
                        if minus:
                            self.rsidDict[rsid]["StabilizedOrientation"] = "minus" 


                if description:
                    d1 = self.tableToList(description)
                    self.rsidDict[rsid]["Description"] = d1[0][0]
                    print(d1[0][0].encode("utf-8"))
                if table:
                    d2 = self.tableToList(table)
                    self.rsidDict[rsid]["Variations"] = d2[1:]

                    print(d2[1:])
        except urllib.error.HTTPError:
            print(url + " was not found or contained no valid information")

    def tableToList(self, table):
        rows = table.find_all('tr')
        data = []
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])
        return data

    def createList(self):
        make = lambda rsname, description, variations, stbl_orientation: \
            {"Name": rsname,
             "Description": description,
             "Genotype": self.snpdict[rsname.lower()] \
                if rsname.lower() in self.snpdict.keys() else "(-;-)", \
             "Variations": str.join("<br>", variations), \
                "StabilizedOrientation":stbl_orientation 
            }

        formatCell = lambda rsid, variation, stbl_orient : \
            "<b>" + str.join(" ", variation) + "</b>" \
                if rsid.lower() in self.snpdict.keys() and \
                   self.snpdict[rsid.lower()] == variation[0] \
                    and stbl_orient == "plus" \
                else str.join(" ", variation)

        messaged_once = False
        for rsid in self.rsidDict.keys():
            curdict = self.rsidDict[rsid]
            if "StabilizedOrientation" in curdict:
                stbl_orient = curdict["StabilizedOrientation"]
            else:
                stbl_orient = "Old Data Format"
                if not messaged_once:
                    print("Old Data Detected, Will not display variations bolding with old data.") 
                    print("See ReadMe for more details")
                    messaged_once = True
            variations = [formatCell(rsid, variation, stbl_orient) for variation in curdict["Variations"]]
            
            maker = make(rsid, curdict["Description"], variations, stbl_orient)
            
            self.rsidList.append(maker)

        #print(self.rsidList[:5])

    def importDict(self, filepath):
        with open(filepath, 'r') as jsonfile:
            self.rsidDict = json.load(jsonfile)

    def importSNPs(self, snppath):
        with open(snppath, 'r') as jsonfile:
            self.snpdict = json.load(jsonfile)

    def export(self):
        #data = pd.DataFrame(self.rsidDict)
        #data = data.fillna("-")
        #data = data.transpose()
        #datapath = os.path.join(os.path.curdir, "data", 'rsidDict.csv')
        #data.to_csv(datapath)
        if os.path.exists("SNPedia"):
            joiner = os.path.join(os.path.curdir,"SNPedia")
        else:
            joiner = os.path.curdir
        filepath = os.path.join(joiner, "data", 'rsidDict.json')
        with open(filepath,"w") as jsonfile:
            json.dump(self.rsidDict, jsonfile)


#parser = argparse.ArgumentParser()


#parser.add_argument('-f', '--filepath', help='Filepath for 23andMe data to be used for import', required=False)

#args = vars(parser.parse_args())


#Some interesting SNPs to get started with
rsid = ["rs1815739", "Rs53576", "rs4680", "rs1800497", "rs429358", "rs9939609", "rs4988235", "rs6806903", "rs4244285"]
rsid += ["rs1801133"]


#os.chdir(os.path.dirname(__file__))

root = Tk()


if os.path.exists("lastsave.txt"):
    last_save = open("lastsave.txt","r")
    last_path = last_save.read()
    last_save.close()
else:
    last_path = "/"


root.filename = filedialog.askopenfilename(initialdir = last_path,title = "Select file",filetypes = (("text files","*.txt"),("all files","*.*")))
#print (root.filename)

root.destroy()
filepath = root.filename

if os.path.exists("SNPedia"):
    joiner = os.path.join(os.path.curdir,"SNPedia")
else:
    joiner = os.path.curdir

path_split = os.path.split(joiner)
last_save = open("lastsave.txt","w")

last_save.write(path_split[0])
last_save.close()




if filepath:
    rsids_on_snpedia = Approved()
    personal = PersonalData(filepath, rsids_on_snpedia)
    snpsofinterest = [snp for snp in personal.snps if personal.hasGenotype(snp)]
    count_of_interest = len(snpsofinterest)
    print("Found " + str(count_of_interest) + " SNPS to be mapped to SNPedia")
    sp = GrabSNPs(crawllimit=60, snpsofinterest=snpsofinterest, target=100)
    rsid += sp.snps
    print(len(sp.snps))
    temp = personal.snps
    random.shuffle(temp)
    print(temp[:10])
    rsid += temp[:50]


if __name__ == "__main__":
    if os.path.exists("SNPedia"):
        joiner = os.path.join(os.path.curdir,"SNPedia")
    else:
        joiner = os.path.curdir
    filepath = os.path.join(joiner, "data", 'rsidDict.json')
    if os.path.isfile(filepath):
        dfCrawl = SNPCrawl(rsids=rsid, filepath=filepath)

    else:
        dfCrawl = SNPCrawl(rsids=rsid)
