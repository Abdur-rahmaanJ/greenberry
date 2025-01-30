from typing import Dict, NamedTuple


class class_instance(NamedTuple):
    name : str
    instance_vars: Dict[str, any]
    