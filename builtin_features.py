from bfeature import BaseFeature
from bs4 import BeautifulSoup
from utils import url_cleanup, clean_soup, get_absolute_url
import urllib2, urllib


###############################################################################
##########                  URL based features
###############################################################################

class IsRootURLFeature(BaseFeature):
    def __init__(self,lname,baseurl):
        super(IsRootURLFeature, self).__init__()
        self.lname = lname.lower()
        self.root_url = baseurl

    def extract(self, url_info):
        return int(url_info[2] == 0)


class IsFirstLevelSublinkFeature(BaseFeature):
    def __init__(self,lname,baseurl):
        super(IsFirstLevelSublinkFeature, self).__init__()
        self.lname = lname.lower()
        self.root_url = baseurl

    def extract(self, url_info):
        return int(url_info[2] == 1)


class IsSecondLevelSublinkFeature(BaseFeature):
    def __init__(self,lname,baseurl):
        super(IsSecondLevelSublinkFeature, self).__init__()
        self.lname = lname.lower()
        self.root_url = baseurl

    def extract(self, url_info):
        return int(url_info[2] == 2)


# class IsUnderSameDomainFeature(BaseFeature):
#     def __init__(self,lname,baseurl):
#         super(IsUnderSameDomainFeature, self).__init__()
#         self.lname = lname.lower()
#         self.root_url = baseurl

#     def extract(self, url_info):
#         return int( len(urllib2.urlparse.urlparse(url_info[0]).hostname)==0 or urllib2.urlparse.urlparse(url_info[0]).hostname == urllib2.urlparse.urlparse(self.root_url).hostname)


class URLAnchorTextHasKeywordsFeature(BaseFeature):
    def __init__(self,lname,baseurl):
        super(URLAnchorTextHasKeywordsFeature, self).__init__()
        self.lname = lname.lower()
        self.root_url = baseurl

    def extract(self, url_info):
        for keyword in self.KEYWORDS:
            if keyword in url_info[1].lower():
                return 1
        return 0


class URLHasKeywordsFeature(BaseFeature):
    def __init__(self,lname,baseurl):
        super(URLHasKeywordsFeature, self).__init__()
        self.lname = lname.lower()
        self.root_url = baseurl

    def extract(self, url_info):
        for keyword in self.KEYWORDS:
            if keyword in url_info[0].lower():
                return 1
        return 0


class URLHasLnameFeature(BaseFeature):
    def __init__(self,lname,baseurl):
        super(URLHasLnameFeature, self).__init__()
        self.lname = lname.lower()
        self.root_url = baseurl

    def extract(self, url_info):
        return int(self.lname in url_info[0].lower())


###############################################################################
##########                  Content based features
###############################################################################

class HasKeywordsFeature(BaseFeature):
    def __init__(self,lname,baseurl):
        super(HasKeywordsFeature, self).__init__()
        self.lname = lname.lower()
        self.root_url = baseurl

    def extract(self, url_info):
        raw_html = self.get_raw_html(url_info[0])
        soup = BeautifulSoup(raw_html)
        soup = clean_soup(soup)

        for keyword in self.KEYWORDS:
            keyword_location = soup.find_all(text=keyword)
            if keyword_location:
                return 1
        return 0


class TitleHasKeywordsFeature(BaseFeature):
    def __init__(self,lname,baseurl):
        super(TitleHasKeywordsFeature, self).__init__()
        self.lname = lname.lower()
        self.root_url = baseurl

    def extract(self, url_info):
        raw_html = self.get_raw_html(url_info[0])
        soup = BeautifulSoup(raw_html)
        try:
            title = soup.find('title').text
        except:
            title = ''

        for keyword in self.KEYWORDS:
            if keyword in title:
                return 1
        return 0


class HasLnameMoreThanKTimesFeature(BaseFeature):
    def __init__(self,lname,baseurl):
        super(HasLnameMoreThanKTimesFeature, self).__init__()
        self.lname = lname.lower()
        self.root_url = baseurl

    def extract(self, url_info):
        raw_html = self.get_raw_html(url_info[0])
        soup = BeautifulSoup(raw_html)
        soup = clean_soup(soup)

        lname_location = soup.find_all(text=self.lname)
        return int(len(lname_location) >= self.K)


class HasRecurringPatternFeature(BaseFeature):
    def __init__(self,lname,baseurl):
        super(HasRecurringPatternFeature, self).__init__()
        self.lname = lname.lower()
        self.root_url = baseurl

    def extract(self, url_info):
        raw_html = self.get_raw_html(url_info[0])
        soup = BeautifulSoup(raw_html)
        soup = clean_soup(soup)

        recurring_locations = soup.find_all('li')
        return int(len(recurring_locations) >= self.K)


class HasConsecutivePDFOutlinksFeature(BaseFeature):
    """
        Empirically: if PDF links exceed 5
    """
    def __init__(self,lname,baseurl):
        super(HasConsecutivePDFOutlinksFeature, self).__init__()
        self.lname = lname.lower()
        self.root_url = baseurl

    def extract(self, url_info):
        count_pdf_links = 0
        raw_html = self.get_raw_html(url_info[0])
        soup = BeautifulSoup(raw_html)
        anchor_list = soup.find_all('a', href=True)
        for anchor in anchor_list:
            new_url = get_absolute_url(url_info[0], anchor.attrs['href'])
            print '\t', new_url
            
            try:
                res = urllib2.urlopen(new_url, timeout=5)
                content_type = res.info().type # 'text/plain'
                main_content_type = res.info().maintype # 'text'

                if main_content_type == 'application':
                    count_pdf_links += 1
            except:
                pass

        return int(count_pdf_links >= self.K)


class HasManyBookmarkLinkFeature(BaseFeature):
    """
        Empirically: if bookmark anchor exceed K
    """
    def __init__(self,lname,baseurl):
        super(HasManyBookmarkLinkFeature, self).__init__()
        self.lname = lname.lower()
        self.root_url = baseurl

    def extract(self, url_info):
        count_bookmarks = 0
        raw_html = self.get_raw_html(url_info[0])
        soup = BeautifulSoup(raw_html)
        anchor_list = soup.find_all('a', href=True)
        for anchor in anchor_list:
            if anchor.attrs['href'].startswith('#'):
                count_bookmarks += 1
            else:
                parser = urllib2.urlparse.urlparse(anchor.attrs['href'])
                if parser.hostname == urllib2.urlparse.urlparse(self.root_url).hostname and len(parser.fragment)>0:
                    count_bookmarks += 1
        
        return int(count_bookmarks >= self.K)