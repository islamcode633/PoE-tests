#!/usr/bin/env python3

"""
Client for testing a PoE chip
"""

import sys
from typing import List, Dict, Any
from time import sleep
from logging import Logger

from jrpc_client import get_client
from methods import PoEMethods
from parameters import PoEParameters
from common_const import Consts


PORTS: tuple = (
    '1/1', '1/2', '1/3',
    '1/4', '1/5', '1/6',
    '1/7', '1/8'
)


class PoEEnableError(Exception):
    """ Error activating the poe function """

class ErrorSetPowerLimit(Exception):
    """ Error setting power limit """

class ErrorDisablePort(Exception):
    """ Failed to disable port ! """


def pre_config(
        client,
        method: PoEMethods,
        params: PoEParameters
    ) -> None:
    """ Setup stage """
    try:
        # Activate PoE function
        result: Any = client.request(method.SET_POE_ENABLE, params.poe_enable(flag=True))
        if not result is None:
            raise PoEEnableError
        # Set a power limit
        result: Any = client.request(method.SET_POWER_LIMIT, params.power_limit(power=Consts.POWER_LIMIT))
        if not result is None:
            raise ErrorSetPowerLimit
        # disable all ports
        for port in PORTS:
            result: Any = client.request(method.SET_CHANGE_PORT_STATE, params.change_port_state(port=port, state='disable'))
            if result is None:
                print(f'{port}: disable')
                continue
            raise ErrorDisablePort
    except PoEEnableError:
        sys.exit('Failed to activate PoE function !')
    except ErrorSetPowerLimit:
        sys.exit(f'Failed to set power to {Consts.POWER_LIMIT} !')
    except ErrorDisablePort:
        sys.exit(f'Failed to disable port {port} !')


def get_ports_map() -> None:
    """ Returns a list of ports on which PoE is enabled """


def errors_counting(ports: List[str]) -> str:
    """ Counts the number of errors for each port """
    res: str = ""
    for uport in sorted(set(ports)):
        frequent: int = 0
        for port in ports:
            if uport == port:
                frequent += 1
        res += f'{uport[-1]}({frequent}) '
    return res

def processing_result(failed: int, success: int, names_failed_ports: str) -> Dict[str, str | int | bool]:
    """ Test data processing """
    result: Dict[str, str | int | bool] = {
        'success': success, 'failed': failed,
        'port': "", 'result': True
    }
    if failed:
        result.update({'result': False})
        result.update({'port': errors_counting(names_failed_ports.strip().split())})
    return result

def test_sequential_activation(
        client,
        method: PoEMethods,
        params: PoEParameters
    ) -> Dict[str, str | int | bool]:
    """ Seq on/off PoE channels """
    names_failed_ports: str = ''
    success: int = 0
    failed: int = 0
    for port in PORTS:
        client.request(method.SET_CHANGE_PORT_STATE, params.change_port_state(port=port, state='enable'))
        sleep(Consts.PAUSE_EXECUTION)
        current_power: float = float(client.request(
            method.GET_PORT_CONSUMPTION,
            params.gigabyte_port(port=port)
        )['Power'])
        if Consts.MINIMAL_POWER < current_power:
            success += 1
            print(f"<UI> {port}: {'%.1f'}W [ OK ]" % current_power)
            continue
        print(f"<UI> {port}: {'%.1f'}W [ Failed ]" % current_power)
        failed += 1
        names_failed_ports += port + " "
    return processing_result(failed, success, names_failed_ports)


if __name__ == '__main__':
    # point enter
    poe_client = get_client()
    poe_method: PoEMethods = PoEMethods()
    poe_params: PoEParameters = PoEParameters()
    pre_config(client=poe_client, method=poe_method, params=poe_params)
    test: Dict[str, str | int | bool] = test_sequential_activation(client=poe_client, method=poe_method, params=poe_params)
    if test['result']:
        print('TEST OK ')
        sys.exit(0)
    print(f"TEST ERR: Port: {test['port']} Failed: {test['failed']}")
    sys.exit(1)


# swap logger for print
# add calcl ports map
