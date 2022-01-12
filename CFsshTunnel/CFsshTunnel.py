from CFsshTunnel import *
from typing import List
import random
from CFsshTunnel.cloudflare_config import cloudflare_config

from CFsshTunnel.package_installer import deb_package_installer

def cloud_ssh_tunnel(cloudflare_config_params: str=None, ssh_port=random.randint(49153,65534), sshd_config_params: str=None, public_keys: str=None, keep_alive: bool=True):
    """
    Configures and initiates server as specified by default/user
    Parameters
        ssh_port(int): specifies port that openssh-server is listening to
        sshd_config(str): specifies config for sshd_config
        public_keys(str): list of authorized public keys to be added to server ~/.ssh/authorized_keys
        keep_alive(bool): specifies where the server python program should keep running infdefinitely
    """
    #Check required packages on server and install if required
    apt_package_installer("openssh-server")

    # https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation
    cloudflare_deb_url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb"
    deb_package_installer(cloudflare_deb_url)
    
    #accepts List[str] or just str
    add_authorized_public_keys(public_keys = public_keys)

    #update ssh_config as specified by user or default parameters and random port if not
    ssh_port = sshd_config(ssh_port=ssh_port, sshd_config_params=sshd_config_params)

    #restarts openssh-server service with new ssh_config
    start_ssh_server()

    #configure cloudflare.yaml
    configured_cloudflare = cloudflare_config(cloudflare_config_params)

    #create a trycloudflare.com free tunnel and route ssh://localhost:ssh_port throught the assigned public domain
    _,_ = create_cloudflare_tunnel(ssh_port, configured_cloudflare)

    #keeps the server alive?
    while(keep_alive):
        continue