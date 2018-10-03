import ipfsapi
import os
import pickle
import subprocess

class IpfsUtility:

	def __init__(self, IPFS_API_PORT = 5001):
		self.api = ipfsapi.connect('127.0.0.1', IPFS_API_PORT)
		self.init_filelist()


	def add(self, path):
		pwd = os.getcwd()
		os.chdir(path)
		os.chdir('..')

		list_of_hashes = []
		# Size is None for directories
		# TODO: Validate path
		file_hashes = str(subprocess.check_output(f'ipfs add -r {path}', shell=True, stderr=open(os.devnull, 'w'))).split('added')[1:]
		file_hashes[-1] = file_hashes[-1][:-1]
		file_hashes = [x[1:-2] for x in file_hashes]
		for filehash in file_hashes:
			size = None
			hash, name = filehash.split(' ')
			if os.path.isfile(name):
				size = os.path.getsize(name)
			list_of_hashes.append({'name' : name, 'hash' : hash, 'size' : size})
		os.chdir(pwd)
		self.add_to_filelist(list_of_hashes)

	# TODO: Move it to appropriate location where it runs during first run only
	def init_filelist(self):
		filelist = {'directory' : [], 'file' : []}
		with open('own.filelist', 'wb') as f_list:
			pickle.dump(filelist, f_list, pickle.HIGHEST_PROTOCOL)

	def get_filelist(self):
		with open('own.filelist', 'rb') as f_list:
			filelist = pickle.load(f_list)
		return filelist

	def add_to_filelist(self, list_of_hashes):
		filelist = self.get_filelist()
		for fileobject in list_of_hashes:
			temp = filelist
			fullpath = fileobject['name'].split('/')
			for path in fullpath[:-1]:
				path_exists = False
				for i in temp['directory']:
					if i['name'] == path:
						# Already exists
						path_exists = True
						temp = i
				if not path_exists:
					new_object = {'name' : path, 'directory' : [], 'file' : []}
					temp['directory'].append(new_object)
					temp = new_object
			new_object = {'name' : fullpath[-1], 'hash' : fileobject['hash'], 'directory' : [], 'file' : []}
			if not fileobject['size']:
				# Is a directory
				dir_or_file = 'directory'
			else:
				# Is a file
				dir_or_file = 'file'
				new_object['size'] = fileobject['size']
			path_exists = False
			for i in temp[dir_or_file]:
				if i['name'] == fileobject['name']:
					# Already exists
					# TODO: Check hash to see if a newer version of file/directory is being added
					path_exists = True
					temp = i
			if not path_exists:
				temp[dir_or_file].append(new_object)
				temp = new_object
		print(filelist)
		with open('own.filelist', 'wb') as f_list:
			pickle.dump(filelist, f_list, pickle.HIGHEST_PROTOCOL)



# TODO: Remove this
# For testing purpose only
def main():
	ipfs = IpfsUtility()
	ipfs.add('D://code')

if __name__ == '__main__':
	main()
		