from CFsshTunnel.CFsshTunnel import CFsshTunnel
from CFsshTunnel.utils.utils import keep_alive
from CFsshTunnel.code_server.code_server import launch_codeserver


if __name__ == "__main__":
    _, hostname, user = CFsshTunnel()
    launch_codeserver(hostname=hostname, user=user)
    keep_alive()