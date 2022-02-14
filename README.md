# ssh linux server creation and tunneling through cloudflare tunnels
	- custom ssh and cloudflare tunneling
	- remote code-server tunneling

Server dependencies: 
	- python>=3.5
	- pip
	- python-apt
	- make(optional instead of pip)

Client dependencies:
	- ssh
	- Cloudflared https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation

# Installation
	- [pip](pip)
	- [source](source)
## pip
```
pip install CFsshTunnel
```
### Uninstall
```
pip uninstall CFsshTunnel
```
## source
```
git clone https://github.com/ThePilot916/CFsshTunnel.git
cd ./CFsshTunnel
make build
make pip-install
```
### Uninstall
sudo make clean
make clean

# Launching
	- [ssh-cloudflare-tunnel](ssh-cloudflare-tunnel)
	- [code-server](code-server)


## ssh-cloudflare-tunnel
### using make
```
sudo make launch_server	
```
### python source/notebooks
```
import CFsshTunnel
#Run either with all default parameters or pass ssh/cloudflare config as required
_, hostname, user = CFsshTunnel.CFsshTunnel()
```

## Code-Server

### server
```
from CFsshTunnel.code_server.code_server import launch_codeserver
#cloudflare config and port designation can be specified as required
launch_codeserver(hostname=hostname, user=user)
```
### client
step 1
```
$ ssh -N -L <client_port>:127.0.0.1:<server_port> <user>@<hostname> &
```
step 2
Open http://localhost:<client_port> on any ssh client browser and enjoy!





