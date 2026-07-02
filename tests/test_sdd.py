"""Tests for the SDD metamodel: exact counting, satisfiability, core/dead features.

Oracles come from the SAT backend (a declared dependency) so CI needs no extra plugin.
"""
import os
import tempfile

from flamapy.metamodels.fm_metamodel.transformations import UVLReader
from flamapy.metamodels.sdd_metamodel.transformations import FmToSDD
from flamapy.metamodels.sdd_metamodel.operations import (
    SDDConfigurationsNumber,
    SDDSatisfiable,
    SDDCoreFeatures,
    SDDDeadFeatures,
)
from flamapy.metamodels.pysat_metamodel.transformations import FmToPysat
from flamapy.metamodels.pysat_metamodel.operations.pysat_configurations_number import (
    PySATConfigurationsNumber,
)
from flamapy.metamodels.pysat_metamodel.operations.pysat_core_features import PySATCoreFeatures
from flamapy.metamodels.pysat_metamodel.operations.pysat_dead_features import PySATDeadFeatures

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
    exact = PySATConfigurationsNumber().execute(FmToPysat(fm).transform()).get_result()
    sdd = SDDConfigurationsNumber().execute(FmToSDD(fm).transform()).get_result()
    assert sdd == exact


def test_satisfiable():
    assert SDDSatisfiable().execute(FmToSDD(_fm(_UVL)).transform()).get_result() is True


def test_unsatisfiable_model():
    assert SDDSatisfiable().execute(FmToSDD(_fm(_UNSAT_UVL)).transform()).get_result() is False


def test_core_features_match_sat():
    fm = _fm(_UVL)
    sat = set(PySATCoreFeatures().execute(FmToPysat(fm).transform()).get_result())
    sdd = set(SDDCoreFeatures().execute(FmToSDD(fm).transform()).get_result())
    assert sdd == sat
    assert 'Base' in sdd and 'Root' in sdd  # mandatory chain is core


def test_dead_features_match_sat():
    fm = _fm(_UVL)
    sat = set(PySATDeadFeatures().execute(FmToPysat(fm).transform()).get_result())
    sdd = set(SDDDeadFeatures().execute(FmToSDD(fm).transform()).get_result())
    assert sdd == sat  # no dead features in this model
