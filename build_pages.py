import os
import os.path
import json
import shutil
import subprocess
import codecs
import re
from operator import itemgetter

import jinja2
import yaml
import PyPDF2
import markdown


env = jinja2.Environment(loader=jinja2.FileSystemLoader("templates"))
index_template = env.get_template("index.html")
election_template = env.get_template("election.html")
manifesto_template = env.get_template("manifesto.html")

elections = list()
election_dirs = os.listdir("manifestos")

def build_path(path):
    return os.path.join("build", path)

def output_dirs(path):
    if "." in os.path.basename(path):
        path = os.path.dirname(path)
    try:
        os.makedirs(path)
        print("Created directory: " + path)
    except OSError:
        # Already exists
        pass

def output_page(path, html):
    output_path = build_path(path)
    output_dirs(output_path)
    with codecs.open(output_path, "w", encoding="utf-8") as file:
        file.write(html)
        print("Wrote file: " + output_path)

def output_file(path, source):
    output_path = build_path(path)
    output_dirs(output_path)
    shutil.copyfile(source, output_path)
    print("Copied file: " + output_path)

def read_manifesto_dir(path):
    manifesto = dict(
        id=os.path.basename(path),
        files=dict()
    )
    files = os.listdir(path)
    file_paths = [os.path.join(path, name) for name in files]
    for fp in file_paths:
        if os.path.basename(fp).startswith("."):
            # ignore hidden files
            continue
        ext = os.path.basename(fp).split(".", 1)[1]
        manifesto["files"][ext] = fp
        if fp.endswith(".yaml"):
            with open(fp, "r") as f:
                manifesto.update(yaml.load(f.read()))           
    return manifesto

def read_election_dir(path):
    election = dict(
        id=os.path.basename(path),
        manifestos=list()
    )
    files = os.listdir(path)
    file_paths = [os.path.join(path, name) for name in files]
    for fp in file_paths:
        if os.path.isdir(fp):
            election["manifestos"].append(read_manifesto_dir(fp))
        elif fp.endswith(".yaml"):
            with open(fp, "r") as f:
                election.update(yaml.load(f.read()))
    return election

def read_all(path):
    elections = list()
    files = os.listdir(path)
    file_paths = [os.path.join(path, name) for name in files]
    for fp in file_paths:
        if os.path.isdir(fp):
            elections.append(read_election_dir(fp))
    return elections

elections = read_all("manifestos")
print(elections)
sorted_elections = sorted(elections, key=itemgetter('date'))
output_page("index.html", index_template.render(elections=sorted_elections))

def output_election_page(election):
    path = "%s/index.html" % election["id"]
    html = election_template.render(election=election)
    output_page(path, html)

def output_manifesto_page(election, manifesto):
    with open(manifesto["files"]["pdf"], "rb") as f:
        page_count = PyPDF2.PdfFileReader(f).getNumPages()
        
    output_dir = election["id"] + "/" + manifesto["id"]

    try:
        with codecs.open(manifesto["files"]["md"], "r", encoding="utf-8") as f:
            md = f.read()
            md_pages = md.split(u'<br class="page-break" />')
            md_html = u''
            page_fmt = u'<div class="page" id="page-{}">\n{}\n</div>'
            i = 1
            for md_page in md_pages:
                md_html += page_fmt.format(i, markdown.markdown(md_page))
                i += 1
    except KeyError:
        md_html="none"
    
    output_page(
        output_dir + "/index.html",
        manifesto_template.render(
            election=election,
            manifesto=manifesto,
            page_count=page_count,
            md_html=md_html
        )
    )
    
    output_file(
        "{}/{}-{}-manifesto.pdf".format(output_dir, election["id"], manifesto["id"]),
        manifesto["files"]["pdf"]
    )
    
    image_dir = build_path(output_dir + "/images")
    output_dirs(image_dir)
    '''
    subprocess.check_call([
        "pdftk",
        manifesto["files"]["pdf"],
        "burst",
        "output",
        "{}/{}-{}-manifesto-page-%d.pdf".format(image_dir, election["id"], manifesto["id"])
    ])
    #os.remove(image_dir + "/doc_data.txt")
    subprocess.check_call([
        "mogrify",
        "-trim",
        "+repage",
        "-background", "white",
        "-alpha", "Remove",
        "+antialias",
        "-density", "300",
        "-format", "png",
        "-resize", "960",
        "--", "{}/{}-{}-manifesto-page-?.pdf".format(image_dir, election["id"], manifesto["id"])
    ])
    '''
    
    
for election in elections:
    output_election_page(election)
    for manifesto in election["manifestos"]:
        output_manifesto_page(election, manifesto)
