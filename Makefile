CURR_PATH := $(pwd)

build:	setup.py
	python setup.py sdist bdist_wheel

pip-install:
	pip install -U ./dist/CFsshTunnel-1.2-py3-none-any.whl

install:
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
	rm -rf ./CFsshTunnel/__pycache__
	pip uninstall CFsshTunnel
