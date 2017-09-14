import os, re, time, urllib.request, threading, sys
from selenium import webdriver
from queue import Queue

class instagram():

#	             ██╗███╗   ██╗██╗████████╗           
#	             ██║████╗  ██║██║╚══██╔══╝            
#	             ██║██╔██╗ ██║██║   ██║               
#	             ██║██║╚██╗██║██║   ██║               
#	 ███████╗    ██║██║ ╚████║██║   ██║       ███████╗
#	 ╚══════╝    ╚═╝╚═╝  ╚═══╝╚═╝   ╚═╝       ╚══════╝

	def __init__(self, user, password, database_path, archive_path, debug=False):
		# JavaScript Elements
		self.GET_IMAGES_JS = '''
var classNames = ['_9bt3u','_2di5p'];
var imageData = [];
function getClassImages(className) {
	var elems = document.getElementsByClassName(className);
	for (i=0;i<elems.length;i++){
		if (elems[i].src !== 'undefined'){
			var link = elems[i].src
			var alpha = link.slice(0,link.indexOf('com')+4)
			var omega = link.slice(link.lastIndexOf('/'),link.length)
			var nstring = alpha + omega
			imageData.push(nstring);
		}
	}
}
getClassImages(classNames[0])
getClassImages(classNames[1])
return imageData
		'''

		self.PROFILE_DATA_JS = '''
var name = document.getElementsByClassName('_rf3jb')[0].innerHTML;
var images = document.getElementsByClassName('_fd86t')[0].innerHTML;
return [name, images];
		'''

		'''
Create DB creator for subfolders of a given folder
params are the DB folder and DB name

create method for bigger object
CREATE DB FROM SUBFOLDS(folder, dbname)
		'''
		self.DEBUG = debug

		# File paths
		self.ARCHIVE_PATH = archive_path
		self.DATABASE_PATH = database_path

		# Full paths
		self.INSTA_DATAFILE = os.path.join(self.DATABASE_PATH, 'instadata.txt')

		# Login
		self.USER = user
		self.PASS = password

		file_data = self.process_datafiles()
		self.init_browser()
		img_data = self.get_data_from_firefox(file_data)
		self.threaded_image_download(img_data)

		# self.preprocess_data()
		# data = self.get_data_from_firefox(self.USER, self.PASS)

#	 ██╗███╗   ██╗██╗████████╗    ██████╗ ██████╗  ██████╗ ██╗    ██╗███████╗███████╗██████╗ 
#	 ██║████╗  ██║██║╚══██╔══╝    ██╔══██╗██╔══██╗██╔═══██╗██║    ██║██╔════╝██╔════╝██╔══██╗
#	 ██║██╔██╗ ██║██║   ██║       ██████╔╝██████╔╝██║   ██║██║ █╗ ██║███████╗█████╗  ██████╔╝
#	 ██║██║╚██╗██║██║   ██║       ██╔══██╗██╔══██╗██║   ██║██║███╗██║╚════██║██╔══╝  ██╔══██╗
#	 ██║██║ ╚████║██║   ██║       ██████╔╝██║  ██║╚██████╔╝╚███╔███╔╝███████║███████╗██║  ██║
#	 ╚═╝╚═╝  ╚═══╝╚═╝   ╚═╝       ╚═════╝ ╚═╝  ╚═╝ ╚═════╝  ╚══╝╚══╝ ╚══════╝╚══════╝╚═╝  ╚═╝
	'''
	Initialize browser and set debug params
	'''
	def init_browser(self):
		p = webdriver.FirefoxProfile()
		p.set_preference('browser.privatebrowsing.autostart', True)
		print('Opening browser...')
		self.BROWSER = webdriver.Firefox(firefox_profile=p)
		if self.DEBUG:
			self.BROWSER.set_window_position(0, 20)
		else:
			self.BROWSER.set_window_position(0, 2000)
		self.BROWSER.set_window_size(500, 500)
		self.BROWSER.implicitly_wait(10)

