import apt
import sys


def install_package(package_name: str):
	"""
	Checks for package and installs if needed
	Parameters
	package_name(str): name of the package to be installed
	"""
	cache = apt.cache.Cache()
	cache.update()
	cache.open()
	print("Checking for "+package_name)
	pkg = cache[package_name]

	if pkg.is_installed:
		print("{pkg_name} already installed".format(pkg_name=package_name))
	else:
		print("Installing {pkg_name} through apt-get".format(pkg_name=package_name))
		pkg.mark_install()
		try:
			cache.commit()
		except Exception as arg:
			print >> sys.stderr, "{pkg_name} installation failed [{err}]".format(pkg_name=package_name,err=str(arg))
