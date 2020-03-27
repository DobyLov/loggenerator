import os
import platform    # For getting the operating system name

# return platform
def get_platform():
    my_platform = platform.system()
    return my_platform.lower()

# return os release
def get_osRelease():
    my_release = platform.release()
    return my_release.lower()

# return os version
def get_osVersion():
    my_os_version = platform.version()
    return my_os_version.lower()

