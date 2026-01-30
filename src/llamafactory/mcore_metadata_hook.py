"""
Runtime hook that guarantees that *any* import of
torch.distributed.checkpoint.metadata exposes `.mcore_data`
as an alias for `.storage_data`.

Safe to leave in production – if the attribute already exists we do
nothing.
"""
import importlib
import sys
from types import ModuleType

_TARGET = "torch.distributed.checkpoint.metadata"


def _patch(module: ModuleType):
    """Idempotently add the alias to the Metadata class inside *module*."""
    Meta = getattr(module, "Metadata", None)
    if Meta is None:  # very old torch – nothing to do
        return
    if not hasattr(Meta, "mcore_data") and hasattr(Meta, "storage_data"):
        setattr(Meta, "mcore_data", property(lambda self: self.storage_data))


class _Finder(importlib.abc.MetaPathFinder):
    """Intercept *every* import of the target module."""

    def find_spec(self, fullname, path, target=None):
        if fullname == _TARGET:
            # Let Python do the real import first, then patch in Loader.exec_module
            return importlib.machinery.ModuleSpec(
                fullname, _Loader(), is_package=False
            )
        return None


class _Loader(importlib.abc.Loader):
    def create_module(self, spec):  # use default machinery
        return None

    def exec_module(self, module):
        # Real import (will fill the module’s namespace)
        real_module = importlib.import_module(module.__name__)
        module.__dict__.update(real_module.__dict__)
        # And now patch it
        _patch(module)


# ------------------------------------------------------------------
# Register the hook and patch the module if it is already imported.
# ------------------------------------------------------------------
sys.meta_path.insert(0, _Finder())
if _TARGET in sys.modules:
    _patch(sys.modules[_TARGET])
print("[Shim] Metadata import hook installed (mcore_data ↔ storage_data)")