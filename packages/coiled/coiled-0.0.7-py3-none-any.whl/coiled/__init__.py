from .core import Cloud
from .cluster import CoiledCluster, Cluster

from . import config

del config

from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions
