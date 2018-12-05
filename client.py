
import urllib
import urllib2
import browsercookie
import json
import sys
import getopt
from multiprocessing.dummy import Pool as ThreadPool
import time


# url = 'https://bridge.paypalcorp.com/searchsvc/profile/orghierarchy/jzhang13'
# user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
#
# values = {'name': 'Michael Foord',
#           'location': 'pythontab',
#           'language': 'Python'}
# headers = {'User-Agent': user_agent}
# data = urllib.urlencode(values)
#
# cj = browsercookie.chrome()
# opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
# response = opener.open(url).read()
cj = browsercookie.chrome();
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

class Spider:
    def __init__(self, userid):
        self.userid = userid
        self.employeeCount = 0
        self.rootURL = getURL(self.userid)
        self.direct_count = 0;
        self.all_managers = dict()

    def traverse(self):
        rootData = opener.open(self.rootURL).read()
        rootJson = json.loads(rootData)
        # file = open('jzhang13.json','r')
        # rootJson = json.load(file)
        orgHierarchyArray = rootJson['data']['orgHierarchyArray'][0]
        for employee in orgHierarchyArray['items'][0]['items']:
            if employee['userId'] == self.userid:
                currentEmployee = employee

        print 'Hierarchy for userid '+currentEmployee['userId']
        print 'First name:'+currentEmployee['preferredName']
        print 'Last name:'+currentEmployee['lastName']
        team_members = currentEmployee['items'][0]['items']
        self.direct_count= len(team_members)
        self.employeeCount+=len(team_members)
        print 'Direct reports number:'+ str(len(team_members))
        if len(team_members) == 0:
            return;
        for member in team_members:
            count = iterate(member['userId'],self.all_managers)
            self.employeeCount+=count;
            if count >0:
                print 'processed:' + str(self.employeeCount)
        #sorted(self.all_managers.values(), lambda x, y: x[1] > y[1], reverse=True)
        print '----------Manager by employee count'
        sortedList = sorted(self.all_managers.values())
        for sortedKey in sortedList:
            for key, value in self.all_managers.iteritems():
                if value == sortedKey:
                    print key + " " + str(value)

        print 'Number of reports:'+ str(self.employeeCount)



def getURL(userid):
        prefix = 'https://bridge.paypalcorp.com/searchsvc/profile/orghierarchy/'
        return prefix+userid

def iterate(user_id,all_managers):
        #time.sleep(0.05)
        count = 0
        rootData = opener.open(getURL(user_id)).read()
        rootJson = json.loads(rootData)
        orgHierarchyArray = rootJson['data']['orgHierarchyArray'][0]
        for employee in orgHierarchyArray['items'][0]['items']:
            if employee['userId'] == user_id:
                currentEmployee = employee
        if 'items' in currentEmployee:
            team_members = currentEmployee['items'][0]['items']
            if len(team_members) == 0:
                return;
            count+=len(team_members)
            #print 'current_number:'+str(count)
            for member in team_members:
                child_count = iterate(member['userId'],all_managers)
                count+=child_count
                # if child_count >0:
                #     print 'current_number:'+str(count)
        if count>0:
            print user_id + " "+ str(count)
            all_managers[user_id] = count

        return count


def main(argv=None):
    input_name = sys.argv[1];
    spider = Spider(input_name);
    spider.traverse();

if __name__ == '__main__':
    sys.exit(main())







