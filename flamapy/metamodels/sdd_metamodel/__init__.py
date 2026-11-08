from flamapy.core.manifest import OperationCapability, PluginManifest
from flamapy.core.models.language_level import LanguageLevel, MajorLevel, MinorLevel

# Costs are estimated milliseconds from the 2026-11-06 calibration (betty synthetic models at 1%
# and 30% constraint density plus JHipster and busybox; worst case of the two densities, never
# decreasing). Compilation depends on the constraint density far more than on the size: the
# sparse models compile in 0.3 s up to 2,000 features, the dense 500-feature one takes 7.5 s and
# the dense 1,000-feature one (like busybox, 1,108 features) does not finish in 5 minutes.
# Counting is then immediate (66 ms at 500 features), but core/dead features condition the SDD
# per variable: 41 s for core and more than 3 minutes for dead on the dense 500-feature model.
MANIFEST = PluginManifest(
    name='sdd',
    calibration='2026-11-06',
    extension='sdd',
    supported_level=LanguageLevel(MajorLevel.BOOLEAN, {MinorLevel.GROUP_CARDINALITY}),
    max_features=2000,
    transformation_cost_curve=((50, 3), (100, 5), (200, 10), (500, 7500), (1000, 300000)),
    operations={
        'satisfiable': OperationCapability(cost=1),
        'configurations_number': OperationCapability(cost_curve=((200, 1), (500, 66))),
        'core_features': OperationCapability(cost_curve=((100, 1), (200, 5), (500, 41000))),
        'dead_features': OperationCapability(cost_curve=((100, 1), (200, 4), (500, 180000))),
    },
)
