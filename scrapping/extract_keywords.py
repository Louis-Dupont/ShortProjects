from bs4 import BeautifulSoup
import urllib.request
import json

SOURCE_URL = "https://developers.google.com/machine-learning/glossary"
with urllib.request.urlopen(SOURCE_URL) as fp:
    doc_html = fp.read().decode("utf8")

soup = BeautifulSoup(doc_html, "html.parser")
keywords = [
    h2['data-text'].strip().lower()
    for h2 in soup.find_all(name='h2', attrs={'class': "hide-from-toc"})
]

with open(FILE_PATH, 'w') as outfile:
    json.dump(keywords, outfile)