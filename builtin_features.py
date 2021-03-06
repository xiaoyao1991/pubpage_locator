from bfeature import BaseFeature
from bs4 import BeautifulSoup
from utils import url_cleanup, clean_soup, get_absolute_url, count_occurence
import urllib2, urllib


###############################################################################
##########                  URL based features
###############################################################################

class IsRootURLFeature(BaseFeature):
    def __init__(self,lname,baseurl, feature_cache):
        super(IsRootURLFeature, self).__init__()
        self.lname = lname.lower()
        self.root_url = baseurl
        self.feature_cache = feature_cache

    def extract(self, url_info, svm_feature=False):
        return int(url_info[2] == 0)


class IsFirstLevelSublinkFeature(BaseFeature):
    def __init__(self,lname,baseurl, feature_cache):
        super(IsFirstLevelSublinkFeature, self).__init__()
        self.lname = lname.lower()
        self.root_url = baseurl
        self.feature_cache = feature_cache

    def extract(self, url_info, svm_feature=False):
        return int(url_info[2] == 1)


class IsSecondLevelSublinkFeature(BaseFeature):
    def __init__(self,lname,baseurl, feature_cache):
        super(IsSecondLevelSublinkFeature, self).__init__()
        self.lname = lname.lower()
        self.root_url = baseurl
        self.feature_cache = feature_cache

    def extract(self, url_info, svm_feature=False):
        return int(url_info[2] == 2)


# class IsUnderSameDomainFeature(BaseFeature):
#     def __init__(self,lname,baseurl, feature_cache):
#         super(IsUnderSameDomainFeature, self).__init__()
#         self.lname = lname.lower()
#         self.root_url = baseurl
#         self.feature_cache = feature_cache

#     def extract(self, url_info, svm_feature=False):
#         return int( len(urllib2.urlparse.urlparse(url_info[0]).hostname)==0 or urllib2.urlparse.urlparse(url_info[0]).hostname == urllib2.urlparse.urlparse(self.root_url).hostname)


class URLAnchorTextHasKeywordsFeature(BaseFeature):
    def __init__(self,lname,baseurl, feature_cache):
        super(URLAnchorTextHasKeywordsFeature, self).__init__()
        self.lname = lname.lower()
        self.root_url = baseurl
        self.feature_cache = feature_cache

    def extract(self, url_info, svm_feature=False):
        if svm_feature:
            counter = 0
            for keyword in self.KEYWORDS:
                counter += count_occurence(keyword, url_info[1])
            return counter

        for keyword in self.KEYWORDS:
            if keyword in url_info[1].lower():
                return 1
        return 0


class URLHasKeywordsFeature(BaseFeature):
    def __init__(self,lname,baseurl, feature_cache):
        super(URLHasKeywordsFeature, self).__init__()
        self.lname = lname.lower()
        self.root_url = baseurl
        self.feature_cache = feature_cache

    def extract(self, url_info, svm_feature=False):
        for keyword in self.KEYWORDS:
            if keyword in url_info[0].lower():
                return 1
        return 0


class URLHasLnameFeature(BaseFeature):
    def __init__(self,lname,baseurl, feature_cache):
        super(URLHasLnameFeature, self).__init__()
        self.lname = lname.lower()
        self.root_url = baseurl
        self.feature_cache = feature_cache

    def extract(self, url_info, svm_feature=False):
        return int(self.lname in url_info[0].lower())


###############################################################################
##########                  Content based features
###############################################################################

class HasKeywordsFeature(BaseFeature):
    def __init__(self,lname,baseurl, feature_cache):
        super(HasKeywordsFeature, self).__init__()
        self.lname = lname.lower()
        self.root_url = baseurl
        self.feature_cache = feature_cache

    def extract(self, url_info, svm_feature=False):
        raw_html = self.feature_cache.query(url_info[0])    #
        if raw_html is None:
            raw_html = self.get_raw_html(url_info[0])
            self.feature_cache.cache(url_info[0], raw_html)

        soup = BeautifulSoup(raw_html)
        soup = clean_soup(soup)

        for keyword in self.KEYWORDS:
            try:
                keyword_location = soup.find_all(text=keyword)
                if svm_feature:
                    return len(keyword_location)
                if keyword_location:
                    return 1
            except:
                pass
        return 0


class TitleHasKeywordsFeature(BaseFeature):
    def __init__(self,lname,baseurl, feature_cache):
        super(TitleHasKeywordsFeature, self).__init__()
        self.lname = lname.lower()
        self.root_url = baseurl
        self.feature_cache = feature_cache

    def extract(self, url_info, svm_feature=False):
        raw_html = self.feature_cache.query(url_info[0])    #
        if raw_html is None:
            raw_html = self.get_raw_html(url_info[0])
            self.feature_cache.cache(url_info[0], raw_html)

        soup = BeautifulSoup(raw_html)
        try:
            title = soup.find('title').text
        except:
            title = ''

        if svm_feature:
            counter = 0
            for keyword in self.KEYWORDS:
                counter += count_occurence(keyword, title)
            return counter

        for keyword in self.KEYWORDS:
            if keyword in title:
                return 1
        return 0


