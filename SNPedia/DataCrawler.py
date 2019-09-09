import sys


from bs4 import BeautifulSoup
from random import shuffle

import urllib.request
import pprint
import json
import argparse
import os
import random


from SNPGen import GrabSNPs
from GenomeImporter import PersonalData


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
            if rsid not in self.rsidDict.keys():
                self.rsidDict[rsid.lower()] = {
                    "Description": "",
                    "Variations": []
                }
                response = urllib.request.urlopen(url)
                html = response.read()
                bs = BeautifulSoup(html, "html.parser")
                table = bs.find("table", {"class": "sortable smwtable"})
                description = bs.find('table', {'style': 'border: 1px; background-color: #FFFFC0; border-style: solid; margin:1em; width:90%;'})

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
        make = lambda rsname, description, variations: \
            {"Name": rsname,
             "Description": description,
             "Genotype": self.snpdict[rsname.lower()] \
             if rsname.lower() in self.snpdict.keys() else "(-;-)", \
             "Variations": str.join("<br>", variations)}

        formatCell = lambda rsid, variation : \
            "<b>" + str.join(" ", variation) + "</b>" \
                if rsid.lower() in self.snpdict.keys() and \
                   self.snpdict[rsid.lower()] == variation[0] \
                else str.join(" ", variation)

        for rsid in self.rsidDict.keys():
            curdict = self.rsidDict[rsid]
            variations = [formatCell(rsid, variation) for variation in curdict["Variations"]]
            self.rsidList.append(make(rsid, curdict["Description"], variations))

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
        filepath = os.path.join(os.path.curdir, "data", 'rsidDict.json')
        with open(filepath,"w") as jsonfile:
            json.dump(self.rsidDict, jsonfile)


parser = argparse.ArgumentParser()


parser.add_argument('-f', '--filepath', help='Filepath for 23andMe data to be used for import', required=False)

args = vars(parser.parse_args())


#Some interesting SNPs to get started with
rsid = ["rs1815739", "Rs53576", "rs4680", "rs1800497", "rs429358", "rs9939609", "rs4988235", "rs6806903", "rs4244285"]
rsid += ["rs1801133"]

#os.chdir(os.path.dirname(__file__))


if args["filepath"]:
    personal = PersonalData(args["filepath"])
    snpsofinterest = [snp for snp in personal.snps if personal.hasGenotype(snp)]
    sp = GrabSNPs(crawllimit=60, snpsofinterest=snpsofinterest, target=100)
    rsid += sp.snps
    print(len(sp.snps))
    temp = personal.snps
    random.shuffle(temp)
    print(temp[:10])
    rsid += temp[:50]


if __name__ == "__main__":
    filepath = os.path.join(os.path.curdir, "data", 'rsidDict.json')
    if os.path.isfile(filepath):
        dfCrawl = SNPCrawl(rsids=rsid, filepath=filepath)

    else:
        dfCrawl = SNPCrawl(rsids=rsid)
