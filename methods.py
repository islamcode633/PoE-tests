"""
Contains methods
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class PoEMethods:
    """ Contains the methods needed to perform Get/Set requests """
    GET_POWER_TOTAL       = "poe.power.total.get"
    GET_POWER_PARAMETERS  = "poe.power.parameters.get"
    GET_POWER_LIMIT       = "poe.power.limit.get"
    GET_DEVICE_STATUS     = "poe.device.status.get"
    GET_PORT_PARAMS       = "poe.port.parameters.get"
    GET_ERROR_COUNTERS    = "poe.port.counters.get"
    GET_PORT_CLASS        = "poe.port.class.get"
    GET_POE_VERSION       = "poe.version.get"
    GET_INFO_CLASS_POWER  = "poe.power.class.info.get"
    GET_PORT_MEASUREMENTS = "poe.port.measurements.get"
    GET_PORT_CONSUMPTION  = "poe.port.status.get"        # Gi {port} -> resp['result']['Power']

    SET_POE_ENABLE        = "poe_enable.set"
    SET_POWER_LIMIT       = "poe.power.limit.set"
    SET_CHANGE_PORT_STATE = "poe.port.enable.mode.set"   # Gi {port} , {"Mode": "enabled"}


# dockstring all const
