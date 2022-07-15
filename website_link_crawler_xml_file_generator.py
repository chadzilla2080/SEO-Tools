from github import Github
import xml
import urllib.parse
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
import time
from datetime import datetime

source_code = requests.get('https://naturalgear.com')
soup = BeautifulSoup(source_code.content, 'lxml')
data = []
links = []


def remove_duplicates(soup):  # remove duplicates and unURL string
    for item in soup:
        match = re.search("(?P<url>https?://[^\s]+)", item)
        if match is not None:
            links.append((match.group("url")))


for link in soup.find_all('a', href=True):
    data.append(str(link.get('href')))
flag = True
remove_duplicates(data)

# Debug Feature, Just Print It Out, See If It Works As Expected
print(data)

while flag:
    try:
        for link in links:
            for j in soup.find_all('a', href=True):
                temp = []
                source_code = requests.get(link)
                soup = BeautifulSoup(source_code.content, 'lxml')
                temp.append(str(j.get('href')))
                remove_duplicates(temp)

                if len(links) > 162:  # set limitation to number of URLs
                    break
            if len(links) > 162:
                break
        if len(links) > 162:
            break
    except Exception as e:
        print(e)
        if len(links) > 162:
            break

for url in links:
    # For Debug Only
    print(links)

# Debug Feature

ls = links
print(ls)

# Import List of URLs - Via a File - Just Uncomment
# list_of_urls = pd.read_csv('list_of_urls.csv')
# list_of_urls

# Or . . . From a Flat File
# with open('list_of_urls.txt','r') as f:
#    list_of_urls = f.read()
#    list_of_urls = list_of_urls.split('\n')

# To String

list_of_urls = "\n".join(ls)

# Debug Feature, Test It Again
print(list_of_urls)

# Convert Back To List
list_of_urls = list_of_urls.split('\n')

# Inspect One Final time
print(list_of_urls)


df = pd.DataFrame(list_of_urls, columns=['urls'])

df["loc"] = df.apply(lambda x: list_of_urls, axis=1)
df["lastmod"] = now.strftime("%Y-%m-%d")
df["changefreq"] = "monthly"
df["priority"] = 0.6

# Inspect DataFrame, Will Need To Write Another Line of Code To Drop Of The Loc column
display(df)

# Finish from here, you'll need to assign a DataFrame and then Export to XML File
df_final = ''

# Follow this to get the Pandas Data Frame Set Correclty  - - -  Website:: https://pythontic.com/pandas/serialization/to_xml
#
#
#
#
#
#

# Last Step To a Github Repo that can merge with any code base, generate the xml file, if the code does not have support or a library for XML generation

# using an access token
g = Github("XXXXXXXX")
repo = g.get_repo("")
with open('sitemap.xml', 'r') as file:
    content = file.read()

contents = repo.get_contents("public/sitemap.xml")
repo.update_file("public/sitemap.xml", "update sitemap",
                 content, contents.sha, branch="main")
