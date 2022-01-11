import subprocess
import time
import urllib.request
import getpass
from typing import List, Union


def create_cf_tunnel(ssh_port: int, test: bool = False) -> Union[List[str],str]:
    """
    Creates cloudflare tunnel for specified localhost:ssh_port
    cloudflare logs stored under cloudflared.log,
    metrics at localhost:ssh_port+1
    
    Parameters
        ssh_port(int): port on which sshd_config has been configured
        test(bool): enabled for testing server connection with sever as client
    Returns
        config_params(List[str]): contains all the ~/.ssh/config parameters to be set by client
        hostname(str): exposed tunnel hostname
    """
    metrics_port = ssh_port+1
    cf_process = subprocess.Popen(["cloudflared","tunnel","--url","ssh://localhost:"+str(ssh_port),
                                  "--logfile","cloudflared.log","--metrics","localhost:"+str(metrics_port)],
                                  stdout=subprocess.PIPE, universal_newlines=True)
    time.sleep(5)
    
    if cf_process.poll() is not None:
        raise RuntimeError("Failed to create cloudflare tunnel\n")
    hostname = None
    
    for _ in range(10):
        try:
            with urllib.request.urlopen("http://127.0.0.1:"+str(metrics_port)+"/metrics") as response:
                response = str(response.read())
                hostname_begin_str = "userHostname=\"https://"
                hostname_end_str = "trycloudflare.com"
                begin = response.find(hostname_begin_str)
                end = response.find(hostname_end_str)
                hostname = response[begin+len(hostname_begin_str):end+len(hostname_end_str)]
                user = getpass.getuser()
        except:
            time.sleep(10)
        if hostname is None:
            raise RuntimeError("Failed to get hostname from cloudflare metrics\n\n")
    
    time.sleep(10)

    header = "| openssh-server quick tunnel route through cloudflare is now alive |"
    print("\n")
    print("+"+"="*(len(header)-2)+"+")
    print(header)
    print("+"+"="*(len(header)-2)+"+")

    print("Update ~/.ssh/config on client as below:\n")
    print("Note: Windows client users on PS/cmd, provide full path to cloudflared.exe in ProxyCommand\n\
        Ex: Instead of \n\
            `ProxyCommand cloudflared access ssh --hostname %h`\n\
        use `ProxyCommand <complete_path_to_cloudflare.exe> access ssh --hostname %h\n\n")
    

    config_params = ["Host "+str(hostname),
                    "\tHostname %h",
                    "\tUser "+str(user),
                    "\tPort "+str(ssh_port),
                    "\tLogLevel ERROR",
                    "\tUserKnownHostsFile /dev/null",
                    "\tProxyCommand cloudflared access ssh --hostname %h"]

    test_config_params = ["Host "+str(hostname),
                        "\tHostname %h",
                        "\tUser "+str(user),
                        "\tPort "+str(ssh_port),        
                        "\tLogLevel ERROR",
                        "\tUserKnownHostsFile /dev/null",
                        "\tStrictHostKeyChecking no",
                        "\tProxyCommand cloudflared access ssh --hostname %h"]

    print("#Client ~/.ssh/config")
    border ="#"+"-"*max(len(config_params[4]),len(config_params[0])) 
    print(border)
    for config in config_params:
        print(config)
    print(border)
    print("\n\nConnect to openssh-server through the following public domain:")
    print("Note: Since user authentication through ssh-rsa key pair is configured to be true by default,\n\
only those users whose public key has been added to the config will be able to access the server\n")
    client_ssh_terminal_connect = "$ ssh "+str(hostname)
    border2 = "-"*len(client_ssh_terminal_connect) 
    print(border2)
    print(client_ssh_terminal_connect)
    print(border2)

    if test:
        config_params = test_config_params

    return config_params, hostname