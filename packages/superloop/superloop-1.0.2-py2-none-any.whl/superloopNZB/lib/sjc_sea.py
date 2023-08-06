######################## FUNCTIONS ##############################
import subprocess

def sjc_sea(directory):
	print 'mv ~/movies/%s /mnt/sanjose/' % directory
	parallel = subprocess.call('parallel cp -rf ~/movies/%s ::: /mnt/sanjose /mnt/seattle/' % (directory), shell=True)
	rm = subprocess.call('rm -rf ~/movies/%s' % (directory), shell=True) 
	print 'mv complete'
