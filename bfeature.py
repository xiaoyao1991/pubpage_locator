import urllib2

class BaseFeature(object):
    def __init__(self):
        super(BaseFeature, self).__init__()
        
        self.K = 5  #num of times lname occurs in the page
        self.KEYWORDS = ['publication', 'publications', 'citation', 'citations', 'curriculum vitae', 
                         'selected publications', 'selected works', 'papers and publications']

        self.root_url = None
        self.lname = None

    
    def extract(self, url):
        raise NotImplementedError("Features must implement the extract method.\n")

    def get_raw_html(self, url):
        return urllib2.urlopen(url).read()



