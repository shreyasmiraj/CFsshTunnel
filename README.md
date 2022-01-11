# open-ssh linux server creation and tunneling through cloudflare quick free tunnel
	- Currently only supports quick free tunnels from cloudflare
	- sshd_config parameters can be changed as required
	- run `make build-whl pip-install` to build and install the package
	- run `make launch_server` on linux server to start the server tunnel
	- connect to the tunneled server from either windows or linux ssh client through the domain assigned

Dependencies on server side: python>=3.8, pip, python-apt, make
Cloudflared installation: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation

## pip install
```
pip install CFsshTunnel==0.4
```

Using it directly from python notebook/script
```
import CFsshTunnel

#Run either with all default parameters or update as needed
CFsshTunnel.cloud_ssh_tunnel()
```
## Uninstall
```
pip uninstall CFsshTunnel
```

execute as root/sudo user since python-apt, /etc/ssh/sshd_config and ~/.ssh/config require that access
In case of runtime error due to failure to acquire cloudflare tunnel, just restart the server, should work in a try or two
ssh Port designation is set to random between `49153 to 65534` unless specified
cloudflare logging should be available as ./cloudflared.log
cloudflare metrics will be on ssh://localhost:ssh_port+1

Successful server tunneling will give a similar terminal output with details for client config and connection
![image](https://user-images.githubusercontent.com/19603746/148923523-39d9f492-388d-4251-8b88-c3247ff809eb.png)

## Colab instance ssh 
run cloud_ssh_tunnel on colab instance, and connect via local terminal/vscode-remote-server
![image](https://user-images.githubusercontent.com/19603746/148963453-cf4cb946-5b21-470e-8e7f-5de27dff71f5.png)

connecting to colab from a local wsl terminal
![image](https://user-images.githubusercontent.com/19603746/148963353-face02f0-34a7-4acf-88a7-863f419df2f6.png)

connecting to vscode-server to colab
(Note: for windows client replace cloudflared in ~/.ssh/config ProxyCommand with full path to cloudflared.exe)
![image](https://user-images.githubusercontent.com/19603746/148964153-5d9b65ee-96d9-4255-a803-c0a0985eddeb.png)





