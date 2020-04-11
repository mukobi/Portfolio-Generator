"""Loads content from the `content` dir of a source site.

This includes only loading meta.json files into a dictionary tree, ignoring other files.
"""
import os
import json
import collections


def __children_sort_key(item_tuple):
    """Extracts the key for sorting from the child meta file."""
    try:
        return item_tuple[1]['meta']['order']
    except KeyError:
        return 0  # defult sort to back


def load_meta_tree(content_in):
    """Loads the meta files for the given site into a dictionary.

    Reads through the directory `content_in`. All `meta.json` files encountered
    are built into a dictionary that is returned.

    Note: operates recursively, so don't try any simbolic linking and shit.
    """

    meta_tree = collections.OrderedDict()
    children = {}
    for filename in os.listdir(content_in):
        filepath = os.path.join(content_in, filename)

        if os.path.isfile(filepath) and filename == 'meta.json':
            with open(filepath) as meta_file:
                meta_tree['meta'] = json.loads(meta_file.read())

        elif os.path.isdir(filepath):
            children[filename] = load_meta_tree(filepath)

    # sort children by their 'order' meta key where higher orders will come first
    meta_tree['children'] = collections.OrderedDict(
        sorted(children.items(), key=__children_sort_key, reverse=True))

    return meta_tree
