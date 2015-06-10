#!/usr/bin/env python3
import json, re, sys
from urllib import parse, request
import psycopg2

REGEX_GIT_SITE = re.compile("^(github.com|bitbucket.org)$", re.I)
DOAP_URL = "https://pypi.python.org/pypi?:action=doap&name=%s&version=%s"
doap_urls = {}

try:
    conn = psycopg2.connect(host="public-udd-mirror.xvm.mit.edu", database="udd", 
    user="public-udd-mirror", password="public-udd-mirror")
    cursor = conn.cursor()
    cursor.execute("SELECT source, upstream_url FROM upstream WHERE upstream_url IS NOT NULL")
except Exception as e:
    sys.stderr.write("failed to get data from database;\n%s\n" % e)
    sys.exit(1)

packages = {}
for name, url in cursor.fetchall():
    parsed = parse.urlparse(url)
    if parsed.hostname:
        match = re.search(REGEX_GIT_SITE, parsed.hostname)
        if match:
            username, package, _ = parsed.path[1:].split("/", 2)
            site = match.group(1)
            packages[name] = [site, username, package]

packages_json = json.dumps(packages, sort_keys=True, indent=4)
sys.stdout.write(packages_json)