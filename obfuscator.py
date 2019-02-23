#!/usr/bin/env python

import urllib2
import zipfile
import csv
import os
import fnmatch
from selenium import webdriver
import time
import random

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
    print("Downloading: %s Bytes: %s") % (file_name, file_size)
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
    print(status)
    f.close()
    return file_name


def browselink(link):
    """
    Browse the provided link and click something at random inside
    :param link: a web link
    :return:
    """
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1420,1080')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(link)
    links = driver.find_elements_by_partial_link_text('')
    l = links[random.randint(0, len(links)-1)]
    l.click()
    print(driver.current_url)


# download our list to the script's folder
if not os.path.isdir(scriptdir):
    os.mkdir(scriptdir)

while True:
    dnld = downloadlist(sitelist)
    unziplist(dnld)
    csvfile = find('*.csv', scriptdir)
    full_list = csv.reader(open(csvfile[0]), delimiter=',')
    chosen_url = random.choice(list(full_list))
    print(chosen_url)
    browselink("http://" + chosen_url[1])
    time.sleep(random.randint(5,60))