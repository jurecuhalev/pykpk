###
#
# Library for parsing http://supervizor.kpk-rs.si/
# Author: Jure Cuhalev - firstname @ lastname .com
#
# Released under the MIT License (MIT)

import requests
from urllib import urlencode
import json
from lxml import etree
from lxml.html.soupparser import fromstring
from lxml.cssselect import CSSSelector

URL = 'http://supervizor.kpk-rs.si'

def search(term, search_type='organ'):
    if search_type == 'organ':
        path = '/api/najdi_organ'
    else:
        path = '/api/najdi_prejem'

    params = { 'term': term }

    full_url = URL + path + '?' + urlencode(params)
    data = requests.get(full_url)

    return data.json

def get_organ(organ_id):
    path = '/organ/%s/' % organ_id
    data = requests.get(URL+path)
    
    root = fromstring(data.text)
    content = {}
    # print etree.tostring(root)
    sel = CSSSelector('section.company-info > h1')
    content['company-info'] = sel(root)[0].text

    #TODO - grab everything else
    return content

def get_podj(podj_id):
    pass

def get_organ_podj(organ_id, podj_id):
    path = '/organ/%s/podj/%s/' % (organ_id, podj_id)
    data = requests.get(URL+path)

    root = fromstring(data.text)
    content = { 'sums-trans': [] }

    sel = CSSSelector('#sums-trans tr')
    sel_time = CSSSelector('time')
    sel_sum = CSSSelector('.summonth')
    for row in sel(root):
        time_list = sel_time(row)
        if not time_list:
            continue

        sum_datetime = time_list[0].attrib['datetime']
        sum_month = float(sel_sum(row)[0].attrib['data-monthsum'])

        content['sums-trans'].append({'datetime': sum_datetime, 'amount': sum_month})

    return content

if __name__ == '__main__':
    # print search('EPK')
    # print get_organ(38580)
    print get_organ_podj(38580, 56329245)