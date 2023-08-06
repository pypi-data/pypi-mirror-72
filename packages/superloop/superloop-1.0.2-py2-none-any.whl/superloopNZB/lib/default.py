######################## FUNCTIONS ##############################
import subprocess

def shared(directory):
	print 'mv ~/movies/%s ~/shared/' % directory
	mv = subprocess.call('mv ~/movies/%s ~/shared/' % directory, shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	print 'mv complete'
