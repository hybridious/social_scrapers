import os, re, time, requests, urllib, threading, sys, bs4
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

servers = {
# 'e': 'https://discordapp.com/channels/208664083577307136/209502186164584449',
# 's': 'https://discordapp.com/channels/208664083577307136/209501891137241089',
# 'h': 'https://discordapp.com/channels/208664083577307136/209502169068601356',

'aco': 'https://discordapp.com/channels/208664083577307136/209502566340493312',
'gif': 'https://discordapp.com/channels/208664083577307136/209502556844457984',
'gifs': 'https://discordapp.com/channels/181630090277289984/183346551916068864',
'loli': 'https://discordapp.com/channels/181630090277289984/204690226675843072',
'pics': 'https://discordapp.com/channels/181630090277289984/183346708929970177',
'porn': 'https://discordapp.com/channels/181630090277289984/198973083418230784',
# 'bots': 'https://discordapp.com/channels/181630090277289984/204328433625464832',

# 'graphics': 'https://discordapp.com/channels/239061839793618944/284346427654668288',
# 'inspiration': 'https://discordapp.com/channels/239061839793618944/243278005835661312',
# 'comics': 'https://discordapp.com/channels/181630090277289984/183036813751877634',

# 'nsfw': 'https://discordapp.com/channels/306933477318852608/306973127827521546',
# 'nsfw2': 'https://discordapp.com/channels/293793820699787275/293814203632844800',
# 'nsfw3': 'https://discordapp.com/channels/239061839793618944/245100374401351680'
}

class discord():
	def __init__(self, email, password, folder, scrolls=100, debug=False):
		self.DESTROY_JS = '''
		var classNames = [
		'notice', 
		'guilds-wrapper',
		'channels-wrap',
		'title-wrap',
		'channel-members-wrap'
		];

		function destroy (elems) {
			for (var i = elems.length - 1; i >= 0; i--) {
				elemprime = document.getElementsByClassName(elems[i])[0]
				if (typeof elemprime !== 'undefined') {
					elemprime.style.display = 'None';
				}
			}
		}

		destroy(classNames);
		'''

		# CLASS VARIABLES
		self.EMAIL = email
		self.PASS = password
		self.DEBUG = debug
		self.DATABASE_FOLD = r'P:\images\personal\discord'
		self.SERVERS = servers

		if sys.argv[1:]:
			self.SCROLLS = int(sys.argv[1:][0])
		else:
			self.SCROLLS = scrolls
		
		self.init_browser()
		self.login_discord()
		self.get_channel_data()
		# self.tear_down()

	def tear_down(self):
		self.BROWSER.close()

	def init_browser(self):
		p = webdriver.FirefoxProfile()
		p.set_preference('browser.privatebrowsing.autostart', True)
		self.BROWSER = webdriver.Firefox(firefox_profile=p)
		self.BROWSER.set_window_size(600, 900)
		if self.DEBUG:
			self.BROWSER.set_window_position(0, 20)
		else:
			self.BROWSER.set_window_position(0, 2000)
		self.BROWSER.implicitly_wait(10)

	def login_discord(self):
		print('Logging in...')
		self.BROWSER.get('https://discordapp.com/login')
		time.sleep(4)
		self.BROWSER.find_element_by_id('register-email').send_keys(self.EMAIL)
		self.BROWSER.find_element_by_id('register-password').send_keys(self.PASS)
		self.BROWSER.find_element_by_css_selector('.btn').click()
		time.sleep(4)
		self.BROWSER.find_element_by_css_selector('.close-3RZM3j').click()
		# self.BROWSER.find_element_by_css_selector('.flexChild-1KGW5q').click()
		time.sleep(4)

	def get_channel_data(self):
		for k in self.SERVERS.keys():
			folder = os.path.join(self.DATABASE_FOLD, k)
			url = self.SERVERS[k]
			image_set = set()

			if not os.path.isdir(folder):
				os.makedirs(folder)

			self.BROWSER.get(url)
			print('\nAccessing channel: {}\nChannel url: {}'.format(k, url))
			time.sleep(10)
			self.BROWSER.execute_script(self.DESTROY_JS)
			time.sleep(1)
			try:
				# buttonClass = 'buttonBrandFilledDefault-2Rs6u5 buttonFilledDefault-AELjWf buttonDefault-2OLW-v button-2t3of8 buttonFilled-29g7b5 buttonBrandFilled-3Mv0Ra largeGrow-2_1w2U actionRed-sT3Bw5 action-2mLTX4'
				# self.BROWSER.find_element_by_css_selector('.ui-button .filled .brand .large .action-button .dark-red .grow').click()
				# self.BROWSER.find_element_by_class_name('.buttonBrandFilledDefault-2Rs6u5').click()
				self.BROWSER.find_element_by_css_selector('.action-2mLTX4').click()
				# self.BROWSER.find_element_by_css_selector('.ui-button').click()
			except:
				pass

			# SCROLLING LOOP
			for x in range(1,self.SCROLLS):
				time.sleep(0.4)
				print('Scrolling... {}/{}'.format(str(x),str(self.SCROLLS)))

				try:
					self.BROWSER.find_element_by_css_selector('.messages-wrapper').send_keys(Keys.PAGE_UP)
				except:
					pass
				if x % 20 == 0 or x == self.SCROLLS-1:
					init = len(image_set)
					image_set.update( re.findall('(https:\/\/cdn.discordapp.com[\w\d\/\.]*)"', str(self.BROWSER.page_source)) )
					print('\nAdded {} images to set...\n'.format( str(len(image_set) - init ) ))
			image_list = list(image_set)
			for count, i in enumerate(image_list):
				files = next(os.walk(folder))[2]
				filename = i[i.rfind('/')+1:]
				dest = os.path.join(folder, filename)
				if not filename in files:
					try:
						with open(dest, 'wb') as f:
							f.write(i)
						# opener = urllib.request.URLopener()
						# opener.addheader('User-Agent', 'webbrowser')
						# opener.retrieve(i, dest)
						print('\nLink: {}\nFile: {}\nProgress: {}/{}\n'.format( i, dest, str(count+1), str(len(image_list)) ))
					except:
						print('\nERROR downloading file: {}\n'.format(i))

# EMAIL PASS FOLD DEBUG
d = discord('fjjfsx@gmail.com', 'GayBacon', '', debug=True)