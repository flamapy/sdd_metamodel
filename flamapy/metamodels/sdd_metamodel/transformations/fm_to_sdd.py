from pysdd.sdd import SddManager, Vtree

from flamapy.core.transformations import ModelToModel
from flamapy.metamodels.fm_metamodel.models import FeatureModel, ClauseSet
from flamapy.metamodels.sdd_metamodel.models import SDDModel


class FmToSDD(ModelToModel):
    """Transform a feature model into an SDD by compiling its CNF with PySDD.

    The CNF is produced by the feature-model ``ClauseSet`` (no SAT-solver dependency), then
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
        clause_set = ClauseSet.from_feature_model(self.source_model, cnf_method=self.cnf_method)
        clauses = [list(clause) for clause in clause_set.clauses]
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
        model.variables = dict(clause_set.variables)
        model.features = dict(clause_set.features)
        model.original_model = self.source_model
        return model
