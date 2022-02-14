import time
import urllib.request


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
