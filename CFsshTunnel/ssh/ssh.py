import subprocess
from CFsshTunnel.utils.package_installer import apt_package_installer

def start_ssh_server():
    """
    Restart ssh
    """
    # Check required packages on server and install if required
    apt_package_installer("openssh-server")
    
    subprocess.run(["service", "ssh", "restart"])


def connect_to_server(hostname: str):
    """
    Checks connection to server hostname
    """
    # Check required packages on server and install if required
    apt_package_installer("openssh-server")
    status = subprocess.check_call(
        ["ssh", hostname, "ls"], shell=False, stdout=subprocess.PIPE)
    if status == 0:
        print("Connection Successful!")
    else:
        print("Failed to connect to remote server")
