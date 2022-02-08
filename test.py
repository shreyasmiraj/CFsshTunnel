import random
import getpass
from CFsshTunnel.utils.package_installer import apt_package_installer, deb_package_installer
from CFsshTunnel.ssh.ssh_config import add_authorized_public_keys, ssh_config_params, sshd_config, ssh_config
from CFsshTunnel.ssh.ssh import start_ssh_server, connect_to_server
from CFsshTunnel.cloudflare.cloudflare import create_cloudflare_tunnel
from CFsshTunnel.cloudflare.cloudflare_config import extract_tunnel_metrics

if __name__ == "__main__":

    # Check required packages on server and install if required
    apt_package_installer("openssh-server")

    CLOUDFLARE_DEB_PATH = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb"
    deb_package_installer("cloudflared", CLOUDFLARE_DEB_PATH)

    # accepts List[str] or just str
    print("\nProvide public auth key for current user running the test server")
    add_authorized_public_keys()

    # update ssh_config as specified by user or default parameters and random
    # port if not
    SSH_PORT = sshd_config()

    # restarts openssh-server service with new ssh_config
    start_ssh_server()

    METRICS_PORT = random.randint(49153, 65534)
    if METRICS_PORT == SSH_PORT:
        METRICS_PORT += 1

    SSH_CLOUDFLARE_CALL = "cloudflared tunnel --url ssh://localhost:" + str(SSH_PORT) +\
        " --logfile cloudflared.log --metrics localhost:" + \
        str(METRICS_PORT)

    METRICS_URL = "http://localhost:" + str(METRICS_PORT) + "/" + "metrics"
    # create a trycloudflare.com free tunnel and route
    # ssh://localhost:SSH_PORT throught the assigned public domain
    create_cloudflare_tunnel(cloudflare_call=SSH_CLOUDFLARE_CALL)

    HOSTNAME = extract_tunnel_metrics(METRICS_URL)
    USER = getpass.getuser()

    SSH_CONFIGURATION = ssh_config_params(
        hostname=HOSTNAME, user=USER, ssh_port=SSH_PORT)

    # update client side ssh_config_params
    ssh_config(SSH_CONFIGURATION)

    # connect to ssh-server through cloudflare public domain tunnel
    connect_to_server(HOSTNAME)
