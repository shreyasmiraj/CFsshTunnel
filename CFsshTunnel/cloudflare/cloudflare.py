import subprocess
import time


def create_cloudflare_tunnel(cloudflare_call: str = None,
                             configured_cloudflare: bool = False,
                             ):
    """
    Creates cloudflare tunnel for specified localhost:ssh_port
    cloudflare logs stored under cloudflared.log,
    metrics at localhost:ssh_port+1

    Parameters
        cloudflare_call(str): cloudflared command to execute
        configured_cloudflare(bool): set to true if ~/.cloudflared/config.yaml
    """

    configured_cloudflare_call = "cloudflared tunnel --config ~/.cloudflared/config.yaml"

    if configured_cloudflare:
        cloudflare_call = configured_cloudflare_call

    cf_process = subprocess.Popen(
        cloudflare_call.split(" "),
        stdout=subprocess.PIPE,
        universal_newlines=True)
    time.sleep(15)

    if cf_process.poll() is not None:
        raise RuntimeError("Failed to create cloudflare tunnel\n")
