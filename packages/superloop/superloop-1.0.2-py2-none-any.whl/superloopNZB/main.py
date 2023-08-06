#!/usr/bin/env python

from mappings import get_show
import subprocess
import re
import os


def main():

	os.system('clear')

	while True:
		
		if(int(ls() >= 1)):
			directory = get_dir()

			if(re.search('UNPACK',directory)):
				refresh = False
				pass
			else:
				sliding_size = get_size(directory)
				print 'SCANNING'
				refresh = True

			while refresh:

				print 'NESTED WHILE LOOP'
				current_size = get_size(directory)
				
				if(sliding_size == current_size):
					print 'ABOUT TO COPY'
					module = get_show(directory)
					print '%s' % module
					module(directory)	
					refresh = False	
				
				else:
					pass
		else:
			pass

def ls():

	ls = subprocess.Popen('ls ~/movies/ | wc -l', shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	list = ls.stdout.readline()
	list = list.strip('\n')
	filecount = int(list)
	ls.kill()

	return filecount

def get_dir():

	directory = subprocess.Popen('ls ~/movies/', shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	directory_name = directory.stdout.readline()
	directory_name = directory_name.strip('\n')   
	directory.kill()
	
	return directory_name

def get_size(directory):

	du = subprocess.Popen('du ~/movies/%s | awk {\'print$1\'}' % directory, shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	filesize_count = du.stdout.readline()
	filesize_count = filesize_count.strip('\n')
	filesize = int(filesize_count)
	du.kill()

	return filesize
	
if __name__ == '__main__':
	main()
