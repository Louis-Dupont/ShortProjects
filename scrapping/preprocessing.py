import pathlib
import json
from collections import Counter

from nltk import word_tokenize

PROJECT_PATH = pathlib.Path().absolute().parent
WIKIPEDIA_PATH = PROJECT_PATH / 'data' / 'full_wikipedia.json'
CLEANED_WIKIPEDIA_PATH = PROJECT_PATH / 'data' / 'cleaned_wikipedia.json'

def counter_subset(counter, subset):
    return Counter({ele: counter[ele] for ele in subset if ele in counter})

with open(WIKIPEDIA_PATH, 'r') as file:
    wiki_data = json.load(file)['valid']

bad_titles = {'A', 'L'}
wiki_data = [data for data in wiki_data if data['title'] not in bad_titles]

titles = {data['title'] for data in wiki_data}

cleaned_data = []
seen_title = []
for data in wiki_data:
    if data['title'] not in seen_title:
        seen_title.append(data['title'])
        cleaned_data.append({
            **data,
            'useful_content': dict(counter_subset(Counter(word_tokenize(data['content'])), titles)),
            'useful_links': list(set(data['links']) & titles)
        })

with open(CLEANED_WIKIPEDIA_PATH, 'w') as file:
    json.dump(cleaned_data, file)
