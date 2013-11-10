import urllib2
import urllib
from bs4 import BeautifulSoup, Comment

def url_cleanup(url):
    parser = urllib2.urlparse.urlparse(url)
    
    modified_path = parser.path
    modified_hostname = parser.hostname

    if modified_hostname is None:
        modified_hostname = ''
    if len(modified_path) == 0:
        modified_path = '/'

    return parser.scheme + '://' + modified_hostname + modified_path

def is_valid_url(url):
    parser = urllib2.urlparse.urlparse(url)
    modified_path = parser.path
    modified_hostname = parser.hostname

    if modified_hostname is None:
        modified_hostname = ''
    if len(modified_path) == 0:
        modified_path = '/'

    url = parser.scheme + '://' + modified_hostname + modified_path

    return len(modified_hostname)>0 and is_url_plain_text(url)

def is_url_plain_text(url):
    try:
        res = urllib2.urlopen(url, timeout=5)
        content_type = res.info().type # 'text/plain'
        main_content_type = res.info().maintype # 'text'
    except:
        return False

    return main_content_type.lower().strip() == 'text'

def get_absolute_url(baseurl, url):     #assume baseurl is absolute
    # print baseurl, '\t', url
    # parser = urllib2.urlparse.urlparse(url)
    # if len(parser.scheme) == 0:     #if no scheme->http, 
    #     url = 'http://' + url
    
    parser = urllib2.urlparse.urlparse(url)
    if parser.hostname is None or len(parser.hostname) == 0:
        return urllib2.urlparse.urljoin(baseurl, url)
    else:
        return url


def under_same_maindomain(url1, url2):
    parser1 = urllib2.urlparse.urlparse(url1)
    parser2 = urllib2.urlparse.urlparse(url2)

    return parser1.hostname == parser2.hostname


def clean_soup(soup):
    soup = soup.find('body')
    for s in soup('script'): # remove script
        s.extract()
    for s in soup('style'): # remove style
        s.extract()
    for s in soup.findAll(text=lambda text:isinstance(text, Comment)): # remove comment tag
        s.extract()

    return soup