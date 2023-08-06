"""Utilities to help read and write Sophize resources as json data."""

import json
from pathlib import Path
from typing import List

from .resources import Argument, Article, Beliefset, Project, Proposition, Term


def get_filename(assignable_id, resource_type):
    """The name of the file is depends on its type and its assignable_id. """
    return _get_resource_code(resource_type) + '_' + assignable_id + '.json'


def remove_nulls(obj):
    """Recursive function to remove nulls in a dict."""
    if isinstance(obj, List):
        return [remove_nulls(list_item) for list_item in obj]
    if not isinstance(obj, dict):
        return obj
    return {k: remove_nulls(v) for k, v in obj.items() if v is not None}


def write_json(directory, assignable_id, resource):
    """Utility function to write a resource as a json file."""
    directory_path = Path(directory)
    Path(directory_path).mkdir(parents=True, exist_ok=True)
    filepath = Path.joinpath(
        directory_path, get_filename(assignable_id, type(resource)))
    with open(filepath, 'w') as fout:
        json.dump(remove_nulls(resource.to_dict()), fout, indent=2)


def resource_from_dict(resource_code, json_data):
    """Utility function to parse resource from json data."""
    if resource_code == 'T':
        return Term.from_dict(json_data)
    if resource_code == 'P':
        return Proposition.from_dict(json_data)
    if resource_code == 'A':
        return Argument.from_dict(json_data)
    if resource_code == 'B':
        return Beliefset.from_dict(json_data)
    if resource_code == 'R':
        return Article.from_dict(json_data)
    if resource_code == 'J':
        return Project.from_dict(json_data)
    if resource_code == 'M':
        return Machine.from_dict(json_data)
    return None


def read_resource(directory, filename):
    """Utility function to read a resource from a json file."""
    filepath = Path.joinpath(Path(directory), filename)
    with open(str(filepath), "r") as file:
        json_data = json.loads(file.read())
    resource = resource_from_dict(filename[0], json_data)
    return [filename[2: -5], resource]


def _get_resource_code(resource_type):
    if resource_type == Term:
        return 'T'
    if resource_type == Proposition:
        return 'P'
    if resource_type == Argument:
        return 'A'
    if resource_type == Beliefset:
        return 'B'
    if resource_type == Article:
        return 'R'
    if resource_type == Project:
        return 'J'
    if resource_type == Machine:
        return 'M'
    return None
