from pkg_resources import get_distribution, DistributionNotFound

APP_NAME_SHORT = "sett"
APP_NAME_LONG = "Secure Encryption and Transfer Tool"

__project_name__ = "sett"
try:
    __version__ = get_distribution(__project_name__).version
except DistributionNotFound:
    __version__ = "0.0.0.dev"
