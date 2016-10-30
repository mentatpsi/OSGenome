import argparse
import os
import string


class PersonalData:
    def __init__(self, filepath):
        if os.path.exists(filepath):
            self.readData(filepath)

    def readData(self, filepath):
        with open(filepath) as file:
            relevantdata = [line for line in file.readlines() if line[0] != "#"]
            file.close()
        self.personaldata = [line.split("\t") for line in relevantdata]
        self.snps = [item[0] for item in self.personaldata]




if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filepath', help='Filepath for json dump to be used for import', required=False)

    args = vars(parser.parse_args())

    if args["filepath"]:
        pd = PersonalData(filepath=args["filepath"])
        print(len(pd.personaldata))
        print(pd.snps[:50])
