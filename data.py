from utils import url_cleanup

class Data(object):
    def __init__(self, lname, baseurl, targeturl):
        super(Data, self).__init__()
        self.lname = lname.lower().strip()
        self.root_url = url_cleanup(baseurl)
        self.target_url = url_cleanup(targeturl)
        
    def __repr__(self):
        return '<%s, %s, %s>' % (self.lname, self.root_url, self.target_url)