class HasLnameMoreThanKTimesFeature(BaseFeature):
    def __init__(self,lname,baseurl, feature_cache):
        super(HasLnameMoreThanKTimesFeature, self).__init__()
        self.lname = lname.lower()
        self.root_url = baseurl
        self.feature_cache = feature_cache

    def extract(self, url_info, svm_feature=False):
        raw_html = self.feature_cache.query(url_info[0])    #
        if raw_html is None:
            raw_html = self.get_raw_html(url_info[0])
            self.feature_cache.cache(url_info[0], raw_html)
            
        soup = BeautifulSoup(raw_html)
        soup = clean_soup(soup)
        try:
            lname_location = soup.find_all(text=self.lname)
        except:
            lname_location = []

        if svm_feature:
            return len(lname_location)
        return int(len(lname_location) >= self.K)


class HasRecurringPatternFeature(BaseFeature):
    def __init__(self,lname,baseurl, feature_cache):
        super(HasRecurringPatternFeature, self).__init__()
        self.lname = lname.lower()
        self.root_url = baseurl
        self.feature_cache = feature_cache

    def extract(self, url_info, svm_feature=False):
        raw_html = self.feature_cache.query(url_info[0])    #
        if raw_html is None:
            raw_html = self.get_raw_html(url_info[0])
            self.feature_cache.cache(url_info[0], raw_html)
            
        soup = BeautifulSoup(raw_html)
        soup = clean_soup(soup)

        try:
            recurring_locations = soup.find_all('li')
        except:
            recurring_locations = []

        if svm_feature:
            return len(recurring_locations)
        return int(len(recurring_locations) >= self.K)


class HasDetectedPublications(BaseFeature):
    def __init__(self,lname,baseurl, feature_cache):
        super(HasDetectedPublications, self).__init__()
        self.lname = lname.lower()
        self.root_url = baseurl
        self.feature_cache = feature_cache

    def extract(self, url_info, svm_feature=False):
        raw_html = self.feature_cache.query(url_info[0])    #
        if raw_html is None:
            raw_html = self.get_raw_html(url_info[0])
            self.feature_cache.cache(url_info[0], raw_html)
        
        from crawler_with_style import PublicationExtractor
        try:
            p = PublicationExtractor()
            publication_candidates = p.locate_records(url_info[0], self.lname, raw_html)
        except:
            publication_candidates = []

        if svm_feature:
            return len(publication_candidates)
        return int(len(publication_candidates) >= self.K)


class HasConsecutivePDFOutlinksFeature(BaseFeature):
    """
        Empirically: if PDF links exceed 5
    """
    def __init__(self,lname,baseurl, feature_cache):
        super(HasConsecutivePDFOutlinksFeature, self).__init__()
        self.lname = lname.lower()
        self.root_url = baseurl
        self.feature_cache = feature_cache

    def extract(self, url_info, svm_feature=False):
        count_pdf_links = 0
        raw_html = self.feature_cache.query(url_info[0])    #
        if raw_html is None:
            raw_html = self.get_raw_html(url_info[0])
            self.feature_cache.cache(url_info[0], raw_html)
            
        soup = BeautifulSoup(raw_html)

        try:
            anchor_list = soup.find_all('a', href=True)
        except:
            anchor_list = []

        for anchor in anchor_list:
            new_url = get_absolute_url(url_info[0], anchor.attrs['href'])

            try:
                print '\t', new_url
                res = urllib2.urlopen(new_url, timeout=3)
                content_type = res.info().type # 'text/plain'
                main_content_type = res.info().maintype # 'text'

                if main_content_type == 'application':
                    count_pdf_links += 1
            except:
                pass

        if svm_feature:
            return count_pdf_links
        return int(count_pdf_links >= self.K)


class HasManyBookmarkLinkFeature(BaseFeature):
    """
        Empirically: if bookmark anchor exceed K
    """
    def __init__(self,lname,baseurl, feature_cache):
        super(HasManyBookmarkLinkFeature, self).__init__()
        self.lname = lname.lower()
        self.root_url = baseurl
        self.feature_cache = feature_cache

    def extract(self, url_info, svm_feature=False):
        count_bookmarks = 0
        raw_html = self.feature_cache.query(url_info[0])    #
        if raw_html is None:
            raw_html = self.get_raw_html(url_info[0])
            self.feature_cache.cache(url_info[0], raw_html)
            
        soup = BeautifulSoup(raw_html)
        
        try:
            anchor_list = soup.find_all('a', href=True)
        except:
            anchor_list = []

        for anchor in anchor_list:
            if anchor.attrs['href'].startswith('#'):
                count_bookmarks += 1
            else:
                parser = urllib2.urlparse.urlparse(anchor.attrs['href'])
                if parser.hostname == urllib2.urlparse.urlparse(self.root_url).hostname and len(parser.fragment)>0:
                    count_bookmarks += 1
        
        if svm_feature:
            return count_bookmarks
        return int(count_bookmarks >= self.K)