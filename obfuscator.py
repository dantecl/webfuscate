#!/usr/bin/env python

import urllib2
import zipfile

sitelist = "http://s3.amazonaws.com/alexa-static/top-1m.csv.zip"
scriptdir = AA

def unziplist {
  with zipfile.ZipFile("file.zip","r") as zip_ref:
     zip_ref.extractall("targetdir")
}

def downloadlist {
file_name = sitelist.split('/')[-1]
u = urllib2.urlopen(sitelist)
f = open(file_name, 'wb')
meta = u.info()
file_size = int(meta.getheaders("Content-Length")[0])
print "Downloading: %s Bytes: %s" % (file_name, file_size)

file_size_dl = 0
block_sz = 8192
while True:
    buffer = u.read(block_sz)
    if not buffer:
        break

    file_size_dl += len(buffer)
    f.write(buffer)
    status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
    status = status + chr(8)*(len(status)+1)
    print status,

f.close()
}

#download our list to the script's folder

