import getpass
import random
import subprocess
import os
from pathlib import Path
from time import process_time

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
		public_key = [str(getpass.getpass(prompt="ssh-rsa pub auth key:"))]

	home = str(Path.home())
	ssh_path = home+"/.ssh/"
	if os.path.exists(ssh_path) != True:
		os.mkdir(ssh_path)
	try:
		with open(ssh_path+"authorized_keys",'a+') as f:
			for key in public_key:
				f.write(str(key)+'\n')
	except:
		print("Error occured while adding keys")

def sshd_config(port=random.randint(49153,65534), default_config = []) -> int:
	"""
		Setup sshd_config as specified by config_params array
		Parameters:
			port(int): selects a random port from 49153 to 65534 unless specified
			default_config(List[str]): ssh_config parameters as a list of str

		Returns:
			-(int): ssh port number
	"""
	if len(default_config) == 0:
		config_params = ["ClientAliveInterval 120",
					"PasswordAuthentication no",
					"PermitRootLogin yes",
					"Port "+str(port)]
	else:
		config_params = default_config

	with open(r"/etc/ssh/sshd_config",'w') as f:
		for config in config_params:
			f.write(config+'\n')
	return port

def ssh_config(config_params):
	home = str(Path.home())
	ssh_path = home+"/.ssh/"
	with open(ssh_path+"config","w+") as f:
		for config in config_params:
			f.write(config+"\n")

def start_ssh_server():
	subprocess.run(["service","ssh","restart"])

def connect_to_server(hostname):
	check = subprocess.check_call(["ssh",hostname,"ls"],shell=False)
	if check == 0:
		print("Connected to remote server successfully!")
	else:
		print("Failed to connect to remote server")