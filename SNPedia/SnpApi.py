from flask import Flask, render_template, request, send_file, jsonify
import base64
from DataCrawler import SNPCrawl
import os
import io

app = Flask(__name__, template_folder='templates')

@app.route("/", methods=['GET', 'POST'])
def main():
    print(vars(request.form))
    filepath = os.path.join(os.path.curdir, "templates", 'snp_resource.html')
    return render_template('snp_resource.html')

@app.route("/excel", methods=['GET', 'POST'])
def create_file():
    content = request.form

    filename = content['fileName']
    filecontents = content['base64']
    filecontents = base64.b64decode(filecontents)

    bytesIO = io.BytesIO()
    bytesIO.write(filecontents)
    bytesIO.seek(0)

    return send_file(bytesIO,
                     attachment_filename=filename,
                     as_attachment=True)


@app.route("/api/rsids", methods=['GET'])
def get_types():
    return jsonify({"results":dfCrawl.rsidList})

if __name__ == "__main__":
    filepath = os.path.join(os.path.curdir, "data", 'rsidDict.json')
    snppath = os.path.join(os.path.curdir, "data", 'snpDict.json')
    if os.path.isfile(filepath):
        if os.path.isfile(snppath):
            dfCrawl = SNPCrawl(filepath=filepath, snppath=snppath)
        else:
            dfCrawl = SNPCrawl(filepath=filepath)
    app.run(debug=True)