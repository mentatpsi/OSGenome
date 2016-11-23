import requests


class GrabSNPs:
    """GrabSNPs(crawllimit, target, snpofinterest) ->
    crawls and attains a list of SNPedia compatible SNPs found within the snps of interest array
    """

    def __init__(self, crawllimit=300, snpsofinterest=None, target=50):
        self.cmcontinue = ""
        print(snpsofinterest[:50])
        self.snps = []
        self.limit = crawllimit
        self.target = target
        if snpsofinterest:
            self.crawl(snpsofinterest=snpsofinterest, target=target)
        else:
            self.crawl(target=target)

    def crawl(self, snpsofinterest=None, cmcontinue=None, target=100):
        members = []
        print(cmcontinue)
        count = 0
        if not cmcontinue:
            curgen = "http://bots.snpedia.com//api.php?action=query&format=json&list=categorymembers&rawcontinue=0&cmtitle=Category%3Ais_a_snp"
            response = requests.get(curgen)
            jd = response.json()
            
            print(jd)

            members.append(jd["query"]["categorymembers"])
            cmcontinue = jd["query-continue"]["categorymembers"]["cmcontinue"]

        while cmcontinue and count <= self.limit:
            curgen = "http://bots.snpedia.com//api.php?action=query&format=json&list=categorymembers&rawcontinue=0&cmtitle=Category%3Ais_a_snp&cmcontinue=" \
                     + cmcontinue
            response = requests.get(curgen)
            jd = response.json()
            #print(jd)
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



