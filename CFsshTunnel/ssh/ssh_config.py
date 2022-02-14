import getpass
import random
import os
from pathlib import Path
from typing import List


def add_authorized_public_keys(public_keys: str = None):
    """
    Adds allowed public keys to ~/.ssh/authorized_keys
    Parameters:
        public_key(str): authorized public keys for ssh
    """

    if public_keys is None:
        public_keys = [str(getpass.getpass(
            prompt="authorized ssh-rsa pub auth keys sep by newline:"))]

    home = str(Path.home())
    ssh_path = home + "/.ssh/"
    if not os.path.exists(ssh_path):
        os.mkdir(ssh_path)
    try:
        with open(ssh_path + "authorized_keys", 'a+') as f:
            for public_key in public_keys:
                f.write(public_key)
                f.write('\n')
    except BaseException:
        raise RuntimeError("Error occured while adding keys")


def sshd_config(ssh_port=random.randint(49153, 65534),
                sshd_config_params: str = None) -> int:
    """
    Setup sshd_config as specified by config_params array
    Parameters:
        ssh_port(int): selects a random port from 49153 to 65534 unless specified
        sshd_config(str): custom sshd_config

    Returns:
        (int): ssh port number
    """

    if sshd_config_params is None:
        config_params = ["ClientAliveInterval 120",
                         "PasswordAuthentication no",
                         "PermitRootLogin yes",
                         "Port " + str(ssh_port)]
    else:
        config_params = [sshd_config_params]

    with open(r"/etc/ssh/sshd_config", 'w') as f:
        for config in config_params:
            f.write(config + '\n')
    return ssh_port


def ssh_config_params(hostname: str, user: str, ssh_port: int) -> List[str]:
    """
    Returns ssh client config for the given hostname, user and port
    """
    config_params = ["Host " + str(hostname),
                     "\tHostname %h",
                     "\tUser " + str(user),
                     "\tPort " + str(ssh_port),
                     "\tLogLevel ERROR",
                     "\tUserKnownHostsFile /dev/null",
                     "\tProxyCommand cloudflared access ssh --hostname %h"]
    return config_params


def ssh_config(config_params: str):
    """
    Configures ~/.ssh/config based on input config parameter
    Parameters
        config_params(str): Holds list of str paramters per line to be added to config
    """

    home = str(Path.home())
    ssh_path = home + "/.ssh/"
    with open(ssh_path + "config", "w+") as f:
        for config in config_params:
            f.write(config + "\n")
