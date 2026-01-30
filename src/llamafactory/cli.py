# Copyright 2025 the LlamaFactory team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# def _patch_tdc_metadata():
#     try:
#         import torch.distributed.checkpoint.metadata as _tdc_meta
#     except ModuleNotFoundError:
#         print("[Shim] torch.distributed.checkpoint.metadata missing")
#         return

#     Meta = getattr(_tdc_meta, "Metadata", None)
#     if Meta is None:
#         print("[Shim] No Metadata class in TDC – nothing to patch")
#         return

#     if hasattr(Meta, "mcore_data"):
#         print("[Shim] Metadata already has mcore_data – nothing to do")
#     elif hasattr(Meta, "storage_data"):
#         # add read-only alias
#         Meta.mcore_data = property(lambda self: self.storage_data)
#         print("[Shim] Added Metadata.mcore_data alias → storage_data")
#     else:
#         print("[Shim] Metadata class has neither storage_data nor mcore_data")

# print("Patching up Metadata.mcore_data error")

# _patch_tdc_metadata()



# """
# Runtime hook that guarantees that *any* import of
# torch.distributed.checkpoint.metadata exposes `.mcore_data`
# as an alias for `.storage_data`.

# Safe to leave in production – if the attribute already exists we do
# nothing.
# """
# import importlib
# import sys
# from types import ModuleType

# _TARGET = "torch.distributed.checkpoint.metadata"


# def _patch(module: ModuleType):
#     """Idempotently add the alias to the Metadata class inside *module*."""
#     Meta = getattr(module, "Metadata", None)
#     if Meta is None:  # very old torch – nothing to do
#         return
#     if not hasattr(Meta, "mcore_data") and hasattr(Meta, "storage_data"):
#         setattr(Meta, "mcore_data", property(lambda self: self.storage_data))


# class _Finder(importlib.abc.MetaPathFinder):
#     """Intercept *every* import of the target module."""

#     def find_spec(self, fullname, path, target=None):
#         if fullname == _TARGET:
#             # Let Python do the real import first, then patch in Loader.exec_module
#             return importlib.machinery.ModuleSpec(
#                 fullname, _Loader(), is_package=False
#             )
#         return None


# class _Loader(importlib.abc.Loader):
#     def create_module(self, spec):  # use default machinery
#         return None

#     def exec_module(self, module):
#         # Real import (will fill the module’s namespace)
#         real_module = importlib.import_module(module.__name__)
#         module.__dict__.update(real_module.__dict__)
#         # And now patch it
#         _patch(module)


# # ------------------------------------------------------------------
# # Register the hook and patch the module if it is already imported.
# # ------------------------------------------------------------------
# sys.meta_path.insert(0, _Finder())
# if _TARGET in sys.modules:
#     _patch(sys.modules[_TARGET])
# print("[Shim] Metadata import hook installed (mcore_data ↔ storage_data)")


def main():
    from .extras.misc import is_env_enabled

    if is_env_enabled("USE_V1"):
        from .v1 import launcher
    else:
        from . import launcher

    launcher.launch()


if __name__ == "__main__":
    from multiprocessing import freeze_support

    freeze_support()
    main()
