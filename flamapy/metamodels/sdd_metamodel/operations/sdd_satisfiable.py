from typing import cast

from flamapy.core.models import VariabilityModel
from flamapy.core.operations import Satisfiable
from flamapy.metamodels.sdd_metamodel.models import SDDModel


class SDDSatisfiable(Satisfiable):
    """Whether the feature model is satisfiable (non-void): the SDD is not the false node."""

    def __init__(self) -> None:
        self._result = False

    def is_satisfiable(self) -> bool:
        return self._result

    def get_result(self) -> bool:
        return self._result

    def execute(self, model: VariabilityModel) -> 'SDDSatisfiable':
        sdd_model = cast(SDDModel, model)
        self._result = not sdd_model.root.is_false()
        return self
