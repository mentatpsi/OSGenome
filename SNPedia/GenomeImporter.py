import argparse
import os
import string
import json
import requests
import pprint

class PersonalData:
    def __init__(self, filepath):
        if os.path.exists(filepath):
            self.readData(filepath)
            self.export()

    def readData(self, filepath):
        
        
        with open(filepath) as file:
            relevantdata = [line for line in file.readlines() if line[0] != "#"]
            file.close()
        

        ap = Approved()
        approved = dict(zip(ap.accepted,[i for i in range(len(ap.accepted))]))
        personaldata = [line.split("\t") for line in relevantdata]
        self.personaldata = [pd for pd in personaldata if pd[0].lower() in approved]
        
        self.snps = [item[0].lower() for item in self.personaldata]
        self.snpdict = {item[0].lower(): "(" + item[3].rstrip()[0] + ";" + item[3].rstrip()[-1] + ")" \
                        for item in self.personaldata}

    def hasGenotype(self, rsid):
        genotype = self.snpdict[rsid]
        return not genotype == "(-;-)"

    def export(self):
        if os.path.exists("SNPedia"):
            joiner = os.path.join(os.path.curdir,"SNPedia")
        else:
            joiner = os.path.curdir

        filepath = os.path.join(joiner, "data", 'snpDict.json')
        with open(filepath, "w") as jsonfile:
            json.dump(self.snpdict, jsonfile)


class Approved:
    def __init__(self):
        if not self.lastsessionexists():
            self.crawl()
            self.export()
        else:
            self.load()

    def load(self):
        if os.path.exists("SNPedia"):
            joiner = os.path.join(os.path.curdir,"SNPedia")
        else:
            joiner = os.path.curdir

        filepath = os.path.join(joiner, "data", 'approved.json')
        with open(filepath) as f:
            self.accepted = json.load(f)

    def lastsessionexists(self):
        if os.path.exists("SNPedia"):
            joiner = os.path.join(os.path.curdir,"SNPedia")
        else:
            joiner = os.path.curdir

        filepath = os.path.join(joiner, "data", 'approved.json')
        return os.path.isfile(filepath)

    def crawl(self, cmcontinue=None):
        members = []
        count = 0
        self.accepted = []
        print("Grabbing approved SNPs")
        if not cmcontinue:
            curgen = "https://bots.snpedia.com/api.php?action=query&list=categorymembers&cmtitle=Category:Is_a_snp&cmlimit=500&format=json"
            response = requests.get(curgen)
            jd = response.json()

            cur = jd["query"]["categorymembers"]
            for item in cur:
                self.accepted += [item["title"].lower()]
            cmcontinue = jd["continue"]["cmcontinue"]

        while cmcontinue:
            curgen = "https://bots.snpedia.com/api.php?action=query&list=categorymembers&cmtitle=Category:Is_a_snp&cmlimit=500&format=json&cmcontinue=" \
                    + cmcontinue
            response = requests.get(curgen)
            jd = response.json()
            cur = jd["query"]["categorymembers"]
            for item in cur:
                self.accepted += [item["title"].lower()]
            try:
                cmcontinue = jd["continue"]["cmcontinue"]
            except KeyError:
                cmcontinue = None
            count += 1
    def export(self):
        if os.path.exists("SNPedia"):
            joiner = os.path.join(os.path.curdir,"SNPedia")
        else:
            joiner = os.path.curdir

        filepath = os.path.join(joiner, "data", 'approved.json')
        with open(filepath, "w") as jsonfile:
            json.dump(self.accepted, jsonfile)

#https://bots.snpedia.com/api.php?action=query&list=categorymembers&cmtitle=Category:Is_a_snp&cmlimit=500&format=json


if __name__ == "__main__":

    

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filepath', help='Filepath for json dump to be used for import', required=False)

    args = vars(parser.parse_args())

    if args["filepath"]:
        pd = PersonalData(filepath=args["filepath"])
        print(len(pd.personaldata))
        print(pd.snps[:50])
        print(list(pd.snpdict.keys())[:10])
        print(list(pd.snpdict.values())[:10])