#	 ██████╗ ██████╗ ███████╗██████╗ ██████╗  ██████╗  ██████╗███████╗███████╗███████╗
#	 ██╔══██╗██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔═══██╗██╔════╝██╔════╝██╔════╝██╔════╝
#	 ██████╔╝██████╔╝█████╗  ██████╔╝██████╔╝██║   ██║██║     █████╗  ███████╗███████╗
#	 ██╔═══╝ ██╔══██╗██╔══╝  ██╔═══╝ ██╔══██╗██║   ██║██║     ██╔══╝  ╚════██║╚════██║
#	 ██║     ██║  ██║███████╗██║     ██║  ██║╚██████╔╝╚██████╗███████╗███████║███████║
#	 ╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚═════╝╚══════╝╚══════╝╚══════╝

	def process_datafiles(self):
		def sort_data(filename):
			data = '\n'.join(self.read_file(filename))
			profile_names_sorted = sorted(re.findall('.com/([\w\d\_\.\-]*)/', data ))				
			data_final = []
			for profile in profile_names_sorted:
				data_final.append('https://www.instagram.com/{}/'.format(profile))
			self.write_file(filename, data)
			print('Sorted {}...\n'.format(filename))

		def check_database_consistency(filename, compare):
			try:
				data = set(self.read_file(filename))
				self.write_file(filename, list(data.update(set(self.read_file(compare)))) )
				sort_data(filename)
				print('Database {} updated...\n'.format(filename))
			except:
				print('Database {} not updated...\n'.format())

		print('Accessing FULL DATABASE')
		return self.read_file(self.INSTA_DATAFILE)

#	 ███████╗██╗██████╗ ███████╗███████╗ ██████╗ ██╗  ██╗
#	 ██╔════╝██║██╔══██╗██╔════╝██╔════╝██╔═══██╗╚██╗██╔╝
#	 █████╗  ██║██████╔╝█████╗  █████╗  ██║   ██║ ╚███╔╝ 
#	 ██╔══╝  ██║██╔══██╗██╔══╝  ██╔══╝  ██║   ██║ ██╔██╗ 
#	 ██║     ██║██║  ██║███████╗██║     ╚██████╔╝██╔╝ ██╗
#	 ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚═╝      ╚═════╝ ╚═╝  ╚═╝

	def get_data_from_firefox(self, data):
		imageData = {}

		# Input user and pass
		print('\nLogging in as: {}'.format(self.USER))
		self.BROWSER.get('https://www.instagram.com/accounts/login/')
		self.BROWSER.find_element_by_name('username').send_keys(self.USER)
		self.BROWSER.find_element_by_name('password').send_keys(self.PASS)
		self.BROWSER.find_element_by_css_selector('._qv64e').click()
		time.sleep(2)
		
		it = time.time()
		# Loop through profile links
		for count, prolink in enumerate(data):
			pro_name = prolink[prolink.find('/', 8)+1:prolink.rfind('/')]
			pro_fold = os.path.join(self.ARCHIVE_PATH, pro_name)
			progress_perc = str( round( (100 * ((count+1)/len(data))) , 2) )
			self.BROWSER.get(prolink)
			time.sleep(3)

			def check_profile():
				# pro_data = self.BROWSER.execute_script(self.PROFILE_DATA_JS)
				try:
					pro_data = self.BROWSER.execute_script(self.PROFILE_DATA_JS)
					if not os.path.isdir(pro_fold):
						os.makedirs(pro_fold)
					return True, pro_data
				except:
					print('\nData collection attempt failed for {}'.format(pro_name))
					return False, 'None'

			result, pro_data = check_profile()

			if result:
				img_profile_total = int(re.sub(',', '', pro_data[1]))
				img_database_total = len(next(os.walk(pro_fold))[2])
				img_delta = int(img_profile_total-img_database_total)
				print('\nLogged in as: {}\nCurrent profile: {}\nStored images: {}\nProfile images: {}\nImage delta: {}'.format( 
					self.USER,
					pro_name,
					img_database_total,
					img_profile_total,
					img_delta
					))

				# Scrolling
				if img_delta > 13:
					scrolls = int(img_delta/11)
					self.BROWSER.execute_script('window.scrollTo(0, document.body.scrollHeight);')
					try:
						self.BROWSER.find_element_by_css_selector('._8imhp').click()
						self.BROWSER.find_element_by_css_selector('._oidfu').click()
					except:
						pass
					for s in range(scrolls):
						self.BROWSER.execute_script('window.scrollTo(0, 0);')
						self.BROWSER.execute_script('window.scrollTo(0, document.body.scrollHeight);')
						print('Scrolling: {}/{}'.format(str(s+1), str(scrolls)))
						time.sleep(1)

				# Capture images
				try:
					time.sleep(2)
					images_captured = self.BROWSER.execute_script(self.GET_IMAGES_JS)
					print(images_captured)
					imageData[pro_name] = images_captured
					print('\nCaptured {} images\nProfile progress: {}%'.format(str(len(images_captured)), progress_perc))
				except:
					print('\nCaptured no images for {}'.format(pro_name))
		ft = time.time()
		dt = round((ft-it), 2)
		print('Retrieving photo data took {} seconds'.format(str(dt) ))

		self.BROWSER.close()
		return imageData

