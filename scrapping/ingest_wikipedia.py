import pathlib
import json
import wikipedia


from itertools import chain
from collections import Counter


PROJECT_PATH = pathlib.Path().absolute().parent
KEYWORDS_PATH = PROJECT_PATH / 'data' / 'keywords.json'
WIKIPEDIA_PATH = PROJECT_PATH / 'data' / 'full_wikipedia.json'

NUMBER_OF_NEW_LINKS = 500


def build_dict_from_links(queries, source):
    wiki_data = []
    invalid_queries = []
    for query in queries:
        try:
            wiki_page = wikipedia.page(query)
            wiki_data.append({
                'query': query,
                'title': wiki_page.title,
                'source': source,
                'summary': wiki_page.summary,
                'content': wiki_page.content,
                'links': wiki_page.links
            })
        except:
            invalid_queries.append(query)
    return wiki_data, invalid_queries

def select_links_to_explore(wiki_data, select_number, existing_links):
    existing_links = set(existing_links)

    all_links = chain(*[data['links'] for data in wiki_data])
    valid_links = [
        link
        for link in all_links
        if ('(identifier)' not in link) and (link not in existing_links)
    ]

    valid_links_counter = Counter(valid_links)
    selected_links, _ = zip(*valid_links_counter.most_common(select_number))
    return selected_links


with open(KEYWORDS_PATH, 'r') as file:
    keywords = json.load(file)

wiki_data, invalid_keywords = build_dict_from_links(queries=keywords, source='keywords')


seen_title = [data['title'] for data in wiki_data]
new_links = select_links_to_explore(wiki_data, NUMBER_OF_NEW_LINKS, seen_title)

new_wiki_data, new_invalid_keywords = build_dict_from_links(queries=new_links, source='new_links')

all_data = {
    'valid': list(chain(wiki_data, new_wiki_data)),
    'invalid': list(chain(invalid_keywords, new_invalid_keywords))
}

with open(WIKIPEDIA_PATH, 'w') as outfile:
    json.dump(all_data, outfile)