from flamapy.core.manifest import PluginManifest
from flamapy.core.models.language_level import LanguageLevel, MajorLevel

MANIFEST = PluginManifest(
    name='sdd',
    extension='sdd',
    supported_level=LanguageLevel(MajorLevel.BOOLEAN, set()),
)
