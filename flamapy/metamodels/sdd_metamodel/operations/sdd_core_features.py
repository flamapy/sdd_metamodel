from typing import Any, cast

from flamapy.core.models import VariabilityModel
from flamapy.core.operations import CoreFeatures
from flamapy.metamodels.sdd_metamodel.models import SDDModel


class SDDCoreFeatures(CoreFeatures):
    """Core features: present in every valid configuration.

    A feature is core iff no model selects it as false, i.e. conjoining its negative literal
    with the compiled SDD yields the false node.
    """

    def __init__(self) -> None:
        self._result: list[Any] = []

    def get_core_features(self) -> list[Any]:
        return self._result

    def get_result(self) -> list[Any]:
        return self._result

    def execute(self, model: VariabilityModel) -> 'SDDCoreFeatures':
        sdd_model = cast(SDDModel, model)
        manager = sdd_model.manager
        core = []
        for variable, name in sdd_model.features.items():
            if (sdd_model.root & manager.literal(-variable)).is_false():
                core.append(name)
        self._result = core
        return self
