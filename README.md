# ssh server cloudflare tunnel
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
	
----------------------------
## Installation
- [pip](#pip)
- [source](#source)
### pip
```
pip install CFsshTunnel
```
#### Uninstall
```
pip uninstall CFsshTunnel
```
### source
```
git clone https://github.com/ThePilot916/CFsshTunnel.git
cd ./CFsshTunnel
make dependencies
make install
```
#### Uninstall
```
sudo make clean
make clean
```
----------------------------

## Launching
- [ssh-cloudflare-tunnel](#ssh-cloudflare-tunnel)
- [code-server](#code-server)


### ssh-cloudflare-tunnel
#### using make
```
sudo make launch_server	
```
#### python source/notebooks
```
import CFsshTunnel
#Run either with all default parameters or pass ssh/cloudflare config as required
_, hostname, user = CFsshTunnel.CFsshTunnel()
```
Note: Ensure to update ~/.ssh/config on the client as displayed on the output after running CFsshTunnel()

### code-server
```
import CFsshTunnel
from CFsshTunnel.code_server.code_server import launch_codeserver
_, hostname, user = CFsshTunnel.CFsshTunnel()
launch_codeserver(hostname=hostname, user=user)
```

----------------------------------
### client - setup

Ensure to update ~/.ssh/config on the client as displayed on the output after running CFsshTunnel()

- ssh
```
$ ssh <user>@<hostname>
```
- code-server
```
$ ssh -N -L <client_port>:127.0.0.1:<server_port> <user>@<hostname>
```
Now open http://localhost:<client_port> on any ssh client browser and enjoy!

-------------------------------------------
### Code-snippets from google-colab
[Colab_notebook](https://colab.research.google.com/drive/152zroEV520DSOr0MhwzHAXIeYOTwmRjV?usp=sharing)

![image](https://user-images.githubusercontent.com/19603746/153889417-2aac027d-d30d-4947-a17e-b6552e9c0b83.png)
![image](https://user-images.githubusercontent.com/19603746/153889593-e5368e12-70ac-4e44-907b-f8630a8f1447.png)
![image](https://user-images.githubusercontent.com/19603746/153889641-ca53ed07-10ce-4869-935f-7027b62d2735.png)







