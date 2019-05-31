import requests
import os


class GrabSNPs:
    """GrabSNPs(crawllimit, target, snpofinterest) ->
    crawls and attains a list of SNPedia compatible SNPs found within the snps of interest array
    """

    def __init__(self, crawllimit=500, snpsofinterest=None, target=50):
        self.cmcontinue = ""
        self.snps = []
        self.limit = crawllimit
        self.target = target
        if self.lastsessionexists():
            cmcontinue = self.importlast()
        else:
            cmcontinue = None

        if snpsofinterest:
            self.crawl(snpsofinterest=snpsofinterest, cmcontinue=cmcontinue, target=target)
        else:
            self.crawl(target=target, cmcontinue=cmcontinue)
        self.export()


    def crawl(self, snpsofinterest=None, cmcontinue=None, target=100):
        members = []
        count = 0
        if not cmcontinue:
            curgen = "https://bots.snpedia.com//api.php?action=query&format=json&list=categorymembers&rawcontinue=0&cmtitle=Category%3Ais_a_snp"
            response = requests.get(curgen)
            jd = response.json()

            members.append(jd["query"]["categorymembers"])
            cmcontinue = jd["query-continue"]["categorymembers"]["cmcontinue"]

        while cmcontinue and count <= self.limit:
            curgen = "https://bots.snpedia.com//api.php?action=query&format=json&list=categorymembers&rawcontinue=0&cmtitle=Category%3Ais_a_snp&cmcontinue=" \
                     + cmcontinue
            response = requests.get(curgen)
            jd = response.json()
            members.append(jd["query"]["categorymembers"])
            cmcontinue = jd["query-continue"]["categorymembers"]["cmcontinue"]
            count += 1

        members = [[i["title"] for i in item] for item in members]

        for member in members:
            self.snps.extend(member)

        if snpsofinterest:
            self.snps = [snp for snp in self.snps if snp.lower() in snpsofinterest]
            print(len(self.snps))

        if len(self.snps) < target:
            self.crawl(snpsofinterest=snpsofinterest, cmcontinue=cmcontinue, target=target)

        self.cmcontinue = cmcontinue

    def lastsessionexists(self):
        filepath = os.path.join(os.path.curdir, "data", 'last_session.txt')
        return os.path.isfile(filepath)

    def importlast(self):
        filepath = os.path.join(os.path.curdir, "data", 'last_session.txt')
        lastsession = open(filepath, "r")
        lines = lastsession.readlines()
        lastsession.close()
        lastsessionvalue = lines[0].strip("\n")
        print(lastsessionvalue)
        return lastsessionvalue


    def export(self):
        filepath = os.path.join(os.path.curdir, "data", 'last_session.txt')
        with open(filepath, "w") as lastsession:
            lastsession.write(self.cmcontinue)
            lastsession.close()




