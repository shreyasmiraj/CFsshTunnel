import sys
import subprocess
import apt


def check_installed(package_name: str) -> bool:
    print("Checking for " + package_name)
    cache = apt.Cache()
    package_installed = False
    if package_name in cache:
        package_installed = cache[package_name].is_installed
    return package_installed


def apt_package_installer(package_name: str):
    """
    Checks for package and installs if needed
    Parameters
        package_name(str): name of the package to be installed
    """
    package_installed = check_installed(package_name=package_name)

    if package_installed:
        print("{pkg_name} already installed".format(pkg_name=package_name))
    else:
        print(
            "Installing {pkg_name} through apt-get".format(pkg_name=package_name))

        cache = apt.cache.Cache()
        cache.update()
        cache.open()
        package = cache[package_name]
        package.mark_install()
        try:
            cache.commit()
        except Exception as arg:
            print >> sys.stderr, "{pkg_name} installation failed [{err}]".format(
                pkg_name=package_name, err=str(arg))


def deb_package_installer(package_name: str, package_url: str):
    """
    Downloads and installs .deb pack from specified url
    """
    package_installed = check_installed(package_name=package_name)
    if package_installed:
        print("{pkg_name} already installed".format(pkg_name=package_name))
    else:
        print("Installing {pkg_name}".format(pkg_name=package_name))
        url_split = package_url.split('/')
        deb_name = url_split[-1]
        try:
            subprocess.call(["wget", package_url])
            subprocess.call(["sudo", "dpkg", "-i", deb_name])
            subprocess.call(["sudo", "rm", "-f", deb_name])
        except BaseException:
            raise RuntimeError(
                "Failed to install package {pkg_name}".format(
                    pkg_name=package_name))
