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

### Execution snippets from a notebook
![image](https://user-images.githubusercontent.com/19603746/153012921-2551412b-9861-445f-93ab-53dd13ecabd8.png)

#### ssh_cloudflare tunnel
![image](https://user-images.githubusercontent.com/19603746/153013085-ddbece3c-1309-423f-9b0c-9b3d2983d6c4.png)

#### code-server cloudflare tunnel
![image](https://user-images.githubusercontent.com/19603746/153013345-1a299234-c454-4c63-8b56-ecdbe8dbb9a0.png)

![image](https://user-images.githubusercontent.com/19603746/153013449-5296b7bf-8d35-4905-b357-3f65c58f828a.png)






