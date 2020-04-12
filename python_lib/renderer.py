"""Renders the static output files using Jinja2.

This includes both loading meta.json files into a dictionary tree and copying
over all other files to the output directory.
"""
import os
import json
import shutil
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

        if 'meta' in meta_tree:
            # build an HTML output file if the meta specifies a template to use
            my_meta = meta_tree['meta']
            if 'template' in my_meta.keys():
                template = template_env.get_template(my_meta['template'])
                rendered = template.render(meta_tree)
                file_out_path = os.path.join(dir_output, 'index.html')
                with open(file_out_path, 'w') as file:
                    file.write(rendered)

        for file_name in os.listdir(dir_content):
            file_path = os.path.join(dir_content, file_name)

            if os.path.isdir(file_path):
                # render the child directory, scoped to its own child meta tree
                recurse(file_path, os.path.join(dir_output, file_name),
                        meta_tree['children'][file_name])

            elif os.path.isfile(file_path) and file_name != 'meta.json':
                # copy file to output director
                # copy2 copies metadata and permissions into a directory
                shutil.copy2(file_path, dir_output)
    recurse(dir_content, site_out, meta_tree)