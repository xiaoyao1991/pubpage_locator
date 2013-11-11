import pickle


class FeatureCache(object):
    def __init__(self):
        super(FeatureCache, self).__init__()

        self.visited_urls = {}


    def cache(self, url, raw_html):
        self.visited_urls[url] = raw_html

    def query(self, url):
        if self.visited_urls.has_key(url):
            return self.visited_urls[url]
        else:
            return None

    def serialize(self):
        fp = open('cache.pkl', 'wb')
        pickle.dump(self.visited_urls, fp)
        fp.close()

    def deserialize(self):
        try:
            self.visited_urls = pickle.load(open('cache.pkl', 'rb'))
        except:
            self.visited_urls = {}