import getpass
import random
import subprocess
import os
from pathlib import Path
from typing import List


def add_authorized_public_keys(public_keys: List[str] = []):
	"""
	Adds allowed public keys to ~/.ssh/authorized_keys
	Parameters:
		public_key(List[str]): List of authorized public keys for ssh
	"""
	if len(public_keys) == 0:
		public_keys = [str(getpass.getpass(prompt="ssh-rsa pub auth key:"))]

	home = str(Path.home())
	ssh_path = home+"/.ssh/"
	if os.path.exists(ssh_path) != True:
		os.mkdir(ssh_path)
	try:
		with open(ssh_path+"authorized_keys",'a+') as f:
			for key in public_keys:
				f.write(str(key)+'\n')
	except:
		raise RuntimeError("Error occured while adding keys")


def sshd_config(ssh_port=random.randint(49153,65534), sshd_config_params = []) -> int:
	"""
	Setup sshd_config as specified by config_params array
	Parameters:
		port(int): selects a random port from 49153 to 65534 unless specified
		sshd_config(List[str]): ssh_config parameters as a list of str

	Returns:
		(int): ssh port number
	"""
	if len(sshd_config_params) == 0:
		config_params = ["ClientAliveInterval 120",
						"PasswordAuthentication no",
						"PermitRootLogin yes",
						"Port "+str(ssh_port)]
	else:
		config_params = sshd_config_params

	with open(r"/etc/ssh/sshd_config",'w') as f:
		for config in config_params:
			f.write(config+'\n')
	return ssh_port


def ssh_config(config_params):
	"""
	Configures ~/.ssh/config based on input config parameter
	Parameters
		-config_params(List[str]): Holds list of str paramters per line to be added to config

	"""
	home = str(Path.home())
	ssh_path = home+"/.ssh/"
	with open(ssh_path+"config","w+") as f:
		for config in config_params:
			f.write(config+"\n")


def start_ssh_server():
	"""
	Restart ssh
	"""
	subprocess.run(["service","ssh","restart"])


def connect_to_server(hostname):
	"""
	Checks connection to server hostname
	"""
	check = subprocess.check_call(["ssh",hostname,"ls"],shell=False)
	if check == 0:
		print("Connected to remote server successfully!")
	else:
		print("Failed to connect to remote server")