import requests, bs4, os

def request(url, tag='', classname='', get='', mode='', regex=''):
	headers = {
		'User-Agent': 'User fucking agent'
	}
	html = requests.get(url, headers=headers).content
	soup = bs4.BeautifulSoup(html, 'lxml')
	if mode == 'html':
		return html
	elif mode == 'tag class':
		return [e.get(get) for e in soup.findAll(tag, class_=classname)]
	elif mode == 'tag':
		print(dir(soup.findAll(tag)))
	elif mode == '':
		return html
	else:
		print(dir())
		# return [e.get(get) for e in soup.findAll(tag)]
		
# url = 'http://binc.com'
url = 'http://bing.com'
# https://archived.moe/b/thread/730322613/
html = requests.get(url).content
soup = bs4.BeautifulSoup(html, 'lxml')
print(soup.prettify())
# print(request(url, tag='a', get='href', mode='html', regex='a href="([\w\d\:\.\/\-]*.html)">'))
# images = request(url, tag='a', classname='thread_image_link', get='href', mode='tag class')
# image = request(images[0], tag='meta', get='url', mode='tag')
# print(image)

# <a href="https://img.yt/img-58fc43c2ba62e.html">
# a href='[\w\d]'

# html = requests.get(images[0], headers=headers).content
# print(html)

# html = request(, 'lxml', mode='html')
# print(html)