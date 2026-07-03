"""Tests for the SDD metamodel: exact counting, satisfiability, core/dead features.

Oracles are computed by brute-forcing the CNF from fm_metamodel's solver-agnostic ClauseSet,
so CI needs no SAT plugin — only flamapy-fm, which is already a declared dependency.
"""
import os
import tempfile
from itertools import product

from flamapy.metamodels.fm_metamodel.transformations import UVLReader
from flamapy.metamodels.fm_metamodel.models import FeatureModel, ClauseSet
from flamapy.metamodels.sdd_metamodel.transformations import FmToSDD
from flamapy.metamodels.sdd_metamodel.operations import (
    SDDConfigurationsNumber,
    SDDSatisfiable,
    SDDCoreFeatures,
    SDDDeadFeatures,
)


def _valid_configs(fm: FeatureModel) -> tuple:
    """(valid configurations as frozensets of selected names, all feature names)."""
    clause_set = ClauseSet.from_feature_model(fm)
    name_of = {vid: name for name, vid in clause_set.variables.items()}
    var_ids = sorted({abs(lit) for clause in clause_set.clauses for lit in clause}
                     | set(clause_set.variables.values()))
    configs = set()
    for bits in product((False, True), repeat=len(var_ids)):
        assignment = dict(zip(var_ids, bits))
        if all(any((lit > 0) == assignment[abs(lit)] for lit in clause)
               for clause in clause_set.clauses):
            configs.add(frozenset(name_of[v] for v in var_ids if assignment[v] and v in name_of))
    return configs, set(clause_set.variables)


def _exact_count(fm: FeatureModel) -> int:
    return len(_valid_configs(fm)[0])


def _core_features(fm: FeatureModel) -> set:
    configs, names = _valid_configs(fm)
    return {name for name in names if configs and all(name in cfg for cfg in configs)}


def _dead_features(fm: FeatureModel) -> set:
    configs, names = _valid_configs(fm)
    return names - (set().union(*configs) if configs else set())

_UVL = """features
    Root {abstract}
        mandatory
            Base
        optional
            A
            B
            C
constraints
    A => B
    A | B
"""

_UNSAT_UVL = """features
    Root {abstract}
        mandatory
            A
constraints
    !A
"""


def _fm(uvl):
    handle, path = tempfile.mkstemp(suffix='.uvl')
    try:
        with os.fdopen(handle, 'w') as file:
            file.write(uvl)
        return UVLReader(path).transform()
    finally:
        os.remove(path)


def test_count_matches_sat_enumeration():
    fm = _fm(_UVL)
    exact = _exact_count(fm)
    sdd = SDDConfigurationsNumber().execute(FmToSDD(fm).transform()).get_result()
    assert sdd == exact


def test_satisfiable():
    assert SDDSatisfiable().execute(FmToSDD(_fm(_UVL)).transform()).get_result() is True


def test_unsatisfiable_model():
    assert SDDSatisfiable().execute(FmToSDD(_fm(_UNSAT_UVL)).transform()).get_result() is False


def test_core_features_match_sat():
    fm = _fm(_UVL)
    expected = _core_features(fm)
    sdd = set(SDDCoreFeatures().execute(FmToSDD(fm).transform()).get_result())
    assert sdd == expected
    assert 'Base' in sdd and 'Root' in sdd  # mandatory chain is core


def test_dead_features_match_sat():
    fm = _fm(_UVL)
    expected = _dead_features(fm)
    sdd = set(SDDDeadFeatures().execute(FmToSDD(fm).transform()).get_result())
    assert sdd == expected  # no dead features in this model
