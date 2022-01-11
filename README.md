# open-ssh linux server creation and tunneling through cloudflare quick free tunnel
	- Currently only supports quick free tunnels from cloudflare
	- sshd_config parameters can be changes as required
	- run `make test` as sudo since it requires editing of /etc/ssh/sshd_config

Dependencies on server side: python>=3.8, pip, python-apt, make
