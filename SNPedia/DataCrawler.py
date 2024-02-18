import logging
import re
import sys
from typing import Optional, Sequence

import requests
from bs4 import BeautifulSoup

import pprint
import json
import argparse
import os
import random

from GenomeImporter import PersonalData, Approved


COMPLEMENTS = {
    "A": "T",
    "T": "A",
    "C": "G",
    "G": "C",
}

VARIANT_REGEXP = re.compile(r'\(([ACTG-]);([ACTG-])\)')


class SNPCrawl:
    def __init__(self, filepath=None, snppath=None):
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

        self.createList()

    def crawl(self, rsids: Sequence[str]) -> None:
        rsids = [item.lower() for item in rsids]
        if rsids:
            self.initcrawl(rsids)
        self.export()
        self.createList()

    def initcrawl(self, rsids):
        count = 0
        with requests.Session() as session:
            for rsid in rsids:
                print(rsid)
                self.grabTable(rsid, session)
                print("")
                count += 1
                if count % 100 == 0:
                    print("%i out of %s completed" % (count, len(rsids)))
                    self.export()
                    print("exporting current results")
        pp = pprint.PrettyPrinter(indent=1)
        #pp.pprint(self.rsidDict)

    def grabTable(self, rsid: str, session: requests.Session) -> None:
        url = "https://bots.snpedia.com/index.php/" + rsid
        try:
            if rsid not in self.rsidDict.keys():
                self.rsidDict[rsid.lower()] = {
                    "Description": "",
                    "Variations": [],
                    "StabilizedOrientation": ""
                }
                response = session.get(url)
                html = response.content
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
        except requests.exceptions.RequestException:
            print(url + " was not found or contained no valid information")

    def tableToList(self, table):
        rows = table.find_all('tr')
        data = []
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])
        return data

    def _complement(self, variant: str) -> Optional[str]:
        m = VARIANT_REGEXP.match(variant)
        if m is None:
            #print("XXX", variant)
            return None

        comp1 = COMPLEMENTS.get(m.group(1))
        comp2 = COMPLEMENTS.get(m.group(2))
        if comp1 > comp2:
            # It seems there is a convention to put them in alphabetic order
            comp1, comp2 = comp2, comp1
        return f"({comp1};{comp2})"

    def _chooseVariation(self, our_snp, variations, stbl_orient: str, debug_rsid: str) -> Optional[int]:
        for i, variation in enumerate(variations):
            if stbl_orient == "plus":
                our_oriented_snp = our_snp
            elif stbl_orient == "minus":
                # TODO: Stabilized orientation doesn't always works (e.g., rs10993994 for GRCh38). Probably we should
                #  look at reference genome used in SNPedia and in the analyzed genome.
                our_oriented_snp = self._complement(our_snp)
            else:
                return None

            if our_oriented_snp == variation[0]:
                return i

        if len(variations) == 3:  # Usually contains all variants.
            logging.warning(f"Couldn't find {our_snp} in {variations} ({debug_rsid}, {stbl_orient})")
        return None

    def createList(self):
        make = lambda rsname, description, variations, stbl_orientation, importance: \
            {"Name": rsname,
             "Description": description,
             "Importance": importance,
             "Genotype": self.snpdict[rsname.lower()] \
                if rsname.lower() in self.snpdict.keys() else "(-;-)", \
             "Variations": str.join("<br>", variations), \
                "StabilizedOrientation":stbl_orientation 
            }

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

            variations_data = curdict["Variations"]
            if rsid.lower() in self.snpdict.keys():
                variation_idx = self._chooseVariation(
                    our_snp=self.snpdict[rsid.lower()],
                    variations=variations_data,
                    stbl_orient=stbl_orient,
                    debug_rsid=rsid.lower(),
                )
            else:
                variation_idx = None

            variations = [" ".join(variation) for variation in variations_data]
            importance = None
            if variation_idx is not None:
                variations[variation_idx] = f'<b>{variations[variation_idx]}</b>'
                try:
                    if len(variations_data[variation_idx]) > 1:
                        importance = float(variations_data[variation_idx][1])
                except ValueError:
                    pass  # Ignore missing importance.

            maker = make(rsid, curdict["Description"], variations, stbl_orient, importance)
            
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


#Some interesting SNPs to get started with
SEED_RSIDS = [
    "rs1815739", "Rs53576", "rs4680", "rs1800497", "rs429358", "rs9939609", "rs4988235", "rs6806903", "rs4244285",
    "rs1801133",
]

#os.chdir(os.path.dirname(__file__))


def find_relevant_rsids(
        personal: PersonalData,
        crawl: SNPCrawl,
        count: int,
) -> Sequence[str]:
    snps_of_interest = [snp for snp in personal.snps if personal.hasGenotype(snp)]
    snps_to_grab = [snp for snp in snps_of_interest if snp not in crawl.rsidDict]
    print(f"Yet to load: {len(snps_to_grab)}/{len(snps_of_interest)} genome SNPs available in SNPedia")
    snps_to_grab_set = set(snps_to_grab)

    result = []
    for rsid in SEED_RSIDS:
        if rsid in snps_to_grab_set:
            result.append(rsid)

    if len(result) < count:
        random.shuffle(snps_to_grab)
        result.extend(snps_to_grab[:count - len(result)])

    print(f"Chose {len(result)} SNPs to load")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filepath', help='Filepath for 23andMe data to be used for import', required=False)
    parser.add_argument('-n', '--count', help='Number of SNPs to download', type=int, default=100)
    args = parser.parse_args()

    if os.path.exists("SNPedia"):
        joiner = os.path.join(os.path.curdir,"SNPedia")
    else:
        joiner = os.path.curdir
    filepath = os.path.join(joiner, "data", 'rsidDict.json')
    if os.path.isfile(filepath):
        dfCrawl = SNPCrawl(filepath=filepath)
    else:
        dfCrawl = SNPCrawl()

    if args.filepath:
        rsids_on_snpedia = Approved()
        personal = PersonalData(args.filepath, rsids_on_snpedia)
        rsids = find_relevant_rsids(personal, dfCrawl, count=args.count)
    else:
        rsids = SEED_RSIDS

    dfCrawl.crawl(rsids)


if __name__ == "__main__":
    main()
