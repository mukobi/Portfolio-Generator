
"""Copies a rendered portfolio to destination folder.

Deletes everything originally in destination except top-leveel items that
start with any of the ignore_delete_prefixes.
"""

import os
import shutil


def copy_portfolio_single(source, destination, ignore_delete_prefix):
    """Copies a rendered portfolio to destination folder.

    Deletes everything originally in destination except top-leveel items that
    start with any of the ignore_delete_prefixes.
    """
    # remove everything in destination that isn't protected
    __delete_folder(destination, ignore_delete_prefix)
    # copy stuff over
    __copy_folder(source, destination)

    print(f'Successfully copied to {os.path.basename(destination)} repo')


def __delete_folder(folder, ignore_delete_prefix):
    """Copies everything in src folder into dst folder.
    """
    for filename in os.listdir(folder):
        # ignore using prefixes
        ignore = False
        for prefix in ignore_delete_prefix:
            if filename.startswith(prefix):
                ignore = True
        if ignore:
            continue
        # otherwise, delete that thang
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except OSError as error:
            print('Failed to delete %s. Reason: %s' % (file_path, error))


def __copy_folder(src, dst, symlinks=False, ignore=None):
    """Copies everything in src folder into dst folder.
    """
    for item in os.listdir(src):
        item_source = os.path.join(src, item)
        item_destination = os.path.join(dst, item)
        if os.path.isdir(item_source):
            shutil.copytree(item_source, item_destination, symlinks, ignore)
        else:
            shutil.copy2(item_source, item_destination)
