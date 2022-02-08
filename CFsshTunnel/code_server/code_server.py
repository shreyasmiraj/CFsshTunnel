import subprocess
import random
import getpass
from sys import stdin
from CFsshTunnel.cloudflare.cloudflare import create_cloudflare_tunnel
from CFsshTunnel.cloudflare.cloudflare_config import extract_tunnel_metrics, cloudflare_config
from CFsshTunnel.utils.decorated_print import box_border
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
        install_process = subprocess.check_output(
            ("sh"), stdin=curl_process.stdout)
        curl_process.wait()


def launch_codeserver(
        port: int = random.randint(
            49153,
            65534),
        cloudflare_config_params: str = None
):
    """
        Launch code-server on specified or random port and map it to a cloudflare tunnel
        port(int): specify port for codeserver
        cloudflare_config_params(str): specify custom cloudflare/config.yaml as needed
    """
    # install code-server if required
    install_codeserver()

    # code-server launch comand
    codeserver_command = "code-server --bind-addr localhost:" + str(port)

    # cloudflare tunnel
    METRICS_PORT = port + 1
    METRICS_URL = "http://localhost:" + str(METRICS_PORT) + "/metrics"
    codeserver_tunnel_command = "cloudflared tunnel --url localhost:" + \
        str(port) + " --metrics localhost:" + str(port + 1)

    # launch code-server
    print("Launching code-server...")
    subprocess.Popen(codeserver_command.split(" "))

    # configure cloudflare config.yaml
    configured_cloudflare = cloudflare_config(
        cloudflare_config_params=cloudflare_config_params)

    print("Creating cloudflare tunnel...")
    # create cloudflare tunnel and map code-server to the tunnel
    create_cloudflare_tunnel(
        cloudflare_call=codeserver_tunnel_command,
        configured_cloudflare=configured_cloudflare)

    hostname = extract_tunnel_metrics(metrics_url=METRICS_URL)
    box_border("Codeserver is now accessible at: https://" + hostname)
