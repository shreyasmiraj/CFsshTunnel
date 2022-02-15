import subprocess
import time
from pathlib import Path

def create_cloudflare_tunnel(cloudflare_call: str = None,
                             cloudflare_config_path: str = None
                             ):
    """
    Creates cloudflare tunnel for specified localhost:ssh_port
    cloudflare logs stored under cloudflared.log,
    metrics at localhost:ssh_port+1

    Parameters
        cloudflare_call(str): cloudflared command to execute
        configured_cloudflare(bool): set to true if ~/.cloudflared/config.yaml
    """
    if cloudflare_config_path is None:
        home = str(Path.home())
        cloudflare_config_path = home+"/.cloudflared/config.yaml"

    configured_cloudflare_call = "cloudflared tunnel --config " + cloudflare_config_path

    if cloudflare_call is None:
        cloudflare_call = configured_cloudflare_call

    cf_process = subprocess.Popen(
        cloudflare_call.split(" "),
        stdout=subprocess.PIPE,
        universal_newlines=True)
    time.sleep(15)

    if cf_process.poll() is not None:
        raise RuntimeError("Failed to create cloudflare tunnel\n")
