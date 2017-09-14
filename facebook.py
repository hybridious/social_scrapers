import os, time, pickle, requests, bs4
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
'''
import modfolds

archive_path = modfolds.arch_fold('test', 'archive', 'facebook')
datafolder = modfolds.data_fold('data', 'txt-databases')
os.path.join(datafolder, 'facebook.txt')
datafile = modfolds.join(datafolder, 'facebook.txt')
'''


JS_scripts = {
'scrolldown':'window.scrollTo(0, document.body.scrollHeight);',
'getimage': 
'''
var node = document.getElementsByClassName('spotlight')[0],
image = node.src;
return image;
''',
'destroy':
'''
var e = [
'fullscreen_post_bg'
];
function destroy (elems) {
	for (var i = elems.length - 1; i >= 0; i--) {
		var elem = document.getElementsByClassName(elems[i])[0];
		if (typeof elem !== 'undefined') {
			elem.style.display = 'None';
		}
	}
}
destroy(e);
'''
}

# archive_path = os.path.join(os.getcwd(), 'test', 'archive', 'facebook')
archive_path = r'P:\images\personal\databases\facebook'
database_path = os.path.join(os.getcwd(), 'data', 'txt-databases', 'facebook.txt')

class facebook():
	def __init__(self, email, password, debug=True):
		self.DEBUG = debug
		self.ARCHIVE_PATH = archive_path
		self.DATABASE_FILE_PATH = database_path
		self.EMAIL = email
		self.PASSWORD = password

		self.init_browser(0,30,800,800)
		data = self.get_images_from_albums(email, password)
		self.download_albumdata(data)
		self.teardown()

	def init_browser(self, x, y, w, h):
		it = time.time()
		p = webdriver.FirefoxProfile()
		p.set_preference('browser.privatebrowsing.autostart', True)
		self.B = webdriver.Firefox(firefox_profile=p)
		if self.DEBUG:
			self.B.set_window_position(x, y)
		else:
			self.B.set_window_position(0, 2000)
		self.B.set_window_size(w, h)
		self.B.implicitly_wait(10)
		ft = time.time()
		secs = str(ft-it)
		print('{} seconds to initialize browser'.format(secs))

	'''
	Gets images from every profile given through a text file of profile links
	'''
	def get_images_from_albums(self):
		profiledata = {}
		images = []
		profiles = self.read_data(self.DATABASE_FILE_PATH)

		it = time.time()
		self.B.get('https://www.facebook.com/login')
		for x in range(5):
			self.B.find_element_by_id('email').send_keys(Keys.CONTROL, Keys.SUBTRACT)
		self.B.find_element_by_id('email').send_keys(self.EMAIL)
		self.B.find_element_by_id('pass').send_keys(self.PASSWORD)
		self.B.find_element_by_id('loginbutton').click()
		ft = time.time()
		secs = str(ft-it)
		print('{} seconds to login'.format(secs))

		time.sleep(5)

		for p in profiles:
			it = time.time()

			# GO TO PROFILE
			self.B.get('{}photos_all'.format(p))
			time.sleep(2)

			# GET PROFILE NAME
			title = str(bs4.BeautifulSoup(self.B.page_source, 'lxml').title)
			profile = title[title.find('>')+1:title.rfind('</title')]

			# GO TO PHOTOS and CLICK FIRST PHOTO in set
			self.B.find_elements_by_class_name('_6-6')[3].click()
			time.sleep(2)
			self.B.find_elements_by_class_name('uiMediaThumbImg')[0].click()
			time.sleep(3)

			# PHOTO THEATER LOOP
			while True:
				try:
					curr_img = self.B.execute_script(JS_scripts['getimage'])
				except:
					self.B.find_elements_by_class_name('snowliftPager')[1].click()
					# self.B.find_elements_by_class_name('snowliftPager')[1].click()

				time.sleep(4)

				if curr_img not in images:
					images.append(curr_img)
					print('{}\nImages {}\n'.format(profile,len(images)))
					self.B.find_elements_by_class_name('snowliftPager')[1].click()
				else:
					break
				# elif len(images)>1 and curr_img == images[len(images)-2]:
				# 	print(curr_img)
				# 	print()
				# 	print('index 0')
				# 	print(images[0])
				# 	print('index 1')
				# 	print(images[len(images)-1])
				# 	print('index 2')
				# 	print(images[len(images)-2])
				# 	print('error at photo theather loop1')
				# 	break
				# elif len(images)>1 and curr_img == images[0]:
				# 	print(curr_img)
				# 	print(images[0])
				# 	print(images[len(images)-1])
				# 	print(images[len(images)-2])
				# 	print('error at photo theather loop2')
				# 	break

				del curr_img

			print('PUSH DATA TO STACK')
			profiledata[profile] = list(images)
			time.sleep(1)

			ft = time.time()
			sec = round(ft-it, 2)
			print('{} Seconds of scraping\nProfile: {}\nImages Total: {}\n'.format(str(sec), profile, len(images) ))
			images.clear()

		# print(profiledata.keys())
		return profiledata

	# IDEAL - IMPLEMENT THREADED DOWNLOAD
	# TEMP FIX - FOR LOOPED THROUGH DICTS
	def download_albumdata(self, data):
		# THREAD EVERY PROFILE
		# DUMP IMAGES FROM PROFILE INTO ARCHIVE FOLDER PATH
		# DATASTRUCTURE
		# {profilename: [imagelist]}
		for profilename in data.keys():
			print(profilename)
			images = data[profilename]
			profilefolder = os.path.join(self.ARCHIVE_PATH, profilename)

			if not os.path.isdir(profilefolder):
				os.makedirs(profilefolder)

			imagelist = os.listdir(profilefolder)
			for count, image_url in enumerate(images):
				filename = image_url[image_url.rfind('/')+1:image_url.rfind('?')]
				if not filename in imagelist:
					print('Downloading {} into {}\n{}/{}\n'.format(image_url, profilename, str(count+1), str(len(images)) ))
					with open(os.path.join(profilefolder, filename), 'wb') as f:
						f.write(requests.get(image_url).content)

	def read_data(self, filename):
		with open(filename) as f:
			return f.read().split('\n')

	def pickle_data(self,data, path):
		with open(path, 'rb') as f:
			pickle.dump(data)

	def read_pickle(self, path):
		with open(path, 'wb') as f:
			return pickle.load()

	def teardown(self):
		self.B.close()

f = facebook(EMAIL, PASSWORD)

