import subprocess
import time
import urllib.request

def create_cf_tunnel(ssh_port: int) -> int:
    """
        Creates cloudflare tunnel for specified localhost ssh_port
        cloudflare logs stored under cloudflared.log,
        metrics at localhost ssh_port+1 
    """
    metrics_port = ssh_port+1
    cf_process = subprocess.Popen(["cloudflared","tunnel","--url","ssh://localhost:"+str(ssh_port),"--logfile","cloudflared.log","--metrics","localhost:"+str(metrics_port)],
                                  stdout=subprocess.PIPE, universal_newlines=True)
    time.sleep(5)
    if cf_process.poll() is not None:
        raise RuntimeError("Failed to create cloudflare tunnel.")
    
    for _ in range(10):
        with urllib.request.urlopen("http://127.0.0.1:"+str(metrics_port)+"/metrics") as response:
            response = str(response.read())
            hostname_begin_str = "userHostname=\"https://"
            hostname_end_str = "trycloudflare.com"
            begin = response.find(hostname_begin_str)
            end = response.find(hostname_end_str)
            hostname = response[begin+len(hostname_begin_str):end+len(hostname_end_str)]
            print(hostname)
        
        if hostname is None:
            raise RuntimeError("Failed to get hostname from cloudflare metrics")
    print("===========================================================\n")
    print("openssh-server tunnel route through cloudflare is now alive\n")
    print("===========================================================\n")
    print("domain name mapped to ssh is: {hostname}\n".format(hostname=hostname))
    
    print("ssh_client config needs to be UPDATED as follows:\n\n")
    print("Host *trycloudflare.com\n")
    print("\tHostName %h\n")
    print("\tUser root\n")
    print("\tPort {ssh_port}".format(ssh_port=ssh_port))
    print("\tProxyCommand cloudflared access ssh --hostname %h")

    print("Connect to openssh-server through `ssh {hostname}`".format(hostname=hostname))
