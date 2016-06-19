import os
import os.path
import json
from operator import itemgetter

import jinja2
import yaml


env = jinja2.Environment(loader=jinja2.FileSystemLoader("templates"))
index_template = env.get_template("index.html")


elections = list()
election_dirs = os.listdir("manifestos")

def election_yaml_path(election_dir):
    return os.path.join(
        "manifestos",
        election_dir,
        election_dir + "-election.yaml"
    )

for election_dir in election_dirs:
    election = dict(id=election_dir)

    # Read meta data
    with open(election_yaml_path(election_dir), "r") as f:
        election.update(yaml.load(f.read()))

    # Get manifestos
    manifestos = list()
    all_files = os.listdir(os.path.join("manifestos", election_dir))
    manifesto_dirs = [
        d for d in all_files
        if os.path.isdir(os.path.join("manifestos", election_dir, d))
    ]
    for mdir in manifesto_dirs:
        manifesto = dict(id=mdir)
        try:
            with open(os.path.join("manifestos", election_dir, mdir, election_dir + "-" + mdir + "-manifesto.yaml"), "r") as f:
                manifesto.update(yaml.load(f.read()))
        except IOError:
            pass
        manifestos.append(manifesto)
    election["manifestos"] = sorted(manifestos, key=lambda m: m.get("priority", 999))
    elections.append(election)

sorted_elections = sorted(elections, key=itemgetter('date'))
print(sorted_elections)
    
with open(os.path.join("build", "index.html"), "w") as f:
    f.write(index_template.render(elections=sorted_elections))

election_template = env.get_template("election.html")

for election in sorted_elections:
    try:
        os.mkdir(os.path.join("build", election["id"]))
    except OSError:
        # Already exists
        pass
    with open(os.path.join("build", election["id"], "index.html"), "w") as f:
        f.write(election_template.render(election=election))
