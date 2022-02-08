# open-ssh linux server creation and tunneling through cloudflare tunnels
	- sshd_config and cloudflare_config parameters can be changed as required
	- connect to the tunneled server from either windows or linux ssh client through the domain assigned

Server dependencies: python>=3.5, pip, python-apt, make

Client dependencies: ssh, Cloudflared installation: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation

# Installation
## pip install
```
pip install CFsshTunnel
```

### Uninstall
```
pip uninstall CFsshTunnel
```

## manual installation
	- run `make build pip-install` to build and install the package
	- run `sudo make test` to test server and client functionality (requires server's pub rsa key to run the test successfully)

## Launching server

### through make
	- run `sudo make launch_server` on linux server to start the server tunnel (launches with all default config)

### from within python source/notebooks
```
import CFsshTunnel
#Run either with all default parameters or pass ssh/cloudflare config as required
CFsshTunnel.CFsshTunnel()
```

## Code-Server

### Launching code-server and mapping to tunnel domain
```
from CFsshTunnel.code_server.code_server import launch_codeserver
#cloudflare config and port designation can be specified as required
launch_codeserver()
```
### Connecting to code server
```
	just open the tunnel domain on any browser
	password prompt should be visible asking for password from ~/.config/code-server/config.yaml or as configured in the code-server config.yaml(ex: cert)
```
execute as root/sudo user since python-apt, /etc/ssh/sshd_config and ~/.ssh/config require that access

In case of runtime error due to failure to acquire cloudflare tunnel, just restart the server, should work in a try or two

ssh Port designation is set to random between `49153 to 65534` unless specified

cloudflare logging should be available as ./cloudflared.log

cloudflare metrics will be on http://localhost:metrics_port

Successful server tunneling will give a similar terminal output with details for client config and connection
![image](https://user-images.githubusercontent.com/19603746/148923523-39d9f492-388d-4251-8b88-c3247ff809eb.png)





