"""
...
"""

from enum import Enum


class Consts(str, Enum):
    """ 
    Common constans for all tests

    :loggin_url: ...
    """
    # using all tests
    LOGGIN_URL = 'http://192.168.127.253/login'
    JSON_RPC = 'http://192.168.127.253/json_rpc'
    USER = 'admin:password'

    # using only PoE test
    POWER_LIMIT = 120
    MINIMAL_POWER = 2.0
    PAUSE_EXECUTION = 3
    PAUSE_BETWEEN_OUT = 1


# dockstring all const
