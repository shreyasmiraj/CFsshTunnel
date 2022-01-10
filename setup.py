from setuptools import setup, find_packages

setup(
	name = 'CFsshTunnel',
	packages = find_packages(),
	version = '0.1',
	license = 'MIT',
	description = 'A light weight open-ssh server tunnel through cloudflare free tunnel service',
	author = 'Shreyas Miraj',
	author_email = 'shreyasmiraj8@gmail.com',
	url = 'https://github.com/ThePilot916/CFsshTunnel',
	download_url = '',
	keywords = ['SSH', 'Tunnel', 'Cloudflare'],
	install_requires = [],
	classifiers = [
		'Intended Audience :: Developers',
		'Topic :: Software Development :: Build Tools',
		'License :: MIT License',
		'Programming Language :: Python :: 3.8'
		]
	)
