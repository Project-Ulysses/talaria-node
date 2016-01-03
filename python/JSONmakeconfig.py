#!/usr/bin/python
import json
import os.path
import shutil
import subprocess
import datetime as dt

jsonfile = "./../config/testconfig.json"
outfile = "ipsec.conf"
backupfile = "ipsec.conf.backup" # "/etc/ipsec.conf.backup"

bash_reload_ipsec = "ipsec reload"

def render_param(key, value):
    return "\t" + key + "=" + value

def render_section(section, parameters):
    section_conf = "conn " + section
    for key, value in parameters.items():
        section_conf += "\n" + render_param(key, value)
    return section_conf

ipsec_conf = "# strongSwan ipsec.conf last updated " + str(dt.datetime.today())


with open(jsonfile, "r") as f:
    # print(f.read())
    config_dict = json.loads(f.read())
    ipsec_dict = config_dict.get("ipsec")
    # render "%default" section of ipsec.conf
    ipsec_conf += "\n\n" + render_section("%default", ipsec_dict.get("default"))
    # render "conn" (connection) section of ipsec.conf
    for conn, params in ipsec_dict.get("connections").items():
        ipsec_conf += "\n\n" + render_section(conn, params)

print(ipsec_conf)

try:
    if os.path.isfile(outfile):
        shutil.copy(outfile, backupfile)
    with open(outfile, "w") as o:
        o.write(ipsec_conf)
except:
    print("Exception: failed to backup " + outfile + " to " + backupfile +
        " and write new configuration to " + outfile)

try:
    subprocess.Popen(bash_reload_ipsec)
except:
    print("\nException: failed to reload ipsec configuration.")
    print("Command: " + bash_reload_ipsec)
