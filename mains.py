import urllib
import urllib2
import os
from HTMLParser import HTMLParser
import requests
def urlEncoder(f):
    # f=f.replace(" ","+")
    f=urllib.quote(f)
    f = f.replace("%20", "+")
    return f


def loadRSS(sd):
    # url of rss feed
    url = 'https://archive.ics.uci.edu/ml/datasets/'+sd
    print url
    # creating HTTP response object from given url
    resp = requests.get(url)
    return resp.content

def loadRSSnew(sd):
    url='https://archive.ics.uci.edu/ml/'+sd
    # creating HTTP response object from given url
    resp = requests.get(url)
    return resp.content

datName=['Abalone']
for dat in datName:
    sd = urlEncoder(dat)
    x = loadRSS(sd)
    sd = []
    class MyHTMLParser(HTMLParser):
        def handle_starttag(self, tag, attrs):
            for attr in attrs:
                if ('href' in attr):
                    sd.append(str(attr).strip())
    parser = MyHTMLParser()
    parser.feed(x)
    mainLink=sd[9]
    mainLink = mainLink[13:]
    mainLink=mainLink[:-2]
    print mainLink
    x=loadRSSnew(mainLink)
    folderName=dat[0:10]
    sd = []
    class MyHTMLParser1(HTMLParser):
        def handle_starttag(self, tag, attrs):
            for attr in attrs:
                if ('href' in attr):
                    print "     attr:", attr
                    sd.append(str(attr).strip())


    parser = MyHTMLParser1()
    parser.feed(x)
    print 'Start Cleaning'
    cleanLinks = []
    for p in sd:
        s = p[10:]
        cleanLinks.append(s[:-2])
    del cleanLinks[0:5]
    print cleanLinks
    folderName=str(folderName)
    xpath = 'C:\\Users\\varagarw\\PycharmProjects\\learnML\\' + folderName
    newpath = r'C:\\Users\\varagarw\\PycharmProjects\\learnML\\' + folderName
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    os.chdir(xpath)
    for link in cleanLinks:
        fin = url = 'https://archive.ics.uci.edu/ml/datasets/'+mainLink
        url = fin + '/' + link
        file_name = url.split('/')[-1]
        u = urllib2.urlopen(url)
        pathe = "C:\\Users\\varagarw\\PycharmProjects\\learnML\\" + folderName + "\\" + file_name
        f = open(pathe, 'wb')
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        print "Downloading: %s Bytes: %s" % (file_name, file_size)
        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)
            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
            status = status + chr(8) * (len(status) + 1)
            print status,

        f.close()

