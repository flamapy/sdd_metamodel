from flamapy.core.manifest import PluginManifest, OperationCapability
from flamapy.core.models.language_level import LanguageLevel, MajorLevel

# Costs from the 2.8 calibration run (2026-07-09): SDD compilation scaled the best of the
# exact backends (counting 0.9ms at 500 features; no ceiling observed on the corpus).
MANIFEST = PluginManifest(
    name='sdd',
    extension='sdd',
    supported_level=LanguageLevel(MajorLevel.BOOLEAN, set()),
    operations={
        'satisfiable': OperationCapability(cost=90),
        'configurations_number': OperationCapability(cost=40),
    },
)
