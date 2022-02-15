import random
import getpass

from typing import List, Tuple
from CFsshTunnel.cloudflare.cloudflare_config import extract_tunnel_metrics
from CFsshTunnel.cloudflare.cloudflare import create_cloudflare_tunnel
from CFsshTunnel.utils.package_installer import apt_package_installer, deb_package_installer
from CFsshTunnel.ssh.ssh_config import add_authorized_public_keys, sshd_config, ssh_config_params, sshd_config
from CFsshTunnel.ssh.ssh import start_ssh_server
from CFsshTunnel.utils.decorated_print import box_border, seperator_command_border, seperator_config_border


def CFsshTunnel(
        cloudflare_config_path: str = None,
        ssh_port=random.randint(
            49153,
            65534),
        sshd_config_params: str = None,
        public_keys: str = None,
        test: bool = False) -> Tuple[List[str], str, str]:
    """
    Configures and initiates server as specified by default/user
    Args
        cloudflare_config_path(str): path to custom cloudflare config.yaml
        ssh_port(int): specifies port that openssh-server is listening to
        sshd_config(str): specifies config for sshd_config
        public_keys(str): list of authorized public keys to be added to server ~/.ssh/authorized_keys
        keep_alive(bool): specifies where the server python program should keep running infdefinitely
    Returns
        ssh_configuration(List[str]): list of str of ssh config for client
        hostname(str): cloudflare tunnel hostname
        user(str): server username
    """
    # Check required packages on server and install if required
    apt_package_installer("openssh-server")

    # https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation
    cloudflare_deb_url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb"
    deb_package_installer("cloudflared", cloudflare_deb_url)

    # accepts List[str] or just str
    add_authorized_public_keys(public_keys=public_keys)

    # update ssh_config as specified by user or default parameters and random
    # port if not
    ssh_port = sshd_config(
        ssh_port=ssh_port,
        sshd_config_params=sshd_config_params)

    # restarts openssh-server service with new ssh_config
    start_ssh_server()

    metrics_port = random.randint(49153, 65534)
    if metrics_port == ssh_port:
        metrics_port += 1

    ssh_cloudflare_call = "cloudflared tunnel --url ssh://localhost:" + str(ssh_port) +\
        " --logfile cloudflared.log --metrics localhost:" + \
        str(metrics_port)

    # create a trycloudflare.com free tunnel and route
    # ssh://localhost:ssh_port throught the assigned public domain
    create_cloudflare_tunnel(
        cloudflare_call=ssh_cloudflare_call,
        cloudflare_config_path=cloudflare_config_path)

    metrics_url = "http://localhost:" + str(metrics_port) + "/metrics"
    hostname = extract_tunnel_metrics(metrics_url)
    user = getpass.getuser()

    ssh_configuration = ssh_config_params(
        hostname=hostname, user=user, ssh_port=ssh_port)

    if test:
        ssh_configuration.insert(
            len(ssh_configuration),
            "\tStrictHostKeyChecking no")

    header = "open_ssh_cloudflare tunnel route is now alive at:\n" + hostname + "\n"
    box_border(header)
    print("Update ~/.ssh/config on client as below:\n")
    print("#Client ~/.ssh/config")
    seperator_config_border(ssh_configuration)
    print(
        "Note: Windows client users on PS/cmd, provide full path to cloudflared.exe in ProxyCommand\n\
        Also applies to linux users if PATH to cloudflared isn't added to $PATH\n\
        Ex: Instead of \n\
            `ProxyCommand cloudflared access ssh --hostname %h`\n\
        use `ProxyCommand <complete_path_to_cloudflare.exe> access ssh --hostname %h\n")
    print("\nConnect to openssh-server through the following public domain:")
    client_command = "$ ssh " + str(hostname)
    seperator_command_border(client_command)
    print("\nNote: Since user authentication through ssh-rsa key pair is configured to be true by default,\n\
        only those users whose public key has been added to the config will be able to access the server")
    return ssh_configuration, hostname, user