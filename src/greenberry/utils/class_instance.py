from typing import Dict, NamedTuple
import logging
logger = logging.getLogger("developer")

class class_instance(NamedTuple):
    name : str
    instance_vars: Dict[str, any]
    actions : Dict[str, any]
    def __getitem__(self, item):
        if item == "attributes":
            logger.debug("NOT RECOMMENED TO ACCESS THIS WAY USE class_instance.instance_vars INSTEAD!!!")
            return self.instance_vars
        if item == "actions":
            logger.debug("NOT RECOMMENED TO ACCESS THIS WAY USE class_instance.actions INSTEAD!!!")
        