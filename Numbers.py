from __future__ import print_function
import urllib2

def get_fact(intent_type, number, random=False):
    """gets random or not random fact based on intent type and return a string
    intent_type = 'trivia', 'math', 'date', or 'year'"""
    if random == True:
        number = 'random'
    else:
        number = str(number)
    url = 'http://numbersapi.com/'+number+'/'+intent_type
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    the_page = response.read()
    return the_page
print(get_fact('trivia', None, random=True))
