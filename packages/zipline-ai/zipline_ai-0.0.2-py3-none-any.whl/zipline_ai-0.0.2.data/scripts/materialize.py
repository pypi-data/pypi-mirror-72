#!python
# tool to materialize feature_sources and feature_sets into thrift configurations
# that zipline jobs can consume

import click
import os
import traceback
import zipline.repo.extract_objects as eo
from zipline.schema.serializer import thrift_simple_json_protected
from zipline.schema.thrift.ttypes import GroupBy, LeftOuterJoin, StagingQuery
from zipline.utils import get_streaming_sources

# This is set in the main function -
# from command line or from env variable during invocation
folder_name_to_class = {
    "group_bys": GroupBy,
    "joins": LeftOuterJoin,
    "staging_queries": StagingQuery
}


@click.command()
@click.option(
    '--zipline_root',
    envvar='ZIPLINE_ROOT',
    help='Path to the root zipline folder',
    default=False)
@click.option(
    '--input_path',
    help='Relative Path to the root zipline folder, which contains the objects to be serialized',
    required=True)
@click.option(
    '--output_root',
    help='Relative Path to the root zipline folder, to where the serialized output should be written',
    default="production")
def extract_and_convert(zipline_root, input_path, output_root):
    """
    CLI tool to convert Python zipline GroupBy's, Joins and Staging queries into their thrift representation.
    The materialized objects are what will be submitted to spark jobs - driven by airflow, or by manual user testing.
    """
    if not zipline_root:
        zipline_root = os.getcwd()
    _print_highlighted("Using zipline root path", zipline_root)
    zipline_root_path = os.path.expanduser(zipline_root)
    obj_folder_name = input_path.split('/', 1)[0]
    obj_class = folder_name_to_class[obj_folder_name]
    _print_highlighted("Object class", obj_class.__name__)
    output_path = os.path.join(zipline_root_path, output_root, obj_folder_name)
    full_input_path = os.path.join(zipline_root_path, input_path)
    _print_highlighted(f"Input {obj_folder_name} from", full_input_path)
    _print_highlighted(f"Writing {obj_folder_name} to", output_path)

    assert os.path.exists(full_input_path), f"Input Path: {full_input_path} doesn't exist"
    if os.path.isdir(full_input_path):
        results = eo.from_folder(zipline_root_path, full_input_path, obj_class)
    elif os.path.isfile(full_input_path):
        assert full_input_path.endswith(".py"), f"Input Path: {input_path} isn't a python file"
        results = eo.from_file(zipline_root_path, full_input_path, obj_class)
    else:
        raise Exception(f"Input Path: {full_input_path}, isn't a file or a folder")

    for name, obj in results.items():
        name = name.split('.', 1)[1]
        final_output_path = output_path
        _write_obj_as_json(name, obj, final_output_path, obj_class)
    print(f"Successfully wrote {len(results)} {(obj_class).__name__} objects to {output_path}")


def _write_obj_as_json(name, obj, output_path, obj_class):
    class_name = obj_class.__name__
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    assert os.path.isdir(output_path), f"Output Path: {output_path} isn't a directory"
    assert hasattr(obj, "name"), f"Can't serialize objects without the name attribute for object {name}"
    assert obj.name is None, f"Name is set internally, users cannot set the name. Conflict [{name} - {obj.name}]"
    # name of the file and name field in the object should basically match. Never change this.
    obj.name = name
    team_name = name.split(".")[0]
    file_name = ".".join([x.replace(".py", "") for x in name.split(".")[1:]])
    _print_highlighted(f"{class_name} Team", team_name)
    _print_highlighted(f"{class_name} Name", name)
    output_folder = os.path.join(output_path, team_name)
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    assert os.path.isdir(output_folder), f"{output_folder} isn't a folder."
    output_file = os.path.join(output_folder, file_name)
    with open(output_file, "w") as f:
        _print_highlighted(f"Writing {class_name} to", output_file)
        f.write(thrift_simple_json_protected(obj, obj_class))


def _print_highlighted(left, right, left_padding=40):
    # print in blue and bold
    print(f"{left:>25} - \033[34m\033[1m{right}\033[00m")

if __name__ == '__main__':
    extract_and_convert()
