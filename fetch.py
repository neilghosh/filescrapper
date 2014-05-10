import sys
import re
import urllib2
import urllib
import getopt
import httplib

## Configurations
# The starting point 
baseURL = "http://69.65.39.194/MobAudioStories.php"
maxLinks = 1000
excludeList = ["None","/","./","#top"]
fileType = ".mp3"
outFile = "links.txt"
overwrite='a'



#Gloab list of links already visited , don't want to get into loop
vlinks = []
#This is where output is stored the list of files 
files = []

def main(argv):
    global maxLinks
    global outFile
    global overwrite
    try:
        opts, args = getopt.getopt(argv,"hn:o:w:")
    except getopt.GetoptError:
        print 'fetch.py -n <maxLinks> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'fetch.py -n <maxLinks> -o <outputfile>'
            sys.exit()
        elif opt in ("-n", "--nfile"):
            maxLinks = int(arg)
        elif opt in ("-o", "--ofile"):
            outFile = arg
        elif opt in ("-w"):
            overwrite = 'w' if arg == 'True' else 'a'
        print 'maxLinks to be fetched is ', maxLinks
        print 'Output file is ', outFile
        print 'Overwrite exiting links ' , overwrite




# A recursive function which takes a url and adds the outpit links in the global 
# output list.
                                           
def findFiles( baseURL ):
    #URL encoding
    baseURL = urllib.quote(baseURL, safe="/:=&?#+!$,;'@()*[]")
    print "Scanning URL "+baseURL
    
    #Check maximum number of links you want to store
    print "Number of link stored - " + str(len(files)) + " of "+ str(maxLinks)
    if(len(files) > maxLinks):
        return

    # the current page
    website = ""
    try:
        website = urllib2.urlopen(baseURL)
    except urllib2.HTTPError, e:
        print baseURL + " NOT FOUND"
        return
    # HTML content of the current page
    html = website.read()
    # fetch the anchor tags using regular expression from the html
    # Beautifull Soup does it wonderfully in one go
    links = re.findall('(?<=href=["\']).*?(?=["\'])', html)
    # 
    for link in links:    
        #print link        
        url = str(link)
        # Found the file type, then store and move to the next link
        if(url.endswith(fileType)):
            print "file link stored" + url                    
            files.append(url)
            f = open(outFile, overwrite)
            f.write(url+"\n")
            f.close
            
            
            request = urllib2.Request(url)
            request.get_method = lambda : 'HEAD'
            try:
                response = urllib2.urlopen(request)
            except urllib2.HTTPError, err:
                print "Unable to fetch "+url
                continue
            print response.info().getheader('Last-Modified').strip()
            
            continue
        # Exlude external links and self links , else it will keep looping
        if not (url.startswith("http") or ( url in excludeList ) ):
            #Build the absolute URL and show it !
            print "abs url = " + baseURL.partition('?')[0].rpartition('/')[0]+"/"+url
            absURL =  baseURL.partition('?')[0].rpartition('/')[0]+"/"+ url
            #Do not revisit the URL 
            if not (absURL in vlinks):
                vlinks.append(absURL)
                findFiles(absURL)
    return 


if __name__ == "__main__":
    main(sys.argv[1:])
    #Finally call the function
    findFiles(baseURL)
    print files

