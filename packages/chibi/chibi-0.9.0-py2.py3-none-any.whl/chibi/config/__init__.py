from .config import __all__ as config_all, Configuration, Logger_configuration
from .logger import *  # noqa


__all__ = config_all + logger.__all__


configuration = Configuration(
    loggers=Logger_configuration()
)


def load( path ):
    configuration.load( path )
