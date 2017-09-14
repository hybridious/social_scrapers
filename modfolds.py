import os

# archivefolder = modfolds.arch_fold('test', 'archive', 'facebook')
# datafolder = modfolds.data_fold('data', 'txt-databases')

# datafolder.txts['facebook.txt']
# dictionary of txts inside of datafolder
# returns full path of given txt name

# os.path.join(datafolder, 'facebook.txt')
# datafile = modfolds.join(datafolder, 'facebook.txt')

class modfolds():
	def __init__(self):
		pass

	def fold(*args):
		print(args)
		# return os.path.join(args)

	def data_fold(*args):
		for x in args:
			path = os.path.join(x)
		print(path)
		return path

archivefolder = modfolds.data_fold('test', 'archive', 'facebook')
datafolder = modfolds.data_fold('data', 'txt-databases')

# print(archivefolder)
# print(datafolder)
# datafolder.txts['']

# archivefolder = arch_fold('test', 'archive', 'facebook')
# datafolder = data_fold('data', 'txt-databases')
# datafile = join(datafolder, 'facebook.txt')