import subprocess


def start_ssh_server():
    """
    Restart ssh
    """
    subprocess.run(["service", "ssh", "restart"])


def connect_to_server(hostname: str):
    """
    Checks connection to server hostname
    """
    status = subprocess.check_call(
        ["ssh", hostname, "ls"], shell=False, stdout=subprocess.PIPE)
    if status == 0:
        print("Connection Successful!")
    else:
        print("Failed to connect to remote server")
