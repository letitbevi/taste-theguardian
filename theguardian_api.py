#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import re
import json
import requests
import nltk

def request_theguardian(params):

    ### theguardian endpoint URL
    r = requests.get('http://content.guardianapis.com/search', params=params)
    response = json.loads(r.text)

    ### pagination rules
    if response['response']['pages'] > 1:
        for current_page in range(1, response['response']['pages']+1):
            params['page'] = current_page
            r = requests.get('http://content.guardianapis.com/search', params=params)
            response = json.loads(r.text)

            ### --DO SOMETHIMG HERE--

            ### Example 1: collect sentences from each article that contain 'Amsterdam'
            articles = collect_sents(response, 'Amsterdam')
            [[print (sent+'\n') for sent in article] for article in articles]
            
            ### Example 2: dump a response as json file 
            dump_json(params['q'], current_page, response)

            ### --DO SOMETHING HERE--

    else: pass

def dump_json(query, current_page, response):
    if not os.path.exists(query):
        os.makedirs(query)
    else: pass
    path = os.path.join(os.path.abspath(query), query+'_page_'+str(current_page)+'.json')
    with open(path, 'w') as f:
        json.dump(response, f)
 
def collect_sents(response, keyword):
    raw_articles = [re.sub('<[^>]*>', '', article['fields']['body']) for article in response['response']['results']] 
    sent_tokenized_articles = [nltk.sent_tokenize(i) for i in raw_articles]
    keyword_sentences = [[sent for sent in article if keyword in sent]for article in sent_tokenized_articles]
    return keyword_sentences

def main():
    params = {
        'api-key': 'aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee', ### your api-key        
        'q': 'Amsterdam',
        'show-tags': 'keyword',
        'show-fields': 'body', 
        'from-date': '2012-01-01', 
        'to-date': '2016-12-31',
        'page-size': '200' ### max pagesize is 200
    }
    request_theguardian(params)

if __name__ == '__main__':
    main()
