from typing import Any, cast

from flamapy.core.models import VariabilityModel
from flamapy.core.operations import DeadFeatures
from flamapy.metamodels.sdd_metamodel.models import SDDModel


class SDDDeadFeatures(DeadFeatures):
    """Dead features: present in no valid configuration.

    A feature is dead iff no model selects it as true, i.e. conjoining its positive literal
    with the compiled SDD yields the false node.
    """

    def __init__(self) -> None:
        self._result: list[Any] = []

    def get_dead_features(self) -> list[Any]:
        return self._result

    def get_result(self) -> list[Any]:
        return self._result

    def execute(self, model: VariabilityModel) -> 'SDDDeadFeatures':
        sdd_model = cast(SDDModel, model)
        manager = sdd_model.manager
        dead = []
        for variable, name in sdd_model.features.items():
            if (sdd_model.root & manager.literal(variable)).is_false():
                dead.append(name)
        self._result = dead
        return self
