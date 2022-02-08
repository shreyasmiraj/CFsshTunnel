import time
import urllib.request
import os
from pathlib import Path
from CFsshTunnel.utils.package_installer import deb_package_installer

def cloudflare_config(cloudflare_config_params: str = None):
    """
    Setup ~/.cloudflared/config.yaml file if config is passed
    Parameters
        cloudflare_config_params(str): str of config to be added to ~/.cloudflared/config.yaml
    """
    # https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation
    cloudflare_deb_url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb"
    deb_package_installer("cloudflared", cloudflare_deb_url)
    if cloudflare_config_params is not None:
        home = Path.home()
        cloudflared_config_path = home + "/.cloudflared/"
        if not os.path.exists(cloudflared_config_path):
            os.mkdir(cloudflared_config_path)
        try:
            with open(cloudflared_config_path + "config.yaml") as f:
                f.write(cloudflare_config_params)
                return True
        except BaseException:
            raise RuntimeError("Failed to configure cloudflare")
    return False


def extract_tunnel_metrics(metrics_url: str) -> str:
    """
    Utility function to extract hostname from cloudflare tunnel metrics
    Parameters
        metrics_url(str): str of url to cloudflare metrics
    Returns
        hostname(str): returns tunnel hostname
    """
    hostname = None
    for _ in range(10):
        try:
            with urllib.request.urlopen(metrics_url) as response:
                response = str(response.read())
                hostname_begin_str = "userHostname=\"https://"
                hostname_end_str = "\"}"
                begin = response.find(hostname_begin_str)
                response = response[begin + len(hostname_begin_str):]
                end = response.find(hostname_end_str)
                hostname = response[:end]
        except BaseException:
            time.sleep(10)
        if hostname is None:
            raise RuntimeError(
                "Failed to get hostname from cloudflare metrics\n\n")
    return hostname
