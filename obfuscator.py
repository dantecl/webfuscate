#!/usr/bin/env python

import urllib2
import zipfile
import csv
import os
import fnmatch

sitelist = "http://s3.amazonaws.com/alexa-static/top-1m.csv.zip"
scriptdir = "/tmp/webfuscate/"


def unziplist(srcfile):
    """
    Unzip the list to $scriptdir
    """
    with zipfile.ZipFile(srcfile, "r") as zip_ref:
        zip_ref.extractall(scriptdir)
    return


def find(pattern, path):
    """
    Find a file based on a pattern
    """
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


def downloadlist(ziplink):
    """
    Download our site list
    """
    file_name = scriptdir + ziplink.split('/')[-1]
    u = urllib2.urlopen(ziplink)
    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, file_size)
    fsize_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break
        fsize_dl += len(buffer)
        f.write(buffer)
    status = r"%10d  [%3.2f%%]" % (fsize_dl, fsize_dl * 100. / file_size)
    status = status + chr(8)*(len(status)+1)
    print status,
    f.close()
    return file_name


# download our list to the script's folder
if not os.path.isdir(scriptdir):
    os.mkdir(scriptdir)

dnld = downloadlist(sitelist)
unziplist(dnld)
csvfile = find('*.csv', scriptdir)
full_list = csv.reader(open(csvfile[0]), delimiter=',')
