import os, bs4, time, requests, random, threading
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from queue import Queue

# GLOBAL PATHS
# ARCHIVE & DATA
# archive_path = os.path.join(os.getcwd(), 'test', 'archive', 'vsco')
archive_path = r'P:\images\personal\databases\vsco'
database_path = os.path.join(os.getcwd(), 'data', 'txt-databases', 'vsco.txt')

JS_scripts = {
'scrolldown': 'window.scrollTo(0, document.body.scrollHeight);',

'getimages' : 
'''
var elems = document.getElementsByTagName('img');
var srcs = [];
for (var i=0; i<elems.length; i++){
	var str1 = elems[i].getAttribute('src');
	var str2 = str1.slice(0, str1.indexOf('?'));
	var res = 'https:'+str2;
	srcs.push(res);
};
return srcs.slice(1, srcs.length);
'''
}

class vsco():
	def __init__(self, debug=True):
		self.DEBUG = debug
		urls = sorted(self.get_data_txt(database_path))

		self.init_browser()
		data = self.get_data_site(urls)
		self.download_data(data)
		self.teardown_browser()

	def init_browser(self):
		# profile = webdriver.FirefoxProfile()
		# profile.set_preference('browser.privatebrowsing.autostart', True)
		path = r'C:\Users\fjjfs\Downloads\chromedriver_win32'
		path = r'C:\Users\fjjfs\Downloads\geckodriver-v0.18.0-win64'
		self.B = webdriver.Firefox(path)
		self.B.set_window_size(500, 900)
		if self.DEBUG:
			self.B.set_window_position(0, 20)
		else:
			self.B.set_window_position(0, -2000)
		self.B.implicitly_wait(10)

	def get_data_site(self, urls):
		# {profile: [images]}
		data = {}
		images = set()

		for url in urls:
			time.sleep(3)
			self.B.get(url)
			p = self.B.title
			profile = p[:p.find(' ')]
			it = time.time()

			while True:
				self.B.execute_script(JS_scripts['scrolldown'])
				time.sleep(5)
				page_images = self.B.execute_script(JS_scripts['getimages'])
				images.update(page_images)

				try:
					self.B.find_element_by_css_selector('.next').click()
				except:
					ft = time.time()
					data[profile] = [i for i in images]
					print('{}\n{} images\n{} seconds\n'.format( profile, str(len(images)), str(round(ft-it, 2)) ) )
					images.clear()
					break

				print(page_images)
				print(self.B.current_url)
				print(len(images))

		return data

	# COULD BE THREADED BY PUTTING EACH IMAGE THROUGH A THREAD
	# OR EVERY PROFILE THROUGH A THREAD
	def download_data(self, data):
		for p in data.keys():
			profilefolder = os.path.join(archive_path, p)
			self.folder_contingency(profilefolder)
			existingfiles = os.listdir(profilefolder)
			images = data[p]
			print(profilefolder)
			for i in images:
				filename = i[i.find('/', 10):].replace('/', '')
				fpath = os.path.join(profilefolder, filename)
				if filename not in existingfiles:
					print('Downloaded {} into {}'.format(filename, p))
					with open(fpath, 'wb') as f:
						f.write(requests.get(i).content)
				else:
					print('{} already downloaded'.format(filename))

		# q = Queue()
		# def download_images(p):
		# 	profilefolder = os.path.join(archive_path, p)
		# 	self.folder_contingency(profilefolder)
		# 	existingfiles = os.listdir(profilefolder)
		# 	images = data[p]
		# 	for i in images:
		# 		filename = i[i.find('/', 10):].replace('/', '')
		# 		fpath = os.path.join(profilefolder, filename)
		# 		if filename not in existingfiles:
		# 			print('Downloaded {} into {}'.format(filename, p))
		# 			with open(fpath, 'wb') as f:
		# 				f.write(requests.get(i).content)

		# def threader():
		# 	while True:
		# 		download_images(q.get())
		# 		q.task_done()
		
		# for x in range(100):
		# 	t = threading.Thread(target=threader)
		# 	t.daemon = True
		# 	t.start()
		
		# for p in data.keys():
		# 	q.put(p)
		
		# q.join()

	# RETRIEVES DATA FROM PATH
	# STRUCTURE - txt \n
	def get_data_txt(self, path):
		with open(path, 'r') as f:
			return f.read().split('\n')

	# MAKES FOLDER IF NOT EXISTS
	def folder_contingency(self, folder):
		if not os.path.isdir(folder):
			os.makedirs(folder)

	# TEARS DOWN WEBBROWSER
	def teardown_browser(self):
		self.B.close()

v = vsco()



# //im.vsco.co/1/557a12eb182c14642282/591f17a30bfc48081a71d4c5/vsco_051917.jpg?w=300&dpr=1
# //im.vsco.co/1/5505f500452482685437/587588a45bf45d0c9e433773/vsco_011017.jpg?w=300&dpr=1

# https://im.vsco.co/1/5505f500452482685437/587588a45bf45d0c9e433773/vsco_011017.jpg

# http://vsco.co/melanienunez/images/1
# http://vsco.co/alexismyhre/images/1
# http://vsco.co/jilliancaple/images/1
# http://vsco.co/covvjayy/images/1
# http://vsco.co/haileydacier/images/1
# http://vsco.co/jocelynweart/images/1
# http://vsco.co/dayleerobles/images/1
# http://vsco.co/jayceekeefe/images/1
# http://vsco.co/jillea/images/1
# http://vsco.co/soleilmorla/images/1
# http://vsco.co/jamieee3/images/1
# http://vsco.co/sydneymorgannnf/images/1
# http://vsco.co/katiehar/images/1
# http://vsco.co/jamiedaneri/images/1
# http://vsco.co/faithllewis/images/1
# http://vsco.co/alexmarsh/images/1
# http://vsco.co/lanashevv/images/1
# http://vsco.co/jillianmdavis11/images/1
# http://vsco.co/natashatk/images/1
# http://vsco.co/kayabeck02/images/1
# http://vsco.co/kayleegrimes01/images/1
# http://vsco.co/emiilyyynicolee/images/1
# http://vsco.co/nevaehdeann/images/1
# http://vsco.co/graciewhitee/images/1