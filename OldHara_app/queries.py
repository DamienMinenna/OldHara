import json
import requests

def query_CrossRef(query):
    crossrefurl = 'https://api.crossref.org/works?query=' + '"' + query + '"'
    crossrefrequest = requests.get(crossrefurl)

    parsed_items = []

    if crossrefrequest.status_code == 200:

        d = json.loads(crossrefrequest.text)
        # numberOfItems = int(d['message']['items-per-page'])
        
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

        manual_search_isNotValid = False
    
    else:
        manual_search_isNotValid = True

    return parsed_items, manual_search_isNotValid

