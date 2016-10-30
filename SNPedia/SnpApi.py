from flask import Flask, render_template, jsonify
import argparse
from DataCrawler import SNPCrawl
import os

app = Flask(__name__, template_folder='templates')

@app.route("/")
def main():
    filepath = os.path.join(os.path.curdir, "templates", 'snp_resource.html')
    return render_template('snp_resource.html')

@app.route("/api/rsids", methods=['GET'])
def get_types():
    return jsonify({"results":dfCrawl.rsidList})

if __name__ == "__main__":
    filepath = os.path.join(os.path.curdir, "data", 'rsidDict.json')
    if os.path.isfile(filepath):
        dfCrawl = SNPCrawl(filepath=filepath)
    app.run(debug=True)