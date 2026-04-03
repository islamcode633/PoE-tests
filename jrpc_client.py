"""
Library for sending requests via json-rpc v1.0
"""

from typing import Dict, Any
from json import loads, dumps
from requests import Session, Response
from logging import Logger

from common_const import Consts


class AuthException(Exception):
    """ Failed to log in """

class InitErrorException(Exception):
    """ Error initializing required parameters """


class BaseRpcRequest:
    """ ... """
    def __init__(
            self,
            session: Session,
            json_rpc: str = Consts.JSON_RPC,
        ) -> None:
        self._session = session
        self._json_rpc = json_rpc

    def _post(
            self,
            payload: Dict[str, Any] | None = None,
            timeout: int = 15
        ) -> Response:
        """ Wrapper for sending a POST request """
        response = self._session.post(
            url=self._json_rpc,
            data=dumps(payload),
            timeout=timeout
        )
        response.raise_for_status()
        return response

    def request(
            self,
            method: str = "",
            params: Any = None
        ) -> Any:
        """ Public api for post queries """
        if not method:
            raise InitErrorException("Parameter [ method ] Not Init valid value !")
        payload: Dict[str, Any] = {
            "id": "1",
            "method": f"{method}",
            "params": params or []
        }
        response: Response = self._post(payload=payload)
        result: Any = loads(response.text)['result']
        return result

def _create_session(
        session: Session = Session(),
        loggin_url: str = Consts.LOGGIN_URL,
        user: str = Consts.USER
    ) -> Session:
    """ returns a Session object """
    res_code: int = session.post(
        url=loggin_url,
        data=user
    ).status_code
    if res_code == 200:
        # Session object with Cookie field after success auth
        return session
    raise AuthException('Authorization error on the switch !')


def get_client():
    """ return Client to perform RPC requests """
    session = _create_session()
    return BaseRpcRequest(session=session)


# add comments
# add loggin
# add simple unittests
# add annotations
