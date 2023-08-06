######################## FUNCTIONS ##############################
import subprocess

def sjc(directory):
	print 'mv ~/movies/%s /mnt/sanjose/' % directory
	mv = subprocess.call('mv ~/movies/%s /mnt/sanjose/' % directory, shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	print 'mv complete'
