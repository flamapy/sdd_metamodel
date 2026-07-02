# flamapy-sdd

`flamapy-sdd` is a [flamapy](https://flamapy.github.io) plugin that compiles a feature model
into a **Sentential Decision Diagram (SDD)** for exact analysis.

SDD is a knowledge-compilation language (a subset of d-DNNF, strictly more succinct than OBDD
in cases), so it supports exact, polytime queries — model counting, consistency, conditioning —
and can stay compact on models where a BDD blows up. It complements the ecosystem:

- `flamapy-bdd` compiles to OBDD (exact, but can explode on large models).
- `flamapy-sharpsat` gives an *approximate* count (ApproxMC) for very large models.
- `flamapy-sdd` gives an **exact** count via a more succinct compilation, on top of the SAT CNF.

It uses [PySDD](https://github.com/wannesm/PySDD).

## Installation

```
pip install flamapy-sdd
```

## Operations

| Operation | Class |
|---|---|
| Exact number of configurations | `SDDConfigurationsNumber` |
| Satisfiable (non-void) | `SDDSatisfiable` |
| Core features | `SDDCoreFeatures` |
| Dead features | `SDDDeadFeatures` |

## Usage

```python
from flamapy.metamodels.fm_metamodel.transformations import UVLReader
from flamapy.metamodels.sdd_metamodel.transformations import FmToSDD
from flamapy.metamodels.sdd_metamodel.operations import SDDConfigurationsNumber

fm = UVLReader('model.uvl').transform()
sdd_model = FmToSDD(fm).transform()
count = SDDConfigurationsNumber().execute(sdd_model).get_result()
```

## License

GPL-3.0-or-later.
