from typing import cast

from flamapy.core.models import VariabilityModel
from flamapy.core.operations import ConfigurationsNumber
from flamapy.metamodels.sdd_metamodel.models import SDDModel


class SDDConfigurationsNumber(ConfigurationsNumber):
    """Exact number of valid configurations, via SDD model counting.

    Model counting is a polytime query on the compiled SDD, so this is exact and — for models
    whose SDD stays compact — scales to cases where explicit enumeration does not.
    """

    def __init__(self) -> None:
        self._result = 0

    def get_configurations_number(self) -> int:
        return self._result

    def get_result(self) -> int:
        return self._result

    def execute(self, model: VariabilityModel) -> 'SDDConfigurationsNumber':
        sdd_model = cast(SDDModel, model)
        # global_model_count counts over every declared variable; SddNode.model_count only
        # counts over the variables the node locally depends on (its own vtree context).
        self._result = int(sdd_model.manager.global_model_count(sdd_model.root))
        return self
