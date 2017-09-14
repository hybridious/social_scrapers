import os, time, pickle, requests
from selenium import webdriver

archivefolder = os.path.join(os.getcwd(), 'test', 'archive', 'reddit')
database = os.path.join(os.getcwd(), 'data', 'txt-databases', 'reddit.txt')

class reddit():
	def __init__(self, debug=True):
		self.jsdestroy='''
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
		self.DEBUG = debug
		self.ARCHIVE_PATH = archivefolder
		self.DATABASE_FILE_PATH = database
		email = 'brandonater1998@hotmail.com'
		password = 'gaybacon1998'

		self.init_browser(0,0,300,300)
		self.retrieveImagesFromSubReddits()

		data = self.get_images_from_albums(email, password)

		try:
			self.pickle_data(data, self.DATABASE_FILE_PATH)
		except:
			pass

		self.download_albumdata(data)
		# self.teardown()

	def retrieveImagesFromSubReddits(self):


	def init_browser(self, x, y, w, h):
		p = webdriver.FirefoxProfile()
		p.set_preference('browser.privatebrowsing.autostart', True)
		self.B = webdriver.Firefox(firefox_profile=p)

		if self.DEBUG:
			self.B.set_window_position(x, y)
		else:
			self.B.set_window_position(0, 2000)

		self.B.set_window_size(w, h)
		self.B.implicitly_wait(10)

	'''
	Gets images from every profile given through a text file of profile links
	'''
	def get_images_from_albums(self, email, pw):
		profiledata = {}
		imagedata = {}
		profiles = self.read_data(self.DATABASE_FILE_PATH)
		self.B.get('https://www.facebook.com/login')
		self.B.find_element_by_id('email').send_keys(email)
		self.B.find_element_by_id('pass').send_keys(pw)
		self.B.find_element_by_id('loginbutton').click()

		for p in profiles:
			it = time.time()
			images = []
			profile = p[p.find('/',8)+1:-1]
			self.B.get(p+'photos/')
			time.sleep(5)
			self.B.find_elements_by_class_name('uiMediaThumbImg')[0].click()
			time.sleep(5)
			while True:
				data = self.B.execute_script('''
var node = document.getElementsByClassName('spotlight')[0],
data = node.getAttribute('alt'),
image = node.src;
return [image, data];
					''')
				checkimg = data[0][data[0].rfind('/')+1:data[0].rfind('?')]
				if checkimg in images:
					break
				else:
					images.append(checkimg)
				print('Profile: {}\nImages count: {}\nCurrent image: {}\n'.format(profile, len(images), checkimg ))
				self.B.find_elements_by_class_name('snowliftPager')[0].click()
				imagedata[checkimg] = data[0]
				time.sleep(.75)
			ft = time.time()

			sec = round(ft-it, 2)
			mins = round(sec/60, 2)
			print('{} seconds\n{} minutes\nScraping time\n\nProfile: {}\nImage count: {}\n'.format(str(sec), str(mins), profile, len(images) ))
			profiledata[profile] = imagedata
			images.clear()

		return profiledata

	def download_albumdata(self, data):
		# {profile: {filename: sauce}}
		for profile, lvl2 in data.items():
			for filename, src in lvl2.items():
				dest = os.path.join(self.ARCHIVE_PATH, profile, filename)

				# make folder if not exist in down folder
				if profile not in os.listdir(self.ARCHIVE_PATH):
					os.makedirs(os.path.join(self.ARCHIVE_PATH, profile))

				# Download photo
				with open(dest, 'wb') as f:
					f.write(requests.get(src).content)

				print('Downloaded: {}\nProfile: {}\n'.format(src, profile ))

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

f = reddit()