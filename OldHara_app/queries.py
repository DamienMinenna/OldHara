import json
import requests

def query_CrossRef(query):
    crossrefurl = 'https://api.crossref.org/works?query=' + '"' + query + '"'
    r = requests.get(crossrefurl)

    d = json.loads(r.text)
    # numberOfItems = int(d['message']['items-per-page'])

    parsed_items = []
    for item in d['message']['items']:
        temp = {}

        temp['doi'] = item['DOI'].lower()
        
        if 'title' in item:
            temp['title'] = str(item['title'][0])

        if 'issued' in item:
            if 'date-parts' in item['issued']:
                if len(item['issued']['date-parts'][0]) >= 1:
                    temp['date'] = str(item['issued']['date-parts'][0][0])

        if 'container-title' in item: 
            temp['journal'] = str(item['container-title'][0])

        numberauthor = 0
        temp['authors'] = ''
        if 'author' in item: 
            for author_i in item['author']:
                if 'given' in author_i:
                    if 'family' in author_i:
                        temp['authors'] = temp['authors'] + str(author_i['given']) + ' ' + str(author_i['family']) + ', '
                        numberauthor += 1
                
            if numberauthor > 0:
                temp['authors'] = temp['authors'][:-2]

        parsed_items.append(temp)

    return parsed_items

