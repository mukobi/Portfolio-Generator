"""Loads content from the `content` dir of a source site.

This includes only loading meta.yaml files into a dictionary tree, ignoring other files.
"""
import os
import collections
import yaml


def __children_sort_key(item_tuple):
    """Extracts the key for sorting from the child meta file."""
    try:
        return int(item_tuple[0].split('.')[0])
    except ValueError:
        return 0  # defult sort to back


def load_meta_tree(content_in):
    """Loads the meta files for the given site into a dictionary.

    Reads through the directory `content_in`. All `meta.yaml` files encountered
    are built into a dictionary that is returned.

    Note: operates recursively, so don't try any simbolic linking and shit.
    """

    meta_tree = collections.OrderedDict()
    meta_tree['meta'] = None
    children = {}
    for filename in os.listdir(content_in):
        filepath = os.path.join(content_in, filename)

        if os.path.isfile(filepath) and filename == 'meta.yaml':
            with open(filepath) as meta_file:
                meta_tree['meta'] = yaml.full_load(meta_file)

        elif os.path.isdir(filepath):
            children[filename] = load_meta_tree(filepath)

        elif os.path.isfile(filepath) and filename != 'meta.yaml':
            if 'files' not in meta_tree.keys():
                meta_tree['files'] = []
            meta_tree['files'].append(filename)

    # sort children by the number in their filename where higher orders will come first
    sorted_tuple = tuple([
        (item[0].split('.', 1)[-1], item[1]) for item in
        sorted(children.items(), key=__children_sort_key, reverse=True)])
    # tuple((key.split('.')[1:], value) for key, value in
    meta_tree['children'] = collections.OrderedDict(sorted_tuple)

    return meta_tree
