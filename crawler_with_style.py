"""
	Crawl with style when extracting data from html:
	1. CSS must be corresponding to a specific HTML element, so we only need to differentiate different html elements
	2. Data output should be of format:
		{
		  	
		}
    3. Keep the original raw_htmls, so that the 'style' will be essentially observed. 

"""


from bs4 import BeautifulSoup, Comment
from page_structure import PageStructure
from urlparse import urljoin
import urllib2
import re
import ast
import sys
import math
import sys
import os
import datetime

TAG_REGEX = re.compile('<\w+>', re.IGNORECASE)
PUNCTUATION_REGEX = re.compile('[^a-zA-Z\s0-9]')
YEAR_REGEX1 = re.compile('(?<=\,|\.|\s|\(|\[|\;|\/)[1|2]\d{3}(?=\,|\.|\s|\)|\[|\;|\/)')
YEAR_REGEX2 = re.compile('(?<=\,|\.|\s|\(|\[|\;|\/)[1|2]\d{3}$', re.MULTILINE)
YEAR_REGEX3 = re.compile('^[1|2]\d{3}(?=\,|\.|\s|\)|\[|\;|\/)', re.MULTILINE)
TMP_DOWNLOAD = 'extractors/PDFs'

def extract_year(title, pdf_link=False):  #empirical function
    year_upperbound = datetime.datetime.now().year
    years1 = YEAR_REGEX1.findall(title)
    years2 = YEAR_REGEX2.findall(title)
    years3 = YEAR_REGEX3.findall(title)

    #sort the years and pick the largest possible year
    years = sorted([int(y) for y in years1] + [int(y) for y in years2] + [int(y) for y in years3], reverse=True)
    for year in years:
        if year <= year_upperbound and year >= 1980:
            return year
    
    # if pdf_link:
    #     try:
    #         # download pdf
    #         full_pdf_path = '%s/tmp.pdf' % TMP_DOWNLOAD
    #         temp = urllib2.urlopen(pdf_link)
    #         output = open(full_pdf_path, 'wb')
    #         output.write(temp.read())
    #         output.close()

    #         # analyze year
    #         metadata = PDFHelper().get_metadata(pdf_link)
    #         if "ModDate" in metadata:
    #             year = metadata["ModDate"]
    #         elif "CreationDate" in metadata:
    #             year = metadata["CreationDate"]
    #         if year:
    #             dates = re.findall('[1|2]\d{3}', year)
    #             if len(dates) > 0:
    #                 date = int(dates[0])
    #                 if date >= 1980 and date <= year_upperbound:
    #                     return date                        
    #     except:
    #         print 'ERROR: EXTRACTING YEAR FROM PDF'
    #         exc_type, exc_obj, exc_tb = sys.exc_info()
    #         fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #         print(exc_type, fname, exc_tb.tb_lineno)

    return None


