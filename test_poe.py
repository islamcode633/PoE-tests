#!/usr/bin/env python3

"""
Simple client for testing a PoE chip
"""

from typing import Optional, List, Dict, Any
import re
import sys
from dataclasses import dataclass
from json import dumps, loads
from time import sleep

from requests import (
    Session,
    Response
)

MINIMAL_POWER: int = 3
PAUSE: int = 3
PORTS: tuple = (
    '1/1', '1/2', '1/3',
    '1/4', '1/5', '1/6',
    '1/7', '1/8'
)
POWER_LIMIT: int = 120


# def wrapp_calc_curr_time() -> Callable[[], int]:
#     """ Freeze the primary timestamp """
#     primary_timestamp: int = int(time())
#     def calculate_current_time() -> int:
#         """ Calculating the current time """
#         current_time: int = int(time())
#         return current_time - primary_timestamp
#     return calculate_current_time

# def take_pause() -> None:
#     """ Freeze terminal output for N seconds """
#     if TIME_UNTIL_NEXT_SURVEY:
#         for sec in range(1, TIME_UNTIL_NEXT_SURVEY + 1):
#             rprint(f'next launch in {TIME_UNTIL_NEXT_SURVEY - sec}', end='\r')
#             sleep(1)

# def activate_all_channels() -> None:
#     """ Execute PoE test """
#     calculate_current_time: Callable[[], int] = wrapp_calc_curr_time()
#     while calculate_current_time() <= TEST_EXEC_TIME:
#         try:
#             for index_port, status in enumerate(show_ports_status()):
#                 if status == 'enabled':
#                     rprint(f'Port: [blue]{PORTS[index_port]}[/blue] -> \
#                            {show_consum_on_port(port=PORTS[index_port])} [W]')
#                     continue
#                 sleep(PAUSE)
#                 rprint(f'Port: [blue]{PORTS[index_port]}[/blue] -> {status}')
#             take_pause()
#         except KeyboardInterrupt:
#             sys.exit('\nInterrupt script execution\n')

class AuthException(Exception):
    """ Failed to log in """

class EnablePoeException(Exception):
    """ Error activating the poe function """

class SetPowerLimitException(Exception):
    """ Error setting power limit """


@dataclass
class FlatStructParser:
    """ Unpacking a dictionary of type {id:'',method:'',error:'',result:} """
    id: int = 0
    method: str = ""
    error: Optional[str] = ""
    result: Optional[str] = ""

class GeneralRequests:
    """ General necessary requests """

    def __init__(self) -> None:
        self.common_url: str = 'http://192.168.127.253/json_rpc'
        with Session() as session:
            self._session = session

    def auth(self) -> int:
        """ Auth on Switch """
        login: str = 'http://192.168.127.253/login'
        user: str = 'admin:password'
        return self._post(url=login, data=user).status_code

    def _post(self,
            url: str,
            data: str,
            headers: Dict[str, str] = {"Content-Type": "application/json"},
            timeout: int = 15
        ) -> Response:
        """ Wrapper over the Session.post method """
        return self._session.post(url=url, headers=headers, data=data, timeout=timeout)

    def _perform_action(self, method) -> Optional[Any]:
        """ Execute context """
        response = FlatStructParser(**loads(self._post(url=self.common_url, data=dumps(method)).text))
        if response.error is None:
            return response.result
        return response.error

    def _get_method(self, method: str, port: str = "", mode: str = "") -> Dict[str, str | List[str]] | None:
        """ Methods required to fulfill the request """
        methods: Dict[str, Dict[str, str | List]] = {
            'poe_enable': {"id": "1", "method": "poe_enable.set", "params": ["true"]},
            'status_port': {"id": "1", "method": "poe.port.status.get", "params": [f"Gi {port}"]},
            'enable_mode': {"id": "1", "method": "poe.port.enable.mode.set",
                            "params": [f"Gi {port}", {"Mode": f"{mode}"}]},
            'power_limit': {"id": "1", "method": "poe.power.limit.set",
                            "params": [f"{POWER_LIMIT}"]}
        }
        if method in methods:
            return methods[method]
        return None


class PoeRequests(GeneralRequests):
    """ Public api requests """

    def poe_enable(self) -> Optional[str]:
        """ Activate function PoE """
        return self._perform_action(method=self._get_method(method='poe_enable'))

    def get_power_consumption(self, port="") -> Optional[str]:
        """ Port energy consumption data """
        response = self._perform_action(method=self._get_method(method='status_port', port=port))
        if response:
            return f"{port} {response['Power']}"
        return None

    def disable(self, port) -> Optional[str]:
        """ Disabled the specified port """
        method = self._get_method(method='enable_mode', port=port, mode='disable')
        if self._perform_action(method=method) is None:
            return 'disabled'
        return None

    def enable(self, port) -> Optional[str]:
        """ Enables the specified port """
        method = self._get_method(method='enable_mode', port=port, mode='enable')
        return self._perform_action(method=method)

    def set_power_limit(self) -> Optional[str]:
        """ Set the specified power """
        return self._perform_action(method=self._get_method(method='power_limit'))

    def free_up_system_resources(self) -> None:
        """ Freeing up system resources """
        self._session.close()


def pre_config(request: PoeRequests) -> None:
    """ Config step """
    if request.auth() != 200:
        raise AuthException('Authorization error on the switch')
    #TODO fix problem with activate poe funct
    #if request.poe_enable() is not None:
    #    raise EnablePoeException('Failed to activate the POE Function')
    #print('Poe Enabled')
    if request.set_power_limit() is not None:
        raise SetPowerLimitException('Failed to Set Maximum Power')

    for port in PORTS:
        print(f'<UI>{port}: {request.disable(port)}')


def test_sequential_activation_of_channels(request: PoeRequests) -> None:
    """ Seq on/off poe channels """
    pre_config(request=request)
    regex: str = r"(\d+)[.]"
    success: int = 0
    failed: int = 0
    for port in PORTS:
        request.enable(port=port)
        sleep(PAUSE)
        current_power: Optional[str] = request.get_power_consumption(port=port)
        if isinstance(current_power, str):
            current_power = current_power.split()[1]
        else:
            continue
        match: Optional[re.Match[str]] = re.search(regex, current_power)
        if match:
            if MINIMAL_POWER < int(current_power := match.group(1)):
                print(f'<UI>{port}: {current_power}W [ OK ]')
                success += 1
                sleep(PAUSE)
                request.disable(port)
                continue
            print(f'<UI>{port}: {current_power}W [ Failed ]')
            failed += 1
    print(f'<UI>Success: {success} \n<UI>Failed: {failed}')

try:
    _request = PoeRequests()
    test_sequential_activation_of_channels(request=_request)
except (AuthException, EnablePoeException, SetPowerLimitException) as e:
    sys.exit(f'{e.args}')
finally:
    _request.free_up_system_resources()
