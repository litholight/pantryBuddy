
from urllib.parse import urlparse
import httplib2 as http
import json

file1 = open("barcode.txt",'r')
barcode = file1.read()
file1.close()
headers = {
          'Content-Type': 'application/json',
            'Accept': 'application/json',
                }
ch = http.Http()
lookup = urlparse('https://api.upcitemdb.com/prod/trial/lookup?upc='+barcode)
resp, content = ch.request(lookup.geturl(), 'GET', '', headers)
#data = json.loads(content)
content = str(content)
titleIndex = content.find("title")+8
endIndex = content.find("description")-3
titleString = content[titleIndex:endIndex]
print(titleString)
