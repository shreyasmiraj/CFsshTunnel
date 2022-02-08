import random
import getpass
from CFsshTunnel.package_installer import apt_package_installer, deb_package_installer
from CFsshTunnel.ssh_config import add_authorized_public_keys, ssh_config_params, sshd_config, ssh_config
from CFsshTunnel.ssh import start_ssh_server, connect_to_server
from CFsshTunnel.cloudflare import create_cloudflare_tunnel
from CFsshTunnel.cloudflare_config import extract_tunnel_metrics

if __name__ == "__main__":

    # Check required packages on server and install if required
    apt_package_installer("openssh-server")

    cloudflare_deb_path = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb"
    deb_package_installer("cloudflared", cloudflare_deb_path)

    # accepts List[str] or just str
    print("\nProvide public auth key for current user running the test server")
    add_authorized_public_keys()

    # update ssh_config as specified by user or default parameters and random
    # port if not
    ssh_port = sshd_config()

    # restarts openssh-server service with new ssh_config
    start_ssh_server()

    metrics_port = random.randint(49153, 65534)
    if metrics_port == ssh_port:
        metrics_port += 1

    ssh_cloudflare_call = "cloudflared tunnel --url ssh://localhost:" + str(ssh_port) +\
        " --logfile cloudflared.log --metrics localhost:" + \
        str(metrics_port)

    metrics_url = "http://localhost:" + str(metrics_port) + "/" + "metrics"
    # create a trycloudflare.com free tunnel and route
    # ssh://localhost:ssh_port throught the assigned public domain
    create_cloudflare_tunnel(cloudflare_call=ssh_cloudflare_call)

    hostname = extract_tunnel_metrics(metrics_url)
    user = getpass.getuser()

    ssh_configuration = ssh_config_params(
        hostname=hostname, user=user, ssh_port=ssh_port)

    # update client side ssh_config_params
    ssh_config(ssh_configuration)

    # connect to ssh-server through cloudflare public domain tunnel
    connect_to_server(hostname)
