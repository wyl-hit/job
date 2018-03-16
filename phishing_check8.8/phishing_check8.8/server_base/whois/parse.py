#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import sys
import re
import pythonwhois

def get_whois(url):
    whois_dict = { 'status':'OK' }
    try:
        whois_raw = pythonwhois.get_whois(url)
    except pythonwhois.shared.WhoisException, e:
        whois_dict['status'] = 'Error: %s' % str(e)
    except Exception, e:
        whois_dict['status'] = 'Error: %s' % str(e)

    if whois_dict['status'].startswith('Error:'):
        return whois_dict

    # Get Information, then deal with for our need 
    whois_dict['domain'] = {}
    whois_dict['contacts'] = {}
    whois_dict['domain']['name'] = url

    # Get domain information
    if 'id' in whois_raw.keys():
        whois_dict['domain']['id'] = whois_raw['id'][-1]
    else:
        whois_dict['domain']['id'] = ''

    domain = ['creation_date', 'expiration_date', 'updated_date']
    for key in domain:
        if key in whois_raw.keys():
            whois_dict['domain'][key] = whois_raw[key][-1]
        else:
            whois_dict['domain'][key] = '0000-00-00'

    
    # if domain id is empty, no such registar url
    #if whois_dict['domain']['id'] == '':
    #    whois_dict['status'] = 'ERROR: No such record'
    #    return whois_dict

    # Get contacts information
    contacts = ['admin', 'tech', 'registrant']
    contacts_details = ['name', 'email', 'phone', 'fax', 'country', 'city',
            'street', 'organization', 'postalcode']
    for key in contacts:
        whois_dict['contacts'][key] = whois_raw['contacts'][key]
        if whois_dict['contacts'][key] is not None:
            for item in contacts_details:
                if item not in whois_dict['contacts'][key].keys():
                    whois_dict['contacts'][key][item] = ''
        
            # the attribute of name and email cannot be empty
            #if empty, delete the item
            if whois_dict['contacts'][key]['name'] == '' or \
               whois_dict['contacts'][key]['email'] == '':
                whois_dict['contacts'][key] = None

    if 'whois_server' in whois_raw.keys():
        whois_dict['whois_server'] = whois_raw['whois_server'][-1]
    else:
        whois_dict['whois_server'] = '' 

    return whois_dict


if __name__ == '__main__':
    import urlparse
    if len(sys.argv) == 1:
        url = 'www.baidu.com'
    else:
        url = sys.argv[1]
   
    # preprocess url get url's network location 
    if not url.startswith('http'):
        url = 'http://' + url.strip()
    url = urlparse.urlparse(url)[1]
    if url.startswith('www.'):
        url = url[4:]

    whois_dict = get_whois(url)  
    print whois_dict
    args=whois_dict['domain']
    print args['id'], args['name']

