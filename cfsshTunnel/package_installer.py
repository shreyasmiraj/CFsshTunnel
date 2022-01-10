import apt
import sys

def install_package(package_name: str):
	"""
		Install's package through apt if not present already
	"""
	cache = apt.cache.Cache()
	cache.update()
	cache.open()

	pkg = cache[package_name]

	if pkg.is_installed:
		print("{pkg_name} already installed".format(pkg_name=package_name))
		return 1
	else:
		print("Installing {pkg_name} through apt-get".format(pkg_name=package_name))
		pkg.mark_install()
		try:
			cache.commit()
			return 1
		except Exception as arg:
			print >> sys.stderr, "{pkg_name} installation failed [{err}]".format(pkg_name=package_name,err=str(arg))
			return 0
