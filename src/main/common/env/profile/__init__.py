from .base_profile_config import BaseProfileConfig
from typing import Type

from common.env.profile.dev_profile_config import DevProfileConfig
from common.env.profile.prod_profile_config import ProdProfileConfig
from common.env.profile.test_profile_config import TestProfileConfig

PROFILE_CLASS_MAP:dict[str, Type[BaseProfileConfig]] = {
    "dev": DevProfileConfig,
    "prod": ProdProfileConfig,
    "test": TestProfileConfig
}