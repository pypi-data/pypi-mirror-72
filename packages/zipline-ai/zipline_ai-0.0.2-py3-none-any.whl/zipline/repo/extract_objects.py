import glob
import importlib.machinery
import importlib.util
import logging
import os


def from_folder(root_path: str,
                full_path: str,
                cls: type):
    """
    Recursively consumes a folder, and constructs a map
    Creates a map of object qualifier to
    """
    if full_path.endswith('/'):
        full_path = full_path[:-1]

    python_files = glob.glob(
        os.path.join(full_path, "**/*.py"),
        recursive=True)
    result = {}
    for f in python_files:
        result.update(from_file(root_path, f, cls))
    return result


def from_file(root_path: str,
              file_path: str,
              cls: type):
    logging.debug(
        "Loading objects of type {cls} from {file_path}".format(**locals()))

    loader = importlib.machinery.SourceFileLoader(
        "dummy_mod_name", file_path)
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)

    # mod_qualifier includes team name and python script name without `.py`
    # this line takes the full file path as input, strips the root path on the left side
    # strips `.py` on the right side and finally replaces the slash sign to dot
    # eg: the output would be `team_name.python_script_name`
    mod_qualifier = file_path[len(root_path.rstrip('/')) + 1:-3].replace("/", ".")
    # the key of result dict would be `team_name.python_script_name.[group_by_name|join_name|staging_query_name]`
    # real world case: psx.reservation_status.v1
    result = {f"{mod_qualifier}.{name}": obj
              for name, obj in list(mod.__dict__.items())
              if isinstance(obj, cls)}
    return result
