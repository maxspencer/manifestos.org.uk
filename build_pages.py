import os
import os.path
import json
import shutil
from operator import itemgetter

import jinja2
import yaml


env = jinja2.Environment(loader=jinja2.FileSystemLoader("templates"))
index_template = env.get_template("index.html")
election_template = env.get_template("election.html")
manifesto_template = env.get_template("manifesto.html")

elections = list()
election_dirs = os.listdir("manifestos")

def output_dirs(path):
    dir = os.path.dirname(path)
    try:
        os.makedirs(dir)
        print("Created directory: " + dir)
    except OSError:
        # Already exists
        pass

def output_page(path, html):
    output_path = os.path.join("build", path)
    output_dirs(output_path)
    with open(output_path, "w") as file:
        file.write(html)
        print("Wrote file: " + output_path)

def output_file(path, source):
    output_path = os.path.join("build", path)
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
    output_page(
        "{}/{}/index.html".format(election["id"], manifesto["id"]),
        manifesto_template.render(election=election, manifesto=manifesto)
    )
    output_file(
        "{e}/{m}/{e}-{m}-manifesto.pdf".format(e=election["id"], m=manifesto["id"]),
        manifesto["files"]["pdf"]
    )

for election in elections:
    output_election_page(election)
    for manifesto in election["manifestos"]:
        output_manifesto_page(election, manifesto)
