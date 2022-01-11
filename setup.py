from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
	name = 'CFsshTunnel',
	packages = find_packages(),
	version = '0.2',
	license = 'MIT',
	description = 'A light weight open-ssh server tunnel through cloudflare free tunnel service',
	long_description = long_description,
	long_description_content_type = "text/markdown",
	url = 'https://github.com/ThePilot916/CFsshTunnel.git',
	download_url = '',
	keywords = ['SSH', 'Tunnel', 'Cloudflare','colab_ssh','aws','aws_ssh','vscode_server','vscode_remote','google colab'],
	install_requires = ["python-apt"],
	classifiers = [
		'Intended Audience :: Developers',
		'Topic :: Software Development :: Build Tools',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3.8'
		]
)
