"""Compiles the contents for sites in ./content using templates in ./templates
and outputs the static web content to ./output.

Usage:
`python compile.py` - Compile all sites.
"""

import os
import json
import shutil
import argparse
from jinja2 import Template

from python_lib import meta_loader
from python_lib import renderer
from python_lib import repo_copier

DEFAULT_VERBOSITY = 1

DIR_ROOT = os.path.dirname(os.path.abspath(__file__))
DIR_SRC = os.path.join(DIR_ROOT, 'source')
DIR_OUTPUT = os.path.join(DIR_ROOT, 'output')

REPO_OUTPUTS = {
    'software': os.path.join(DIR_ROOT, './../sticksandstones'),
    'photos': os.path.join(DIR_ROOT, './../Photography-Portfolio')
}


def main():
    """Main execution function."""
    # parse args
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-v', '--verbosity',
        help='Verbosity level, 0 is least verbose.',
        default=1, type=int, choices=range(0, 3))
    parser.add_argument(
        'site', nargs='?', default=None,
        help='Name of an individual source project to compile')
    args = parser.parse_args()

    # run compilation
    if args.site == None:
        compile_all(args.verbosity)
    else:
        compile_individual(args.site, args.verbosity)


def compile_all(verbosity):
    """Compiles all site at once."""
    for name in os.listdir(DIR_SRC):  # TODO: multithread
        compile_individual(name, verbosity)


def compile_individual(name, verbosity):
    """Compiles only the site matching name `name`."""
    # get input folders
    dir_input = os.path.join(DIR_SRC, name)
    dir_input_precompile = os.path.join(dir_input, 'precompile')
    dir_input_templates = os.path.join(dir_input, 'templates')
    dir_input_content = os.path.join(dir_input, 'content')

    # get output folder
    dir_output = os.path.join(DIR_OUTPUT, name)
    # clean output folder
    shutil.rmtree(dir_output, ignore_errors=True)

    # run precompile code
    if os.path.exists(dir_input_precompile):
        for executable_name in sorted(os.listdir(dir_input_precompile)):
            os.system(os.path.join(dir_input_precompile, executable_name))

    # load in stuff
    meta_tree = meta_loader.load_meta_tree(dir_input_content)
    if verbosity >= 2:
        print(json.dumps(meta_tree, indent=2))

    # render stuff
    renderer.render_site(
        dir_input_content, dir_output, meta_tree, dir_input_templates)

    if verbosity >= 1:
        print(f'Compiled: {name}')

    # copy stuff to output repository
    repo_copier.copy_portfolio_single(dir_output, REPO_OUTPUTS[name], ['.'])


if __name__ == "__main__":
    main()
