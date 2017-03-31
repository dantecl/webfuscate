#!/usr/bin/env python

import urllib2
import zipfile

sitelist = "http://s3.amazonaws.com/alexa-static/top-1m.csv.zip"
scriptdir = "/opt/webfuscate"


def unziplist(srcfile):
    with zipfile.ZipFile(srcfile, "r") as zip_ref:
        zip_ref.extractall("targetdir")
    return


def downloadlist(ziplink):
    file_name = ziplink.split('/')[-1]
    u = urllib2.urlopen(ziplink)
    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, file_size)
    fsize_dl = 0
    block_sz = 8192
    while True:
        bfr = u.read(block_sz)
        if not bfr:
            break

    fsize_dl += len(buffer)
    f.write(buffer)
    status = r"%10d  [%3.2f%%]" % (fsize_dl, fsize_dl * 100. / file_size)
    status = status + chr(8)*(len(status)+1)
    print status,
    f.close()

# download our list to the script's folder
downloadlist(sitelist)
