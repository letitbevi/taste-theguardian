#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import json
import requests

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
            path = os.path.join(os.path.abspath(params['q']), params['q']+'_page_'+str(current_page)+'.json')
            with open(path, 'w') as outfile:
                json.dump(response, outfile)
    else: pass

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