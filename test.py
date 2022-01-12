from CFsshTunnel import *
from CFsshTunnel.package_installer import apt_package_installer

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

    # configure cloudflare.yaml
    configured_cloudflare = cloudflare_config()

    # create a trycloudflare.com free tunnel and route
    # ssh://localhost:ssh_port throught the assigned public domain
    config_params, hostname = create_cloudflare_tunnel(
        ssh_port, configured_cloudflare, test=True)

    # update client side ssh_config_params
    ssh_config(config_params)

    # connect to ssh-server through cloudflare public domain tunnel
    connect_to_server(hostname)
