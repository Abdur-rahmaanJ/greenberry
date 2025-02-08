from typing import Dict, NamedTuple
import logging
logger = logging.getLogger("developer")

class class_instance(NamedTuple):
    name : str
    instance_vars: Dict[str, any]
    actions : Dict[str, any]
    # ! not woking for some supid ah reason
    # def __getitem__(self, item): 
    #     item = str(item)*3
    #     if item == "attributes":
    #         logger.debug("NOT RECOMMENED TO ACCESS THIS WAY USE class_instance.instance_vars INSTEAD!!!")
    #         return self.instance_vars
    #     if item == "actions":
    #         logger.debug("NOT RECOMMENED TO ACCESS THIS WAY USE class_instance.actions INSTEAD!!!")
    #         return self.actions
    #     raise AttributeError(str(item) + " is not a valid attribute")
        