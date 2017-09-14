import os, re, time, requests, urllib.request, threading
from selenium import webdriver
from queue import Queue

# spath = r'L:\pythonscripts\scrapers\instagram\resources'
spath = r'P:\images\personal\twit'
database_path = os.path.join(os.getcwd(), 'data', 'txt-databases', 'twitter.txt')
archive_path = os.path.join(os.getcwd(), 'test', 'archive', 'twitter')

class twitter():
	def __init__(self):
		pass

	def init_browser(self):
		pass
	def teardown_(self):
		pass
	def get_image_data(self):
		pass
q = Queue()
imageData = {}

# Reads files given filename
def readFile(filename):
	with open(filename, 'r') as f:
		text = f.read()
	return text

# Makes files and downloads images
def downloadImages(key, imageData):
	folder = os.path.join(spath, key)
	q_ = Queue()

	if not os.path.isdir(folder):
		os.makedirs(folder)

	def getImages(img, folder):
		src = img
		files = next(os.walk(folder))[2]
		filename = img[img.rfind('/')+1:]
		dest = os.path.join(folder, filename)

		if not filename in files:
			print('Username: {}\nLink: {}\nFile: {}\n'.format(key, src, dest))
			with open(dest, 'wb') as f:
				f.write(requests.get(src).content)
		else:
			print('File exits: {}\nAccount: {}\n'.format(filename, key))

	# Threader
	def imgThreader():
		while True:
			getImages(q_.get(), folder)
			q_.task_done()

	# Start threads
	for x in range(100):
		t = threading.Thread(target=imgThreader)
		t.daemon = True
		t.start()

	# Keys in queue
	for i in range(len(imageData[key])):
		q_.put(imageData[key][i])

	q_.join()

# Reads data from file
# Logs in
# Loops over accounts and downloads image data
def main():
	# JavaScript for image retrieval
	imageJS = '''
	elems = document.getElementsByClassName('AdaptiveMedia-photoContainer js-adaptive-photo');
	cleanElems = [];

	for (var i = elems.length - 1; i >= 0; i--) {
		cleanElems.push(elems[i].getAttribute('data-image-url'))
	};

	return cleanElems
	'''

	# Read the file
	data = readFile(database_path).split('\n')

	# Set up web profile
	profile = webdriver.FirefoxProfile()
	profile.set_preference('browser.privatebrowsing.autostart', True)

	# Open, position, and navigates firefox
	d = webdriver.Firefox(firefox_profile=profile)
	d.set_window_position(0, 2000)
	d.set_window_size(500, 500)
	d.implicitly_wait(10)

	# RETRIEVE DATA
	for a in range(len(data)):
		username = data[a][data[a].find('/', 10)+1:data[a].rfind('/')]
		d.get(data[a])
		d.execute_script('document.getElementById("signin-dropdown").style.display = "none";')
		time.sleep(3)
		scroll = d.execute_script('return document.getElementsByClassName("ProfileNav-value")[0].innerHTML;')
		scrolls = int(re.sub(',', '', re.sub('K', '000', re.sub('\.', '', scroll))))

		# s1 = re.sub('\.', '', scroll)
		# s2 = re.sub('K', '000', s1)
		# scrolls = int(re.sub(',', '', s2))

		for s in range(scrolls):
			si = int(d.execute_script('return document.body.scrollHeight'))
			d.execute_script('window.scrollTo(300, 0);')
			d.execute_script('window.scrollTo(300, document.body.scrollHeight);')
			time.sleep(3.5)
			sf = int(d.execute_script('return document.body.scrollHeight'))
			print('Scrolling: {}/{}'.format(str(s+1), str(scrolls)))
			if sf - si == 0:
				break

		time.sleep(5)
		images = d.execute_script(imageJS)
		imageData[username] = images
		print('\nImages captured: {}'.format(str(len(images))))
		print('Profile progress: {}/{}\n'.format(str(a+1), str(len(data))))

	d.close()

	# Threader
	def threader():
		while True:
			downloadImages(q.get(), imageData)
			q.task_done()

	# Start threads
	for x in range(20):
		t = threading.Thread(target=threader)
		t.daemon = True
		t.start()

	# Keys in queue
	for key in imageData:
		q.put(key)

	q.join()

if __name__ == '__main__':
	main()
