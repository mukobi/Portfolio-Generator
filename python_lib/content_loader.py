"""Loads content from the `content` dir of a source site.

This includes only loading meta.json files into a dictionary tree, ignoring other files.
"""
import os
import json


def load_meta_tree(content_in):
    """Loads the meta files and copies over the other files for the given site.

    Reads through the directory `content_in`. All `meta.json` files encountered
    are built into a dictionary that is returned.

    Note: operates recursively, so don't try any simbolic linking and shit.
    """
    meta = {'children': {}}
    for filename in os.listdir(content_in):
        filepath = os.path.join(content_in, filename)

        if os.path.isfile(filepath) and filename == 'meta.json':
            with open(filepath) as meta_file:
                meta['meta'] = json.loads(meta_file.read())

        elif os.path.isdir(filepath):
            meta['children'][filename] = load_meta_tree(filepath)

    return meta
