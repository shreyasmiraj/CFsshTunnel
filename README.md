# open-ssh linux server creation and tunneling through cloudflare quick free tunnel
	- Currently only supports quick free tunnels from cloudflare
	- sshd_config parameters can be changed as required
	- run `make build-whl pip-install` to build and install the package
	- run `make test` and `make lanch_server` as sudo since it requires editing of /etc/sshd_config
	- run `make launch_server` on linux server to start the server tunnel
	- connect to the tunneled server from either windows or linux ssh client through the domain assigned

Dependencies on server side: python>=3.8, pip, python-apt, make

##pip installation
```
pip install CFsshTunnel==0.2
```

Using it directly from python notebook/script
```
import CFsshTunnel

#Run either with all default parameters or update as needed
CFsshTunnel.cloud_ssh_tunnel()	
```
	
Successful server tunneling will give a similar terminal output with details for client config and connection
![image](https://user-images.githubusercontent.com/19603746/148923523-39d9f492-388d-4251-8b88-c3247ff809eb.png)