class PublicationExtractor(object):
    def __init__(self):
        self.error = ''

        self.real_records = []
        self.br_case = False
        self.pubpage = ''
        self.lname = ''
        self.base_url = ''
        self.soup = None
        self.page_structure = None
        self.seed_regex = None


    def locate_records(self, pubpage, lname, cached_html=None):
        """ 
            Given lastname as seed and the pubpage, extract publication records
            
            Input: seed lastname, pubpage(url),
            Output: a list of publication records (may contain false positives).  Each record is a plain string.  
            URLs will not be preserved because many URLs tend to be relative path and so, 
            would cause grant forward to have too many broken links. We can also search google or bing to get the pdf some other way. 
        """

        try:
            # Initial config
            self.pubpage = pubpage
            self.lname = lname
            self.br_case = False
            self.page_structure = PageStructure()

            regex_str = '[^a-zA-Z]%s(?!\w|@)|\s+%s(?!\w|@)|^%s(?!\w|@)' % (lname,lname,lname)
            self.seed_regex = re.compile(regex_str, re.IGNORECASE)

            if cached_html:
                self.soup = BeautifulSoup(cached_html)
            else:
                self.soup = BeautifulSoup(urllib2.urlopen(pubpage, timeout=3).read())

            self.set_base_url()
            self.clean_soup()

            self.locate_seeds()
            self.detect_special_case()
            self.find_majority_tag()
            self.page_structure.sort()

            if self.br_case:
                self.handle_br_case()

            else:
                self.handle_normal_case()
            
        except Exception, e:
            self.error = '%s\nEXTRACTOR-PUBLICATION RECORD: LOCATE RECORDS ERROR %s' % (self.error, e)
            print 'LOCATE RECORDS ERROR ', e
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
        return self.real_records


    def set_base_url(self):
        base_tag = self.soup.find('base')
        if base_tag:
            try:
                self.base_url = base_tag.attrs['href']
            except:
                self.base_url = self.pubpage
        else:
            self.base_url = self.pubpage
    
    def clean_soup(self):
        self.soup = self.soup.find('body')
        for s in self.soup('script'): # remove script
            s.extract()
        for s in self.soup('style'): # remove style
            s.extract()
        for s in self.soup.findAll(text=lambda text:isinstance(text, Comment)): # remove comment tag
            s.extract()

    def locate_seeds(self):
        tmp_locations = self.soup.findAll(text=self.seed_regex) # locate where the seed lname is
        for tmp_location in tmp_locations:
            key = str(tmp_location.parent)
            if self.page_structure.location_freq_counter.has_key(key):
                old_value = self.page_structure.location_freq_counter[key]
                new_value = (old_value[0], old_value[1]+1)
                self.page_structure.location_freq_counter[key] = new_value
            else:
                new_value = (tmp_location.parent, 1)
                self.page_structure.location_freq_counter[key] = new_value
            self.page_structure.locations.append(tmp_location.parent)
            self.page_structure.num_valid_names += 1

    def detect_special_case(self):
        ###############################################################################
        ### Check the location_freq_counter to DETECT the special case pattern
        ### NOTE: Very empirical, detected by counting how many names in a parent 
        ### tag
        ###############################################################################
        for k,v in self.page_structure.location_freq_counter.iteritems():
            tag_name = v[0].name
            tag_attr = v[0].attrs

            detection_list = self.soup.findAll(tag_name, tag_attr)
            for item in detection_list:
                if len(self.seed_regex.findall(item.text.lower())) > 5:  # empirical, any parent contains more than 5 times of self.seed_regex
                    self.br_case = True
                    print 'Suspicious Special Case Detected!'

    def find_majority_tag(self):
        ############################################################################### 
        ### Check the majority of tags and their attr. If attrs not exist for most of 
        ### them. Then compare tags. This step is significant to find the smallest tag 
        ### that contains the lastname, and remove other insignificant tags
        ###############################################################################
        self.page_structure.tag_counter = {}
        for location in self.page_structure.locations:
            key = str(location.name) + str(location.attrs)
            if self.page_structure.tag_counter.has_key(key):
                self.page_structure.tag_counter[key] += 1
            else:
                self.page_structure.tag_counter[key] = 1


    def handle_br_case(self):
        ###############################################################################
        ### Handle br case
        ### Assume br only appears in a parent, either be p or div. We need to
        ### find this p or div
        ### ???? temporarily don't support pdf link extraction
        ###############################################################################
        tag_attr_pair = self.page_structure.sorted_tag_counter[-1][0].split('{')    #???? -1
        target_tag = tag_attr_pair[0]   # not for second round selecting, but for eliminating noise tags from location_freq_counter
        target_attr = ast.literal_eval('{' + tag_attr_pair[1])

        target_containers = []

        for k,v in self.page_structure.location_freq_counter.iteritems():
            tag = v[0]
            if tag.name == target_tag and tag.attrs == target_attr:
                target_containers.append(tag)

        for container in target_containers:
            content = ""
            if container.name in ["li", "p", "div", "ol", "ul", "br", "tr", "td", "table"]:
                content += "\n\n\n\n"
            for child in container.recursiveChildGenerator():
                if isinstance(child, basestring):
                    childtext = child.strip()
                    # print 1
                    if (len(childtext) > len(self.lname) or len(PUNCTUATION_REGEX.findall(childtext))>0 ): #and content not in childtext and childtext not in content:
                        # print 11
                        content += " %s" % childtext
                
                elif child.name in ["li", "p", "div", "ol", "ul", "tr", "td", "table"]:
                    # print 2
                    content += '\n\n\n\n'
                elif child.name in ['br']:
                    # print 3
                    content += '\nbrbr\n'
                elif child.text:
                    # print 4
                    childtext = child.text.strip()
                    if (len(childtext) > len(self.lname) or len(PUNCTUATION_REGEX.findall(childtext))>0 ):# and content not in childtext and childtext not in content:
                        # print 44
                        content += " %s" % child.text
            try:
                content = content.encode('ascii', 'ignore')
            except Exception, e:
                print e
            # print content

            # postprocessing to get the formatted pub records        
            tmp_new_real_records = []
            new_real_record = ''
            records = content.split("\nbrbr\n")
            for i in range(0, len(records)):
                record = records[i].strip()
                try:                    
                    record = record.encode("ascii", "ignore")
                except Exception, e:
                    print "ERROR ", e, record                
                record = ' '.join(record.split())
                if record not in self.real_records and len(record.split()) > 5 and len(record.split()) < 200:
                    year = extract_year(record, '')
                    self.real_records.append({'record':record, 'pdf_link':'', 'year':year})
                elif len(record)>0:
                    print '!!!!!!!!!!!!!!!!!!!!!!!' + record

        # Test output
        for i in range(len(self.real_records)):
            print str(i) + '>>>>' + str(self.real_records[i])


    def handle_normal_case(self):
        ###############################################################################
        ### Normal case
        ### Select the tags and attrs again. Do some verification on it: 
        ### 1. Must contain lastname
        ### 2. Length must be correct ????
        ### 3. What about tags with empty attrs ????
        ### 4. What about <br> linebreak    ???? they will be counted as a same tag
        ###############################################################################
        
        # Parse the tag and attr
        print self.page_structure.sorted_tag_counter
        tag_attr_pair = self.page_structure.sorted_tag_counter[-1][0].split('{')
        tag = tag_attr_pair[0]
        attr = ast.literal_eval('{' + tag_attr_pair[1])

        if tag.lower() == 'body':   # In case of those undetected unknown cases
            if len(self.page_structure.sorted_tag_counter) > 1:
                tag_attr_pair = self.page_structure.sorted_tag_counter[-2][0].split('{')
                tag = tag_attr_pair[0]
                attr = ast.literal_eval('{' + tag_attr_pair[1])
            else:
                return []


        #in-line css is not a distinctive attr, should remove
        attr.pop('style', None)
        attr.pop('Style', None)
        attr.pop('lang', None)
        attr.pop('Lang', None)
        # print tag, attr
        
        # Second round Select
        tmp_second_round_locations = self.soup.findAll(tag, attrs=attr)
        second_round_locations = []
        for tmp_location in tmp_second_round_locations:
            num_valid_names2 = self.seed_regex.findall(tmp_location.text.lower())
            if len(num_valid_names2) <= 3 and len(num_valid_names2) >= 1:   # ????empirical
                second_round_locations.append(tmp_location)

        # Zoom out from second_round_locations to locate the largest parent
        stop_flag = False
        parents_seen = []
        largest_parents = []
        prev_locations = second_round_locations
        depth = 0
        duplicate_largest_parents = 0   # when duplicate parents are seen many times, we know that this duplicate parent may be the parent that contain all the pubs
        MAXIMUM_DUPLICATES_PARENTS = 3  #???? empirical 
        while True:
            depth += 1
            
            # Stopping conditions
            if len(second_round_locations) == 0:
                return []

            if depth > 20:  # In case of forever looping
                return []   

            unique_parent_counter = {}
            tmp_container = []
            # print 'while=================================================================\n======================================================================\n'
            for second_round_location in second_round_locations:
                second_round_parent = second_round_location.parent

                key = str(second_round_parent)
                if unique_parent_counter.has_key(key):
                    unique_parent_counter[key] += 1
                else:
                    unique_parent_counter[key] = 1

                # print second_round_location
                # print '================================'
                # print second_round_parent
                # print '======================================================================\n\n\n'
                if second_round_parent in parents_seen: #When seen duplicate records, but also could be the page editor's fault
                    duplicate_largest_parents += 1
                    if duplicate_largest_parents >= MAXIMUM_DUPLICATES_PARENTS:
                        print '\n\n\n\n\n\n\n\n\nfffffffffffffffound'
                        stop_flag = True
                        break
                else:
                    parents_seen.append(second_round_parent)
                    tmp_container.append(second_round_parent)

            if stop_flag is not True:
                prev_locations = second_round_locations
                second_round_locations = tmp_container
            else:
                # print depth
                largest_parents = second_round_locations
                break

        print len(largest_parents)
        # print largest_parents

        ###############################################################################
        ### Now we can locate the list of largest parents containing the publication 
        ### signature. Further improvements should be done on extracting real pub
        ###############################################################################
        
        for largest_parent in largest_parents:
            content = ""
            pdf_link = self.get_pdf(largest_parent, self.base_url, self.pubpage)  # extract pdf link if possible
            if largest_parent.name in ["li", "p", "div", "ol", "ul", "br", "tr", "td", "table"]:
                content += "\n\n\n\n"
            for child in largest_parent.recursiveChildGenerator():

                # try:
                #   print '<<<<<<<<<<<<<<<<<' + str(child)
                # except Exception, e:
                #   pass

                if isinstance(child, basestring):   #if it is a string
                    childtext = child.strip()
                    # print 1
                    # this text segment is long / is some punctuation / is all upper case which is probably conference name / is number, probably year
                    if (len(childtext) > len(self.lname) or len(PUNCTUATION_REGEX.findall(childtext))>0 or childtext.isupper() or childtext.strip().isdigit() ) and content not in childtext and childtext not in content:
                        if len(childtext) > 500 and childtext.lower().rfind(self.lname) == -1:   # empirical ????
                            pass
                        else:
                            # print 11
                            content += " %s" % childtext

                elif child.name in ["li", "p", "div", "ol", "ul", "tr", "td", "table"]:
                    # print 2
                    content += '\n\n\n\n'
                elif child.name in ['br']:
                    # print 3
                    content += '\n\n'
                elif child.text:
                    # print 4
                    childtext = child.text.strip()
                    if (len(childtext) > len(self.lname) or len(PUNCTUATION_REGEX.findall(childtext))>0 ) and content not in childtext and childtext not in content:
                        # print 44
                        content += " %s" % child.text
            try:
                content = content.encode('ascii', 'ignore')
            except Exception, e:
                print e

            # postprocessing to get the formatted pub records        
            new_real_record = ''
            records = content.split("\n\n\n")
            for i in range(0, len(records)):
                record = records[i].strip()
                try:                    
                    record = record.encode("ascii", "ignore")
                except Exception, e:
                    print "ASCII ERROR ", e, record
                
                record = ' '.join(record.split())
                if record not in new_real_record and len(record.split()) > 2 and len(record.split()) < 100:
                    new_real_record += record + ' '

            for badword in [" pdf ", " ps ", " bibtex ", " slides ", " ppt "]: #remove useless anchor text
                pattern = re.compile(badword, re.IGNORECASE)
                new_real_record = pattern.sub(' ', new_real_record) 

            if new_real_record not in self.real_records and len(new_real_record.split()) > 5 and len(new_real_record.split()) < 200:  # only keep the unique records.  content with fewer than 5 words or more than 200 words don't count 
                year = extract_year(new_real_record, pdf_link)
                self.real_records.append({'record':new_real_record, 'pdf_link':pdf_link, 'year':year})
            elif len(new_real_record)>0:
                print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!' + new_real_record

        # Test output
        for i in range(len(self.real_records)):
            print str(i) + '>>>>' + str(self.real_records[i])





    # Assume only one pdf was included in a pub record
    def get_pdf(self, container, base_url, pubpage):
        retval = ''
        try:
            cadidate_links = container.findAll('a', href=True)
            for candidate in cadidate_links:
                if '.pdf' in candidate['href'].lower():
                    link = candidate['href']
                    retval = urljoin(base_url, link)

        except Exception, e:
            self.error = "%s\nEXTRACTOR-PUBLICATION RECORD: EXTRACT PDF LINK ERROR %s" % (self.error, e)
            print "EXTRACT PDF LINK ERROR ", e
        return retval

