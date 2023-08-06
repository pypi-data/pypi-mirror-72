from __future__ import annotations

import os
import logging
import logging.config
import configparser
from typing import Union

import adit.constants as const

__all__ = ['Config']


class Config:
    _INSTANCE = None

    def __init__(self, config_file: str = None) -> None:
        self.config = configparser.ConfigParser()
        if config_file is None:
            self.__init_with_default()
        else:
            self.__init_with_file(config_file)

    def __init_with_default(self) -> None:
        self.config['adit'] = {}
        self.config['adit']['workdir'] = self.workdir = os.getenv(const.ADIR_HOME_ENV, const.DEFAULT_WORK_DIR)
        self.config['adit']['aditconfig_file'] = self.configfile = os.path.join(self.workdir, const.ADIT_CONF)
        self.config['adit']['logging_conf'] = self.loggingconf = os.path.join(self.workdir, const.LOGGING_CONF)
        self.config['adit']['adit_log'] = self.logfile = os.path.join(self.workdir, 'log', const.ADIT_LOGFILE)
        self.config['adit']['weed_log'] = self.logfile = os.path.join(self.workdir, 'log', const.WEED_LOGFILE)
        self.config['adit']['dask_log'] = self.logfile = os.path.join(self.workdir, 'log', const.DASK_LOGFILE)
        self.config['adit']['dfs_engine'] = const.SUPPORTED_DFS_ENGINES[0]
        self.config['adit']['cluster_user'] = const.DEFAULT_CLUSTER_TOKEN
        self.config['adit']['cluster_pass'] = const.DEFAULT_CLUSTER_TOKEN

    def __init_with_file(self, config_file: str = None) -> None:
        self.config._interpolation = configparser.ExtendedInterpolation()
        self.config.read(config_file)

    def dump_config(self) -> None:
        with open(self.configfile, 'w') as configfile:
            self.config.write(configfile)

    def set(self, section: str, key: str, val: str) -> None:
        assert section is not None and section is not "", "section should never be None or empty"
        assert key is not None and key is not "", "key should never be None or empty"
        assert val is not None and val is not "", "val should never be None or empty"

        self.config[section][key] = val

    def get_str(self, section: str, key: str, default: str = None) -> Union[str, None]:
        assert section is not None and section is not "", "section should never be None or empty"
        assert key is not None and key is not "", "key should never be None or empty"

        if section not in self.config.sections():
            return default

        if key not in self.config[section]:
            return default

        return self.config[section][key]

    def get_int(self, section: str, key: str, default: int) -> Union[int, None]:
        res = self.get_str(section=section, key=key, default=None)
        if res is None:
            return default
        else:
            try:
                res = int(res)
                return res
            except Exception as ex:
                logging.error(f"wrong config type for {section}.{key}. Expected integer value instead.", ex)
                raise Exception(f"wrong config type for {section}.{key}. Expected integer value instead.")

    def get_bool(self, section: str, key: str, default: bool) -> bool:
        res = self.get_str(section=section, key=key, default=None)
        if res is None:
            return default
        else:
            try:
                res = bool(res)
                return res
            except Exception as ex:
                logging.error(f"wrong config type for {section}.{key}. Expected boolean value instead.", ex)
                raise Exception(f"wrong config type for {section}.{key}. Expected boolean value instead.")

    @classmethod
    def init(cls, config_file: str = None) -> None:
        cls._INSTANCE = Config(config_file)

    @classmethod
    def instance(cls) -> Config:
        if cls._INSTANCE is None:
            raise Exception(f"AditConfig instance have not been initialized. " +
                            f"Please call AditConfig.init() to init AditConfig first.")
        return cls._INSTANCE
