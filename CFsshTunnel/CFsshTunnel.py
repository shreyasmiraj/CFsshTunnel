from CFsshTunnel import *
from typing import List
import random

def cloud_ssh_tunnel(ssh_port=random.randint(49153,65534), sshd_config_params: List[str]=[], public_keys: List[str]=[], keep_alive: bool = True):
    """
    Configures and initiates server as specified by default/user
    Parameters
        ssh_port(int): specifies port that openssh-server is listening to
        sshd_config(List[str]): specifies config for sshd_config
        public_keys(List[str]): list of authorized public keys to be added to server ~/.ssh/authorized_keys
        keep_alive(bool): specifies where the server python program should keep running infdefinitely
    """
    #Check required packages on server and install if required
    install_package("openssh-server")
    install_package("cloudflared")

    #accepts List[str] or just str
    add_authorized_public_keys(public_keys = public_keys)
        
    #update ssh_config as specified by user or default parameters and random port if not
    ssh_port = sshd_config(ssh_port=ssh_port, sshd_config_params=sshd_config_params)

    #restarts openssh-server service with new ssh_config
    start_ssh_server()

    #create a trycloudflare.com free tunnel and route ssh://localhost:ssh_port throught the assigned public domain
    _,_ = create_cf_tunnel(ssh_port)

    #keeps the server alive?
    while(keep_alive):
        continue