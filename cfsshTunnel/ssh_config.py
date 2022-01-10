import getpass
import random
import subprocess
from pathlib import Path

def add_authorized_public_keys(public_key=[]) -> int:
	"""
	Parameters:
		public_key:
			- (str): authorized public key for ssh
			- (List[str]): List of authorized public keys for ssh
	Returns:
		- (int):
				0 - failure
				1 - success
	"""
	if len(public_key) == 0:
		public_key = [getpass.getpass()]
		print("asked key")
	try:
		home = str(Path.home())
		with open(home+"/.ssh/authorized_keys",'a') as f:
			for key in public_key:
				f.write(str(key)+'\n')
		return 1
	except:
		print("Error occured while adding keys")
		return 0

def ssh_config(port=random.randint(49153,65535)) -> int:
	"""
		Setup sshd_config as specified by config_params array
		selects a random port from 49152 to 65535
		Returns:
			-(int): ssh port number
	"""
	config_params = ["ClientAliveInterval 120",
					"PasswordAuthentication no",
					"PermitRootLogin yes",
					"Port "+str(port)]

	with open(r"/etc/ssh/sshd_config",'w') as f:
		for config in config_params:
			f.write(config+'\n')
	return port

def start_ssh_server():
	subprocess.run(["service","ssh","restart"])