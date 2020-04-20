"""Compiles the contents for sites in ./content using templates in ./templates
and outputs the static web content to ./output.

Usage:
`python compile.py` - Compile all sites.
"""

import os
from PIL import Image

INCLUDED_FILE_EXTENSIONS = ['.jpg', '.jpeg', '.png']

DIR_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR_ALBUMS = os.path.join(DIR_PROJECT_ROOT, 'content/Albums')


def main():
    """Main execution function."""
    # find all image file paths in Albums folder
    image_file_paths = []
    for root, _, files in os.walk(DIR_ALBUMS):
        for file_name in files:
            # exclude files that don't match our file extensions
            matches_file_extension = False
            for extension in INCLUDED_FILE_EXTENSIONS:
                if file_name.lower().endswith(extension):
                    matches_file_extension = True
            if not matches_file_extension:
                continue
            image_file_paths.append(os.path.join(root, file_name))

    # append the image dimensions into the name of each file
    num_files_renamed = 0
    for file_path in image_file_paths:
        # get image dimensions as ' widthxheight'
        with Image.open(file_path) as img:
            width, height = img.size
            dimension_string = f'.{width}x{height}'
        base_name, file_extension = os.path.splitext(file_path)
        if not base_name.endswith(dimension_string):
            new_file_path = base_name + dimension_string + file_extension
            os.rename(file_path, new_file_path)
            num_files_renamed += 1
    print(f'Photos: Renamed {num_files_renamed} images.')


if __name__ == "__main__":
    main()