# Tests
if __name__ == '__main__':
    p = PublicationExtractor()

    p.locate_records('http://www.cs.toronto.edu/~hinton/', 'hinton')
    
    # p.locate_records('http://www.cs.princeton.edu/~blei/publications.html', 'blei')
    
    # p.locate_records('http://people.cs.umass.edu/~mccallum/pubs.html', 'mccallum')

    # p.locate_records('http://nlp.stanford.edu/manning/papers/', 'manning')

    # p.locate_records('http://adsc.illinois.edu/people/zhenjie-zhang', 'zhang')

    # p.locate_records('http://www.comp.nus.edu.sg/~tbma/cv.html', 'ma') # (difficult to identify the publication?)

    # p.locate_records('http://lunadong.com/', 'dong')

    # p.locate_records('http://www.clairelegoues.com.s3-website-us-east-1.amazonaws.com/', 'claire')

    # p.locate_records('http://www.ece.rice.edu/~al4/publications.html', 'lingamneni')

    # p.locate_records('http://www.win.tue.nl/~nikhil/pubs.html', 'bansal')

    # p.locate_records('http://richardt.name/publications/', 'richardt')

    # p.locate_records('http://www.hbs.edu/faculty/Pages/profile.aspx?facId=6437&facInfo=pub', 'christensen')

    # p.locate_records('http://business.illinois.edu/facultyprofile/All_Publications.aspx?ID=119', 'petruzzi')

    # p.locate_records('http://www.library.illinois.edu/people/bios/jimhahn/', 'hahn')

    # p.locate_records('http://www.emilyknox.net/pubs.html', 'knox')

    # p.locate_records('http://cogcomp.cs.illinois.edu/page/publications', 'roth')

    # p.locate_records('http://www.informatik.uni-trier.de/~ley/pers/hd/l/Liu:Bing.html', 'liu')

    # p.locate_records('http://www.cast.centers.vt.edu/publications/index.html', 'yoon')

    # p.locate_records('http://chemistry.fas.nyu.edu/object/nadriancseeman.html', 'seeman')

    # p.locate_records('http://www.indiana.edu/~nano/publications.html', 'jarrold')

    # p.locate_records('http://www.iwu.edu/english/facultystaff/Terkla.html', 'terkla') #(EXTREMELY HARD)