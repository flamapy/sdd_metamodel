from pysdd.sdd import SddManager, Vtree

from flamapy.core.transformations import ModelToModel
from flamapy.metamodels.fm_metamodel.models import FeatureModel
from flamapy.metamodels.pysat_metamodel.transformations import FmToPysat
from flamapy.metamodels.sdd_metamodel.models import SDDModel


class FmToSDD(ModelToModel):
    """Transform a feature model into an SDD by compiling its CNF with PySDD.

    The CNF is produced by reusing the SAT metamodel's ``FmToPysat`` transformation, then
    conjoined clause by clause into an SDD over a balanced vtree.
    """

    @staticmethod
    def get_source_extension() -> str:
        return 'fm'

    @staticmethod
    def get_destination_extension() -> str:
        return 'sdd'

    def __init__(self, source_model: FeatureModel, cnf_method: str = 'distributive') -> None:
        self.source_model = source_model
        self.cnf_method = cnf_method
        self.destination_model = SDDModel()

    def transform(self) -> SDDModel:
        # Only pass cnf_method for a non-default encoding, so the plugin also works against
        # releases of flamapy-sat that predate the Tseytin cnf_method option.
        if self.cnf_method == 'distributive':
            sat_model = FmToPysat(self.source_model).transform()
        else:
            sat_model = FmToPysat(self.source_model, cnf_method=self.cnf_method).transform()

        clauses = [list(clause) for clause in sat_model.get_all_clauses().clauses]
        var_count = max((abs(literal) for clause in clauses for literal in clause), default=1)

        vtree = Vtree(var_count=var_count, vtree_type='balanced')
        manager = SddManager.from_vtree(vtree)
        root = manager.true()
        for clause in clauses:
            clause_node = manager.false()
            for literal in clause:
                clause_node = clause_node | manager.literal(literal)
            root = root & clause_node

        model = self.destination_model
        model.manager = manager
        model.root = root
        model.variables = dict(sat_model.variables)
        model.features = dict(sat_model.features)
        model.original_model = self.source_model
        return model
