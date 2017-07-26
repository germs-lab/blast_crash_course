#!/usr/bin/python

import urllib2
import os
import sys
import time
import errno

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

if len(sys.argv) != 3:
    print "USAGE: fetch-genomes.py <genome_id_list> <out_dir>"
    sys.exit(1)

url_template = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nucleotide&id=%s&rettype=fasta&retmode=text"

mkdir_p(sys.argv[2])

for id in open(sys.argv[1]):
    id = id.strip()
    if id == "":
        continue

    sys.stdout.write("Fetching %s..." % id)
    sys.stdout.flush()
    gbk_out_file = os.path.join(sys.argv[2], id + ".gbk")
    if os.path.exists(gbk_out_file):
        print "already fetched"

    open(gbk_out_file, "w").write(urllib2.urlopen(url_template % id).read())
    print "Done"
    time.sleep(1.0/3)

