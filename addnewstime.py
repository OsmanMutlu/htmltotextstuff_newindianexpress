import sys
import codecs
import re
import lxml.html
import shutil
#from fuzzywuzzy import fuzz

filename = sys.argv[1]

text_path = re.sub(r"(.*\/)[^\/]*$", r"\g<1>", filename)

try:
    with codecs.open(filename, "r", "utf-8") as f:
        lines = f.readlines()
except FileNotFoundError:
    ofilename = re.sub(r".*\/([^\/]*)$", r"\g<1>", filename)
    print("FILE IS EMPTY!!! : " + ofilename)
    with open(text_path + "empty_files","a") as g:
        g.write(ofilename + "\n")
    shutil.move(filename, text_path + "empties/" + ofilename)
    sys.exit()

hfilename = re.sub(r".*\/([^\/]*)$", r"\g<1>", filename)

with codecs.open(hfilename, "rb", "utf-8") as g:
    html_file = g.read()

doc = lxml.html.document_fromstring(html_file)
title = doc.xpath("//h1[@class='ArticleHead']/text()")
time = doc.xpath("//p[@class='ArticlePublish' and position()=1]/span/text()")

if not time:
    time = doc.xpath("//input[@class='article_created_on']/@value")

if not title:
    title = doc.xpath("//meta[@name='title']/@content")

if not title:
    title = doc.xpath("//title/text()")

"""
soup = BeautifulSoup(html, 'html.parser')
title = soup.find("h1", class_="heading1")
time = soup.find("span", class_="time_cptn")

if not title:
    title = soup.find("title")
"""
if title and time:
    title = re.sub(r"\n|\r", r"", str(title[0]))
    time = re.sub(r"\n|\r", r"", str(time[-1]))
#    if not any(fuzz.ratio(title,line)>70 for line in lines):
    lines.insert(0,time)
    lines.insert(0,title)
else:
    with codecs.open(text_path + "no_title_or_time", "a", "utf-8") as h:
        h.write(re.sub(r".*\/([^\/]*)$", r"\g<1>", filename))

with codecs.open(filename, "w", "utf-8") as f:
    for line in lines:
        if line:
            line = re.sub(r"\n|\r", r"", line)
            f.write(line + "\n")
