bl_info = {
    "name": "pcb2blender importer",
    "description": "Enables Blender to import .pcb3d files, exported from KiCad.",
    "author": "Bobbe",
    "version": (1, 7, 0),
    "blender": (3, 2, 0),
    "location": "File > Import",
    "category": "Import-Export",
    "support": "COMMUNITY",
    "wiki_url": "https://github.com/30350n/pcb2blender",
}

import importlib.util, subprocess, sys
from pathlib import Path

dependencies = {
    "skia-python": "skia",
    "pillow": "PIL",
}
module_names = ("import", "materials")

dependency_path = (Path(__file__).parent / "site-packages").resolve()
dependency_path.mkdir(exist_ok=True)
sys.path.append(str(dependency_path))

missing = []
for dependency, module_name in dependencies.items():
    if not importlib.util.find_spec(module_name):
        missing.append(dependency)
if missing:
    subprocess.check_call((
        sys.executable, "-m",
        "pip", "install", "--no-deps", *missing, "-t", str(dependency_path)
    ))

modules = []
for module_name in module_names:
    if module_name in locals():
        modules.append(importlib.reload(locals()[module_name]))
    else:
        modules.append(importlib.import_module("." + module_name, package=__package__))

def register():
    for module in modules:
        module.register()

def unregister():
    for module in modules:
        module.unregister()
