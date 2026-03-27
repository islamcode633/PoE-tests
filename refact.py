#!/usr/bin/env python3

"""
...
"""

import sys
#from time import sleep
from requests import Session

from jrpc_client import JsonRpcRequest, Constans, create_session
from excepts_poe import (
    EnablePoeException,
    SetPowerLimitException,
)
from json_rpc_methods import PoEMethods


LOGGIN_URL: str = Constans.LOGGIN_URL.value
JSON_RPC: str = Constans.JSON_RPC.value
HEADER: dict[str, str] = Constans.HEADER.value
USER: str = Constans.USER.value
POWER_LIMIT: int = Constans.POWER_LIMIT.value
MINIMAL_POWER: float = Constans.MINIMAL_POWER.value
PAUSE_EXECUTION: int = Constans.PAUSE_EXECUTION.value
PAUSE_BETWEEN_OUT: int = Constans.PAUSE_BETWEEN_OUT.value

PORTS: tuple = (
    '1/1', '1/2', '1/3',
    '1/4', '1/5', '1/6',
    '1/7', '1/8'
)


if __name__ == '__main__':
    try:
        with create_session(session=Session()) as _session:
            client = JsonRpcRequest(session=_session)
            method = PoEMethods()

            if not client.request(method.set_poe_enable, params=[True]):
                raise EnablePoeException
            if not client.request(method.set_power_limit, params=[f'{120}']):
                raise SetPowerLimitException

            #client = PoeClient(session=_session)
            #print(client.get_port_consumption(port='1/1'))
            #print(client.change_port_state(port='1/1', mode='ENABLE'))
    except EnablePoeException:
        sys.exit('Failed to activate PoE function !')
    except SetPowerLimitException:
        sys.exit(f'Failed to set power to {POWER_LIMIT} !')
    except Exception:
        sys.exit(1)



# def test_sequential_activation_of_channels():
#     """ Seq on/off poe channels """
#     pass

# add calcl ports map
# add more exceptions
# add singleton pattern
# add logger

# doc string + comment params + typing
