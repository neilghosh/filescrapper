from bs4 import BeautifulSoup
import re
import urllib2
import urllib


vlinks = []
files = []
baseURL = "http://69.65.39.194/MobAudioStories.php"

                                           
def findFiles( baseURL ):
    #baseURL.replace(" ","%20")
    baseURL = urllib.quote(baseURL, safe="/:=&?#+!$,;'@()*[]")
    print "Scanning URL "+baseURL
    
    #Check maximum number of links you want to store
    print "Number of link stored - " + str(len(files))
    if(len(files) > 1000):
        return

    #soup = BeautifulSoup(urllib2.urlopen(baseURL))
    website = ""
    try:
        website = urllib2.urlopen(baseURL)
    except urllib2.HTTPError, e:
        print baseURL + " NOT FOUND"
        return
    html = website.read()
    links = re.findall('(?<=href=["\']).*?(?=["\'])', html)
    #tags = soup.find_all(href=re.compile(".\.php$"))
    #for link in soup.find_all('a'):
    #print html
    for link in links:    
        #print link
        
        url = str(link)
        if(url=="None" or url=="/" or url=="./" or url=="#top"):
            continue            
            #ignore the external link
        if(url.endswith(".mp3")):
            print "file link stored" + url                    
            files.append(url)
            f = open('links.txt', 'a')
            f.write(url+"\n")
            f.close
            continue
        if not (url.startswith("http")):
            #Build the absolute URL
            print "abs url = " + baseURL.partition('?')[0].rpartition('/')[0]+"....."+"/"+ "........."+url
            absURL =  baseURL.partition('?')[0].rpartition('/')[0]+"/"+ url
            #Only Keep the MP3 urls
            if not (absURL in vlinks):
                vlinks.append(absURL)
                findFiles(absURL)
    return 

findFiles(baseURL)
print files