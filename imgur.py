import requests, bs4, re, threading, os, time, queue

# url = 'http://imgur.com/a/KV0UZ#WfTcF7K'
url = 'http://imgur.com/a/KV0UZ'
html = requests.get(url).content
soup = bs4.BeautifulSoup(html, 'lxml')
images = ['https:'+e.get('src') for e in soup.findAll('img')][:-3]
title = str(soup.title)
albumname = title[title.rfind('<title>')+7:title.rfind('-')].strip()

archivefolder = os.path.join(os.getcwd(), 'test', 'archive', 'imgur')
dest = os.path.join(archivefolder, albumname)

if not os.path.isdir(dest):
	os.makedirs(dest)

for x in images:
	filename = x[x.rfind('/')+1:]
	print(filename)
	with open(os.path.join(dest, filename), 'wb') as f:
		f.write(requests.get(x).content)