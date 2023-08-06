import logging

from .client import InteliquentClient


__author__ = 'Inteliquent'
__version__ = '0.2.0'


# Set up logging to ``/dev/null`` like a library is supposed to.
# http://docs.python.org/3.3/howto/logging.html#configuring-logging-for-a-library
class NullHandler(logging.Handler):
    def emit(self, record):
        pass


log = logging.getLogger('inteliquent')
log.addHandler(NullHandler())


__all__ = ["InteliquentClient"]
