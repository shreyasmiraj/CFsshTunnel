import subprocess
import random
import time
from CFsshTunnel.utils.decorated_print import box_border, seperator_command_border
from CFsshTunnel.utils.package_installer import check_installed


def install_codeserver():
    """
        Installs code-server from https://code-server.dev/install.sh script
    """
    package_installed = check_installed("code-server")
    if package_installed is False:
        print("Installing code-server")
        curl_process = subprocess.Popen(
            "curl -fsSL https://code-server.dev/install.sh".split(" "),
            stdout=subprocess.PIPE)
        subprocess.check_output(("sh"), stdin=curl_process.stdout)
        curl_process.wait()


def launch_codeserver(user:str,
        hostname: str, 
        code_server_config_path: str = None,
        server_port: int = random.randint(
            49153,
            65534),
        client_port: int = None,
        ssh_mode: bool = True
):
    """
    Launch code-server on specified or random port and map it to specified cloudflare tunnel
    Args:
        user(str): server user
        hostname(str): cloudflare tunnel hostname
        code_server_config_path(str): path to custom config.yaml for code-server
        server_port(int): specify port for codeserver
        client_port(int): specify client port to connect to code-server
        ssh_mode(bool): mode of connection to code-server via ssh, if false
                        a new cloudflare tunnel is created and mapped to code-server,
                        passwd auth is enforced from default config and custom config.yaml is not allowed
                        to ensure safety
    """
    # install code-server if required
    install_codeserver()
    
    if client_port is None:
        client_port = server_port

    if ssh_mode is False:
        auth_mode = "password"
    else:
        auth_mode = "none"

    if code_server_config_path is None:
        #defaul code-server config file
        code_server_config_path = "~/.config/code-server/config.yaml"

    # code-server launch comand
    codeserver_command = "code-server" + " "\
         + "--bind-addr" + " " + "127.0.0.1:"+ str(server_port) + " "\
         + "--auth" + " " + auth_mode + " "\
         + "--config"+ " " + code_server_config_path
    
    # launch code-server
    print("Launching code-server...")
    subprocess.Popen(codeserver_command.split(" "))
    time.sleep(5)
    #port forward client localhost to remote instance
    print("\nPort forward client localhost:" + str(client_port) + " onto the remote code-server instance through ssh as follows(run this on your client device): ")
    seperator_command_border("$ ssh -N -L "+ str(client_port) + ":127.0.0.1:" + str(server_port) + " " + user + "@" + hostname + " " + "&")
    box_border("Codeserver is now accessible at: http://localhost:" + str(client_port) +"\n Note: localhost cannot provide SSL, so use http instead of https")