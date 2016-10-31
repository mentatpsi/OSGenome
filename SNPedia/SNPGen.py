import requests
import json



class GrabSNPs:
    def __init__(self, crawllimit=500):
        self.snps = []
        self.limit = crawllimit
        self.crawl()
    def crawl(self):
        curgen = "http://bots.snpedia.com//api.php?action=query&format=json&list=categorymembers&rawcontinue=0&cmtitle=Category%3Ais_a_snp"
        response = requests.get(curgen)
        jd = response.json()
        print(jd)
        members = []
        members.append(jd["query"]["categorymembers"])
        cmcontinue = jd["query-continue"]["categorymembers"]["cmcontinue"]
        count = 0
        print(type(cmcontinue))
        while cmcontinue and count <= self.limit:
            curgen = "http://bots.snpedia.com//api.php?action=query&format=json&list=categorymembers&rawcontinue=0&cmtitle=Category%3Ais_a_snp&cmcontinue=" \
                     + cmcontinue
            response = requests.get(curgen)
            jd = response.json()
            members.append(jd["query"]["categorymembers"])
            cmcontinue = jd["query-continue"]["categorymembers"]["cmcontinue"]
            count += 1

        print(members)
        members = [[i["title"] for i in item] for item in members]

        for member in members:
            self.snps.extend(member)


if __name__ == "__main__":
    sn = CrawlSNPS()
    print(sn.snps)
