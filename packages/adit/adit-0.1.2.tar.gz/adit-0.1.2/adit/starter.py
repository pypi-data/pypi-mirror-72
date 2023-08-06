import os
import sys
import logging
import logging.config

from adit.config import Config
from adit.controllers import DfsController, DaskController
from adit import constants as const

# TODO: move the initialization of this into a class or a function and then report user if the environment have not been set
WORKDIR = os.getenv(const.ADIR_HOME_ENV, const.DEFAULT_WORK_DIR)
logger = logging.getLogger(__file__)


def init_logging() -> None:
    log_config = os.path.join(WORKDIR, const.LOGGING_CONF)
    try:
        if os.path.exists(log_config):
            logger.info(f"Initialize logging with {log_config}.")
            logging.config.fileConfig(log_config)
        else:
            logger.error(f"ERROR: Cannot found logging config at {log_config}. Please reinstall!")
    except Exception as ex:
        logger.error(f"Failed to init logging config. Please check the log config file under {log_config}.", exc_info=ex)
        sys.exit(-1)


def init_config(mode: str = None, args: dict = None) -> None:
    configfile = os.path.join(WORKDIR, const.ADIT_CONF)
    try:
        if os.path.exists(configfile):
            logger.info(f"Initialize Adit config with {configfile}.")
            Config.init(config_file=configfile)
            config = Config.instance()
            logger.info(f"Add program arguments as config with.")
            config.set("adit", "mode", mode)
            for key, val in args.items():
                config.set("adit", key, val)
            logger.info(f"Add program arguments as config with.")
            config.dump_config()
        else:
            logger.error(f"ERROR: Cannot found Adit config at {configfile}.")
    except Exception as ex:
        logging.error(f"Failed to init Adit config. Please check the log config file under {configfile}.", exc_info=ex)
        sys.exit(-1)


def start_dfs(mode: str = None, args: dict = None) -> None:
    logger.info(f"Starting Distributed File System...")
    dfs_controller = DfsController.instance()
    dfs_controller.start(mode=mode, args=args)


def start_dask(mode: str = None, args: dict = None) -> None:
    logger.info(f"Starting Dask...")
    dask_controller = DaskController.instance()
    dask_controller.start(mode=mode, args=args)


def start_stream_engine(mode: str = None, args: dict = None) -> None:
    logger.info(f"Starting Streaming Engine...")
    pass


def start(mode: str = None, args: dict = None) -> None:
    try:
        logging.basicConfig(format='[%(asctime)s][%(levelname)8s] %(filename)s:%(lineno)s | %(name)s.%(funcName)s() - %(message)s',
                            level=logging.DEBUG)
        init_logging()
        init_config(mode=mode, args=args)
        start_dfs(mode=mode, args=args)
        start_dask(mode=mode, args=args)
        start_stream_engine(mode=mode, args=args)
    except Exception as ex:
        logger.error(f"Failed to start Adit int {mode} mode", exc_info=ex)