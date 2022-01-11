# open-ssh linux server creation and tunneling through cloudflare quick free tunnel
	- Currently only supports quick free tunnels from cloudflare
	- sshd_config parameters can be changed as required
	- run `make build-whl pip-install` to build and install the package
	- run `make test` and `make lanch_server` as sudo since it requires editing of /etc/sshd_config
	- run `make launch_server` on linux server to start the server tunnel
	- connect to the tunneled server from either windows or linux ssh client through the domain assigned

Dependencies on server side: python>=3.8, pip, python-apt, make