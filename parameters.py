"""
Contains params for requests
"""

from typing import List, Dict
from dataclasses import dataclass

PortIdentifier = str


@dataclass
class PoEParameters:
    """ Returns the data structures needed to execute a specific query """

    def poe_enable(self, flag: bool) -> List[bool]:
        """ Activate/Deactivate poe function """
        if isinstance(flag, bool):
            return [flag]
        raise TypeError('Error: flag must be of type: [ bool ]') from None

    def power_limit(self, power: int) -> List[str]:
        """ Set power from parameter """
        if power < 0:
            raise ValueError('Error Param: power limit not be negative number !') from None
        return [f'{power}']

    def change_port_state(
            self,
            port: PortIdentifier,
            state: str
        ) -> List[PortIdentifier | Dict[str, str]]:
        """ Change state port [Enabled | Disabled] """
        state = state.lower()
        if state in {'enable', 'disable'}:
            return [f"Gi {port}", {"Mode": f"{state}"}]
        raise ValueError('Error: Ports state can be [ enable ] or [ disable ] !') from None

    def gigabyte_port(self, port: PortIdentifier) -> List[PortIdentifier]:
        """ Returns the port identifier """
        return [f"Gi {port}"]
