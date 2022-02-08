import random
from CFsshTunnel.package_installer import apt_package_installer, deb_package_installer
from CFsshTunnel.ssh_config import add_authorized_public_keys, sshd_config, ssh_config
from CFsshTunnel.ssh import start_ssh_server, connect_to_server
from CFsshTunnel.cloudflare import create_cloudflare_tunnel
from CFsshTunnel.CFsshTunnel import cloud_ssh_tunnel

if __name__ == "__main__":

    # Check required packages on server and install if required
    apt_package_installer("openssh-server")

    cloudflare_deb_path = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb"
    deb_package_installer(cloudflare_deb_path)

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
    metrics_url = "http://127.0.0.1:"+str(metrics_port)

    ssh_cloudflare_call = "cloudflared tunnel --url ssh://localhost:" + str(ssh_port) +\
                              " --logfile cloudflared.log --metrics " + \
        str(metrics_url)

    # create a trycloudflare.com free tunnel and route
    # ssh://localhost:ssh_port throught the assigned public domain
    create_cloudflare_tunnel(cloudflare_call=ssh_cloudflare_call)
    ssh_config_params, hostname = cloud_ssh_tunnel(ssh_port=ssh_port, test=True)

    # update client side ssh_config_params
    ssh_config(ssh_config_params)

    # connect to ssh-server through cloudflare public domain tunnel
    connect_to_server(hostname)
