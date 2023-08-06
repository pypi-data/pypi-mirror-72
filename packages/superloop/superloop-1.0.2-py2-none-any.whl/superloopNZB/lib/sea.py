######################## FUNCTIONS ##############################
import subprocess

def sea(directory):
	print 'mv ~/movies/%s /mnt/seattle/' % directory
	mv = subprocess.call('mv ~/movies/%s /mnt/seattle/' % directory, shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	print 'mv complete'
