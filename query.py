#!/usr/bin/env python2.7 
from StringIO import StringIO
import subprocess
import tempfile
import argparse
import json
import csv
import sys
import os

CLANG_QUERY_CMD = "clang-query -p={db} -f={q} {f}"

def parse_results(r):
    rf = StringIO(r)
    rt = []
    rd = csv.reader(rf)
    for l in rd:
        rt.append((l[0],l[1]))
    return rt

def run_query(query, database, file):
    # Write query out into a named temporary file. 
    nt = tempfile.NamedTemporaryFile(delete=False)
    # This assumes we have a patched clang-query that can output in csv.
    nt.write("set output csv\n")
    nt.write(query)
    nt.write("\n")
    ntnm = nt.name
    nt.close()

    # Run the query.
    c = CLANG_QUERY_CMD.format(db=database, f=file, q=ntnm)
    print c
    r = subprocess.check_output(c, shell=True)
    #os.unlink(ntnm)
    return parse_results(r)

def main(args):
    print json.dumps(run_query(args.query, args.database, args.file))
    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    parser.add_argument("database")
    parser.add_argument("file")
    args = parser.parse_args()
    sys.exit(main(args))
