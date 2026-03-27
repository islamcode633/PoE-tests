"""
Contains all the methods described
 in the specification JSON RPC v1.0
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class PoEMethods:
    """ ... """
    # operation GET
    get_power_total = "poe.power.total.get"
    get_power_parameters = "poe.power.parameters.get"
    get_power_limit = "poe.power.limit.get"
    get_device_status = "poe.device.status.get"
    get_port_params = "poe.port.parameters.get"
    get_error_counters = "poe.port.counters.get"
    get_port_class = "poe.port.class.get"
    get_poe_version = "poe.version.get"
    get_info_class_power = "poe.power.class.info.get"
    get_port_measurements = "poe.port.measurements.get"
    get_port_consumption = "poe.port.status.get" # [f"Gi {port}"] -> resp['result']['Power']

    # operation SET
    set_poe_enable = "poe_enable.set"
    set_power_limit = "poe.power.limit.set"
    set_change_port_state = "poe.port.enable.mode.set" # [f"Gi {port}", {"Mode": f"{mode.lower()}"}]
