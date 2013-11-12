class PageStructure(object):
    def __init__(self):
        self.locations = []
        self.location_freq_counter = {}
        self.num_valid_names = 0
        self.tag_counter = {}
        self.sorted_tag_counter = []

    def sort(self):
        for key, value in sorted(self.tag_counter.iteritems(), key=lambda (k,v): (v,k)):
            self.sorted_tag_counter.append((key,value))
