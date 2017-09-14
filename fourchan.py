import requests, bs4, re, threading, os, time, threading, bs4
from queue import Queue

q = Queue()

archive_fold = os.path.join(os.getcwd(), 'test', 'archive', '4chan')
url = 'http://boards.4chan.org/b/thread/741810184'
res = str(requests.get(url).content)
soup = bs4.BeautifulSoup(res, 'lxml')
t_name = str(soup.title)
t_name = t_name[t_name.find('- ')+1:t_name.find(' - 4chan')]
files = ['https:'+e.get('href') for e in soup.findAll('a', class_='fileThumb')]

dest = os.path.join(archive_fold, t_name)

if not os.path.isdir(dest):
	os.makedirs(dest)

def download_images(thing):
	link = thing[1]
	filename = link[link.rfind('/')+1:]
	print(link, thing[0])
	with open(os.path.join(dest, filename), 'wb') as f:
		f.write(requests.get(link).content)

def threader():
	while True:
		download_images(q.get())
		q.task_done()

for x in range(100):
	t = threading.Thread(target=threader)
	t.daemon = True
	t.start()

for f in enumerate(files):
	# print(l[0], l[1])
	q.put(f)

q.join()


'''
# chan('4chan',board, queries, seek_delay=40)
# GIANT JERK OFF BANK IS THE DREAM
# for b in boards:

# make a thread for every board
# function to search for relavent threads on each board
# construct folder structure and dump files attained from threads
# each thread is checked every 30 seconds

# EACH BOARD LINK IS DYNAMICALLY ACCESSED
# DUMP EACH Q FOR BOARD IN data['BOARDS']

q = Queue()
data = {
'queries': [
'rule34',
'rule 34',
'r34',
'snap',
'her',
'tit',
'boob',
'porn',
'bikini',
'milf',
'blowjob',
'loli',
'celeb',
'nake',
'creep',
'porn',
'nude',
'webm',
'R34',
'fap',
'spooky',
'braces'
],

'boards': [
'wg',
'gif',
'aco',
'b',
's',
'e',
# 'bant'
],

'regex': [
'&gt;',
'&#039;',
'&quot;',
'&#039;'
]
}

uber_patt = '\w\d\s\&\#\;\,\.\(\)\?'
thread_patt = '"(\d*)":{"date"*'
tease_patt = '\"teaser\":\"([{}]*)'.format(uber_patt)
sleeptime = 0.2
threads = 200

archive_fold = os.path.join(os.getcwd(), 'test', 'archive', '4chan')
# data_fold = os.path.join(os.getcwd(), 'data', 'txt-databases', '')

for b in data['boards']:
	board = b
	b_url = 'https://boards.4chan.org/{}/catalog'.format(board)
	domain = b_url[:b_url.find('/',8)+1]

	board_html = str(requests.get(b_url).content)
	t_links = re.findall(thread_patt, board_html)
	teases = re.findall(tease_patt, board_html)

	def pack_threads():
		if len(teases) == len(t_links):
			for i in range(len(teases)):
				yield (domain+'{}/thread/'.format(board)+t_links[i], teases[i])

	def thread_filter(pack):
		t_url = pack[0]
		tease = pack[1].lower()

		# Request from the threads in boards
		t_html = str(requests.get(t_url).content)
		images = re.findall('a href=\"(\/\/i.4cdn[\w\d\/\.]*)\"\starget=\"_blank', t_html)
		img_links = ['https:'+i for i in images]
		clean_tease = [tease.replace(ch, '') for ch in ['&#039;', '&gt;', '&amp;', '?', '(', ')', '&lt;'] if ch in tease]
		thread_fold = os.path.join(archive_fold, b, clean_tease[:60])

		# for ch in ['&#039;', '&gt;', '&amp;', '?', '(', ')', '&lt;']:
		# 	if ch in tease:
		# 		clean_tease = tease.replace(ch, '')

		# print(t_url)
		# print(thread_fold)
		if not os.path.isdir(thread_fold):
			os.makedirs(thread_fold)
			img_list = os.listdir(thread_fold)
			for i, url in enumerate(img_links):
				filename = url[url.rfind('/')+1:]
				time.sleep(sleeptime)
				if filename not in img_list:
					percent = round(( 100*((i+1)/len(img_links)) ), 2)
					print('board: {}\nthread: {}\nimage count: {}\npercentage: {}%\n'.format(b, cleanTease, len(img_links), percent ))
					with open(os.path.join(thread_fold, filename), 'wb') as f:
						f.write(requests.get(url).content)

		# if len(img_links) > 10:
		# 	print(len(img_links), tease)
		# 	# time.sleep(5)

	def threader():
		while True:
			thread_filter(q.get())
			q.task_done()

	for x in range(threads):
		t = threading.Thread(target=threader)
		t.daemon = True
		t.start()

	for t in pack_threads():
		for c in data['queries']:
			if c in t[1]:
				q.put(t)
	q.join()
'''