CURR_PATH := $(pwd)

dependencies:
	sudo apt-get update

	#install_cloudflared
	wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
	sudo dpkg -i cloudflared-linux-amd64.deb
	#remove .deb file after installation
	sudo rm -f cloudflared-linux-amd64.deb
	
	sudo apt-get install ssh

	sudo apt-get install python-apt

build:	setup.py
	python setup.py sdist bdist_wheel

pip-install:
	pip install -U ./dist/*.whl

install: setup.py
	python setup.py install

test:	test.py
	python test.py

launch_server: server.py
	python server.py

clean:
	rm -rf *.egg-info
	rm -rf build
	rm -rf dist
	rm -rf cloudflared.log
	rm -rf ./*/__pycache__
	pip uninstall CFsshTunnel
