from __future__ import annotations

from adit.config import Config
from typing import Union
import inspect

__all__ = ['CheckPointController']


class CheckPointController:
    _INSTANCE = None
    _CONFIG_SECTION = "adit"
    _ENGINE = Config.instance().get_str(_CONFIG_SECTION, "checkpoint_engine", "etcd")
    _CHECKPOINT_LOCAL_FILE = Config.instance().get_str(_CONFIG_SECTION, "checkpoint_file", "checkpoint")

    @classmethod
    def instance(cls):
        if cls._INSTANCE is None:
            instance_cls = globals().get(cls._ENGINE + "_CheckPoint")
            assert inspect.isclass(instance_cls), "The given checkpoint engine is unknown."
            cls._INSTANCE = instance_cls()

        return cls._INSTANCE
