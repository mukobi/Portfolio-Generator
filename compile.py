"""Compiles the contents for sites in ./content using templates in ./templates
and outputs the static web content to ./output.

Usage:
`python compile.py` - Compile all sites.
"""

import os
import json
import shutil
from jinja2 import Template

from python_lib import content_loader
from python_lib import renderer

DEFAULT_VERBOSITY = 0

DIR_ROOT = os.path.dirname(os.path.abspath(__file__))
DIR_SRC = os.path.join(DIR_ROOT, 'source')
DIR_OUTPUT = os.path.join(DIR_ROOT, 'output')


def main():
    """Main execution function."""
    verbosity = 1
    compile_all(verbosity)


def compile_all(verbosity=DEFAULT_VERBOSITY):
    """Compiles all site at once."""
    for name in os.listdir(DIR_SRC):
        compile_individual(name, verbosity)


def compile_individual(name, verbosity=DEFAULT_VERBOSITY):
    """Compiles only the site matching name `name`."""
    # get input folders
    dir_input = os.path.join(DIR_SRC, name)
    dir_input_templates = os.path.join(dir_input, 'templates')
    dir_input_content = os.path.join(dir_input, 'content')
    # get output folder
    dir_output = os.path.join(DIR_OUTPUT, name)
    # clean output folder
    shutil.rmtree(dir_output, ignore_errors=True)

    # load in stuff
    meta_tree = content_loader.load_meta_tree(dir_input_content)
    if verbosity >= 2:
        print(json.dumps(meta_tree, indent=2))

    # render stuff
    renderer.render_site(
        dir_input_content, dir_output, meta_tree, dir_input_templates)

    if verbosity >= 1:
        print(f'Compiled: {name}')


if __name__ == "__main__":
    main()
