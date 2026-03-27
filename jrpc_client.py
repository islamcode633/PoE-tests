"""
Shared user library
"""

from typing import List
from enum import Enum
from json import loads, dumps

from excepts_poe import (
    AuthException,
    InitErrorException
)

class Constans(Enum):
    """ ... """
    # using all tests
    LOGGIN_URL = 'http://192.168.127.253/login'
    JSON_RPC = 'http://192.168.127.253/json_rpc'
    HEADER = {"Content-Type": "application/json"}
    USER = 'admin:password'

    # using only PoE test
    POWER_LIMIT = 120
    MINIMAL_POWER = 2.0
    PAUSE_EXECUTION = 3
    PAUSE_BETWEEN_OUT = 1


class JsonRpcRequest:
    """ ... """
    def __init__(self, session) -> None:
        self._session = session

    def _post(self, method = None, timeout = 15):
        """ Wrapper for sending a POST request """
        return self._session.post(
            url=Constans.JSON_RPC.value,
            headers=Constans.HEADER.value,
            data=dumps(method),
            timeout=timeout
        )

    def request(self, method = None, params = None):
        """ ... """
        if not method:
            raise InitErrorException("Parameter [ method ] Not Init valid value !")
        if not params:
            params = []
        response = self._post(method={
            "id": "1",
            "method": f"{method}",
            "params": params}
        )
        r = loads(response.text)['result']
        return r is None


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

def create_session(session):
    """ Auth on Switch """
    res_code = session.post(
        url=Constans.LOGGIN_URL.value,
        headers=Constans.HEADER.value,
        data=Constans.USER.value
    ).status_code
    if not res_code == 200:
        raise AuthException('Authorization error on the switch !')
    # Session object with Cookie field after success auth
    return session