#	 ████████╗██╗  ██╗██████╗ ███████╗ █████╗ ██████╗ ██╗███╗   ██╗ ██████╗ 
#	 ╚══██╔══╝██║  ██║██╔══██╗██╔════╝██╔══██╗██╔══██╗██║████╗  ██║██╔════╝ 
#	    ██║   ███████║██████╔╝█████╗  ███████║██║  ██║██║██╔██╗ ██║██║  ███╗
#	    ██║   ██╔══██║██╔══██╗██╔══╝  ██╔══██║██║  ██║██║██║╚██╗██║██║   ██║
#	    ██║   ██║  ██║██║  ██║███████╗██║  ██║██████╔╝██║██║ ╚████║╚██████╔╝
#	    ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝ ╚═╝╚═╝  ╚═══╝ ╚═════╝ 

	'''
	loops through imageData = {profilename:[images]}
	makes directories for profilenames, keys
	

	'''

	def threaded_image_download(self, imageData):
		q = Queue()
		def get_images(pro_name):
			images = imageData[pro_name]
			for count, src in enumerate(images):
				pro_fold = os.path.join(self.ARCHIVE_PATH, pro_name)
				if not os.path.isdir(pro_fold):
					os.makedirs(pro_fold)
				files = next(os.walk(pro_fold))[2]
				filename = src[src.rfind('/')+1:]
				dest = os.path.join(pro_fold, filename)
				if not filename in files:
					try:
						opener = urllib.request.URLopener()
						opener.addheader('User-Agent', 'webbrowser')
						opener.retrieve(src, dest)
						print('\nUsername: {}\nLink: {}\nFile: {}\nProgress: {}/{}'.format( str(pro_name), str(src), str(dest), str(count+1), str(len(images)) ))
					except:
						print('\nERROR DOWNLOADING FILE: {}\nFOLDER: {}\n'.format( src, pro_name ))

		def threader():
			while True:
				get_images(q.get())
				q.task_done()
		
		# Start threads
		for x in range(100):
			t = threading.Thread(target=threader)
			t.daemon = True
			t.start()

		# Keys in queue
		for k in imageData.keys():
			q.put(k)

		q.join()

	'''
	Reads from a txt file and returns a list of items
	split by new lines
	'''
	def read_file(self, filename):
		with open(filename, 'r') as f:
			return f.read().split('\n')

	'''
	Joins a list into a vertical list of strings in a txt
	'''
	def write_file(self, filename, data):
		with open(filename, 'w') as f:
			return f.write('\n'.join(data))

users = {'meskelpapi': 'madballs1998'}
# 'outhereyeetin_': 'getinsane'

for k, v in users.items():
	i = instagram(k, v, os.path.join(os.getcwd(), 'data', 'txt-databases'),  debug=True)