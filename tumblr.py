import os, time, sys, shelve
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class tumblr():
	def __init__(self, email, password, blog, debug=False):
		# Javascript to get rid of cluttering elements
		self.destroyElemsJS='''
		e = ['fullscreen_post_bg', 'fullscreen_post_footer',
		'l-header-container', 'showcase-pagination',
		'about-tumblr-btn', 'section-content'];
		function destroy (elems) {
			for (var i = elems.length - 1; i >= 0; i--) {
				elemprime = document.getElementsByClassName(elems[i])[0];
				if (typeof elemprime !== 'undefined') {
					elemprime.style.display = 'None';
				}
			}
		}
		destroy(e);
		'''

		# Set tumblr object paramaters
		self.DEBUG = debug
		self.EMAIL = email
		self.PASSWORD = password
		self.BLOG_URL = blog
		self.init_browser()

	'''
	Uploads images in subfolders of given folder
	'''
	def batch_upload(self, folder):
		# self.DATABASE_PATH = os.path.join(os.getcwd(), folder)
		self.DATABASE_PATH = r'P:\images\personal\index'
		# data = self.batchify(10)

		s = shelve.open('tumblr_data.db')
		data = s['tumblr']
		self.upload(data)

	'''
	Opens firefox browser
	checks debug paramaters
	Logs into tumblr account passed
	'''
	def init_browser(self):
		# Open browser
		p = webdriver.FirefoxProfile()
		p.set_preference('browser.privatebrowsing.autostart', True)
		self.BROWSER = webdriver.Firefox(firefox_profile=p)
		self.BROWSER.implicitly_wait(10)
		print('Opened...')

		# Set DEBUG params
		if self.DEBUG:
			self.BROWSER.set_window_position(0, 20)
			self.BROWSER.set_window_size(400, 800)
		else:
			self.BROWSER.set_window_position(0, 2000)
			self.BROWSER.maximize_window()

		self.BROWSER.get('https://www.tumblr.com/login')
		self.BROWSER.execute_script(self.destroyElemsJS)

		for x in range(5):
			self.BROWSER.find_element_by_id('signup_determine_email').send_keys(Keys.CONTROL, Keys.SUBTRACT)

		self.BROWSER.find_element_by_id('signup_determine_email').send_keys(self.EMAIL)
		self.BROWSER.find_element_by_id('signup_forms_submit').click()
		time.sleep(5)
		self.BROWSER.find_element_by_id('signup_password').send_keys(self.PASSWORD)
		self.BROWSER.find_element_by_id('signup_forms_submit').click()

	'''
	Looks for images inside profile folders
	seperates them into uploading batches
	returns dict[folder batch num] = [[10 strings], [10 strings]]
	{profile batch 0: [10strings]}
	'''
	def batchify(self, batch_size):
		profile_folders = next(os.walk(self.DATABASE_PATH))[1]
		def get_data():
			init_data = {}
			for sub_folders in profile_folders:
				folder_path = os.path.join(self.DATABASE_PATH, sub_folders)
				images = next(os.walk(folder_path))[2]
				init_data[sub_folders] = [os.path.join(folder_path, i) for i in images]
			return init_data

		def structure_data(data):
			s = shelve.open('tumblr_data.db')
			final_data = {}
			def chunks(l, n):
				for i in range(0, len(l), n):
					yield l[i:i+n]
			for count, k in enumerate(data.keys()):
				images = data[k]
				for count, chunk in enumerate(chunks(images, batch_size)):
					final_data['{} batch {}'.format(k, str(count+1))] = chunk
			try:
				s['tumblr'] = final_data
			finally:
				s.close()				
			# print(final_data)
			return final_data

		return structure_data(get_data())

	'''
	Makes new photo post with set of data given
	and removes them from dictionary read from
	shelve object
	'''
	def upload(self, data):
		s = shelve.open('tumblr_data.db')
		try:
			data = s['tumblr']
		finally:
			s.close()

		def sort_keys(dic):
			key_name = [k[:k.rfind('h')+1] for k in dic.keys()][4:]
			print(key_name)
			for count, n in enumerate(key_name):
				yield str('{} {}'.format(n, count+1))

		self.BROWSER.get(self.BLOG_URL)
		time.sleep(3)

		for k in sort_keys(data):
			time.sleep(5)
			try:
				self.BROWSER.find_element_by_id('new_post_label_photo').click()
			except:
				pass
			time.sleep(5)

			print(len(data.keys()))
			print('Currently uploading {}'.format(k))
			for count, i in enumerate(data.pop(k)):
				try:
					s = shelve.open('tumblr_data.db')
					s['tumblr'] = data
				finally:
					s.close()
				
				if os.path.isfile(i):
					self.BROWSER.find_element_by_name('photo').send_keys(i)

					if count == 1:
						# Scroll down and fill text area with profile name
						self.BROWSER.execute_script('window.scrollTo(0, document.body.scrollHeight);')
						self.BROWSER.execute_script(r'document.getElementsByClassName("editor-placeholder")[0].innerHTML = ""')
						self.BROWSER.execute_script(r'document.getElementsByClassName("editor-richtext")[0].childNodes[0].innerHTML = "{}<br></br>"'.format(k))
						time.sleep(1)
					if count % 5 == 0:
						try:
							self.BROWSER.find_element_by_class_name('ui_button').click()
						except:
							pass

						# Scroll down every 5th image uploaded
						self.BROWSER.execute_script('window.scrollTo(0, document.body.scrollHeight);')
						time.sleep(1)

			time.sleep(5)
			self.BROWSER.find_element_by_class_name('create_post_button').click()
			time.sleep(5)


t = tumblr(
	email, 
	password, 
	sitename,
	debug=True)

t.batch_upload(path)



# if youtube knows what comments you like they can link that to your phone number
# that you gave when you signed up for gmail
# Using the comments they can use natural language learning to find out the context
# Literally finding out what you support and believe or hate

# you could scrape popular sites to get a sentiment analysis for investing in stocks
