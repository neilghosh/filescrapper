import datetime
import PyRSS2Gen

items = []

file = open('links.txt', 'r')
 
for line in file:
    print line
    item = PyRSS2Gen.RSSItem(
         title = "Golpo Cast",
         link = line,
         description = "Bangla stories "
                       "from Radio Mirchi"+line,
         guid = PyRSS2Gen.Guid(line),
         pubDate = datetime.datetime(2003, 9, 6, 21, 31))
    items.append(item)

rss = PyRSS2Gen.RSS2(
    title = "Golpo Cast",
    link = "",
    description = "Bangla stories"
                  "from various radio stations",

    lastBuildDate = datetime.datetime.now(),

    items = items)

rss.write_xml(open("pyrss2gen.xml", "w"))