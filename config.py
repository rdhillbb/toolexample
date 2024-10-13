import yaml
import importlib
from langchain_core.tools import BaseTool

def dynamic_import(module_path, import_items):
    """Dynamically imports specified objects from a module."""
    module = importlib.import_module(module_path)
    imported_objects = {}
    for item in import_items:
        object_name = item["name"]
        imported_objects[object_name] = getattr(module, object_name)
    return imported_objects

def readconfig(confile: str):
    with open(confile, "r") as file:
        config = yaml.safe_load(file)

    all_imported_objects = {}
    objs = []
    for module_info in config["modules"]:
        module_path = module_info["path"]
        imports = module_info["imports"]

        imported_objects = dynamic_import(module_path, imports)
        for name, obj in imported_objects.items():
            all_imported_objects[name] = obj
            if isinstance(obj, BaseTool):
                # For BaseTool instances, we don't call them, we just append them
                objs.append(obj)
            else:
                # For regular classes, we instantiate them
                objs.append(obj())

    return objs
