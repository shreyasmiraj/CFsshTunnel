from CFsshTunnel import *

if __name__ == "__main__":
    
    #accepts List[str] or just str
    add_authorized_public_keys()
        
    #update ssh_config as specified by user or default parameters and random port if not
    ssh_port = sshd_config()

    #restarts openssh-server service with new ssh_config
    start_ssh_server()

    #create a trycloudflare.com free tunnel and route ssh://localhost:ssh_port throught the assigned public domain
    _,_ = create_cf_tunnel(ssh_port)

    #keeps the server alive?
    while(True):
        continue