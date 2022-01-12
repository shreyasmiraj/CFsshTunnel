import subprocess
import time
import urllib.request
import getpass
import os
from pathlib import Path
from typing import List, Union


def cloudflare_config(cloudflare_config_params: str = None):
    """
    Setup ~/.cloudflared/config.yaml file if config is passed
    Parameters
        cloudflare_config_params(str): str of config to be added to ~/.cloudflared/config.yaml
    """
    if cloudflare_config_params is None:
        return False
    else:
        home = Path.home()
        cloudflared_config_path = home + "/.cloudflared/"
        if not os.path.exists(cloudflared_config_path):
            os.mkdir(cloudflared_config_path)
        try:
            with open(cloudflared_config_path + "config.yaml") as f:
                f.write(cloudflare_config_params)
                return True
        except BaseException:
            raise RuntimeError("Failed to configure cloudflare")


def extract_tunnel_metrics(metrics_url: str):
    """
    Utility function to extract hostname from cloudflare tunnel metrics
    Parameters
        metrics_url(str): str of url to cloudflare metrics
    """
    hostname = None
    for _ in range(10):
        try:
            with urllib.request.urlopen(metrics_url) as response:
                response = str(response.read())
                hostname_begin_str = "userHostname=\"https://"
                hostname_end_str = "\"}"
                begin = response.find(hostname_begin_str)
                end = response.find(hostname_end_str)
                hostname = response[begin +
                                    len(hostname_begin_str):end]
                user = getpass.getuser()
        except BaseException:
            time.sleep(10)
        if hostname is None:
            raise RuntimeError(
                "Failed to get hostname from cloudflare metrics\n\n")
    return hostname, user


def create_cloudflare_tunnel(ssh_port: int,
                             configured_cloudflare: bool,
                             cloudflare_call: str = None,
                             test: bool = False) -> Union[List[str],
                                                          str]:
    """
    Creates cloudflare tunnel for specified localhost:ssh_port
    cloudflare logs stored under cloudflared.log,
    metrics at localhost:ssh_port+1

    Parameters
        ssh_port(int): port on which sshd_config has been configured
        configured_cloudflare(bool): set to true if ~/.cloudflared/config.yaml
        test(bool): enabled for testing server connection with sever as client
    Returns
        config_params(List[str]): contains all the ~/.ssh/config parameters to be set by client
        hostname(str): exposed tunnel hostname
    """
    metrics_port = ssh_port + 1
    metrics_url = "http://127.0.0.1:" + str(metrics_port) + "/metrics"
    default_cloudflare_call = "cloudflared tunnel --url ssh://localhost:" + str(ssh_port) +\
                              " --logfile cloudflared.log --metrics localhost:" + \
        str(metrics_port)
    configured_cloudflare_call = "cloudflared tunnel --config ~/.cloudflared/config.yaml"

    if cloudflare_call is None:
        if configured_cloudflare:
            cloudflare_call = configured_cloudflare_call
        else:
            cloudflare_call = default_cloudflare_call

    cf_process = subprocess.Popen(
        cloudflare_call.split(" "),
        stdout=subprocess.PIPE,
        universal_newlines=True)
    time.sleep(15)

    if cf_process.poll() is not None:
        raise RuntimeError("Failed to create cloudflare tunnel\n")

    hostname, user = extract_tunnel_metrics(metrics_url)

    ssh_config_params = ["Host " + str(hostname),
                         "\tHostname %h",
                         "\tUser " + str(user),
                         "\tPort " + str(ssh_port),
                         "\tLogLevel ERROR",
                         "\tUserKnownHostsFile /dev/null",
                         "\tProxyCommand cloudflared access ssh --hostname %h"]

    if test:
        ssh_config_params.insert(
            len(ssh_config_params),
            "\tStrictHostKeyChecking no")

    header = "| openssh-server quick tunnel route through cloudflare is now alive |"
    print("\n")
    print("+" + "=" * (len(header) - 2) + "+")
    print(header)
    print("+" + "=" * (len(header) - 2) + "+")
    print("Update ~/.ssh/config on client as below:\n")
    print(
        "Note: Windows client users on PS/cmd, provide full path to cloudflared.exe in ProxyCommand\n\
        Ex: Instead of \n\
            `ProxyCommand cloudflared access ssh --hostname %h`\n\
        use `ProxyCommand <complete_path_to_cloudflare.exe> access ssh --hostname %h\n\n")
    print("#Client ~/.ssh/config")
    border = "#" + "-" * len(str(max(ssh_config_params, key=len)))
    print(border)
    for config in ssh_config_params:
        print(config)
    print(border)
    print("\n\nConnect to openssh-server through the following public domain:")
    print("Note: Since user authentication through ssh-rsa key pair is configured to be true by default,\n\
only those users whose public key has been added to the config will be able to access the server\n")
    client_ssh_terminal_connect = "$ ssh " + str(hostname)
    border2 = "-" * len(client_ssh_terminal_connect)
    print(border2)
    print(client_ssh_terminal_connect)
    print(border2)

    return ssh_config_params, hostname
