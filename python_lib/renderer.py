"""Renders the static output files using Jinja2.

This includes both loading meta.json files into a dictionary tree and copying
over all other files to the output directory.
"""
import os
import json
from jinja2 import Environment, FileSystemLoader, Template


def render_site(dir_content, site_out, meta_tree, dir_template):
    """Loads the meta files and copies over the other files for the given site.

    Reads through the directory `content_in`. All `meta.json` files encountered
    are built into a dictionary that is returned. All other files are copied
    over to `site_out`.

    Note: operates recursively, so don't try any simbolic linking and shit.
    """
    template_env = Environment(
        loader=FileSystemLoader(dir_template)
    )

    def recurse(dir_content, dir_output, meta_tree):
        os.makedirs(dir_output, exist_ok=True)  # make dir if doesn't exist

        for filename in os.listdir(dir_content):
            file_in_path = os.path.join(dir_content, filename)
            my_meta = meta_tree['meta']

            if filename == 'meta.json':
                # build an HTML output file if the meta specifies a template to use
                if 'template' in my_meta.keys():
                    template = template_env.get_template(my_meta['template'])
                    rendered = template.render(meta_tree)
                    file_out_path = os.path.join(dir_output, 'index.html')
                    with open(file_out_path, 'w') as file:
                        file.write(rendered)

            elif os.path.isdir(file_in_path):
                # render the child directory, scoped to its own child meta tree
                recurse(file_in_path, os.path.join(dir_output, filename),
                        meta_tree['children'][filename])

            elif os.path.isfile(file_in_path):
                # TODO: copy file to output director
                pass

    recurse(dir_content, site_out, meta_tree)
