import atexit
import signal

from adit.controllers import DaskController, DfsController


# TODO: add more exit/terminate/kill handler
def atexit_handler():
    DaskController.instance().shutdown()
    DfsController.instance().shutdown()


def init():
    atexit.register(atexit_handler)
    signal.signal(signal.SIGHUP, atexit_handler)
    signal.signal(signal.SIGABRT, atexit_handler)
    signal.signal(signal.SIGKILL, atexit_handler)
    signal.signal(signal.SIGTERM, atexit_handler)
