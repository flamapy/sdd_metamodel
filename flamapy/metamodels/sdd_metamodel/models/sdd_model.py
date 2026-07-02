from typing import Any, Optional

from flamapy.core.models import VariabilityModel


class SDDModel(VariabilityModel):
    """A Sentential Decision Diagram (SDD) representation of a feature model.

    An SDD is a knowledge-compilation form (a subset of d-DNNF, strictly more succinct than
    OBDD in cases) that supports exact, polytime queries: model counting, consistency and
    conditioning. It is built by compiling the feature model's CNF with the ``PySDD`` library.
    """

    @staticmethod
    def get_extension() -> str:
        return 'sdd'

    def __init__(self) -> None:
        self.manager: Any = None  # pysdd SddManager
        self.root: Any = None     # pysdd SddNode (the compiled formula)
        self.variables: dict[str, int] = {}  # feature name -> SDD variable index (1-based)
        self.features: dict[int, str] = {}    # SDD variable index -> feature name
        self.original_model: Optional[VariabilityModel] = None

    def feature_variables(self) -> list[int]:
        """SDD variable indices that correspond to features."""
        return list(self.features.keys())
