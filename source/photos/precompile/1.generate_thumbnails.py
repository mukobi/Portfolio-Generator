"""Generates thumbnails for each image in Albums formatted `thumb.{orig_name}`.
"""

import os
from PIL import Image

THUMBNAIL_COMPRESSION_RATIO = 0.25
INCLUDED_FILE_EXTENSIONS = ['.jpg', '.jpeg', '.png']
THUMBNAIL_OUTPUT_PREXIF = 'thumb.'

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

    # create thumbnail if it doesn't exist
    num_thumbnails_generated = 0
    for input_path in image_file_paths:
        if os.path.basename(input_path).startswith(THUMBNAIL_OUTPUT_PREXIF):
            continue  # don't make a thumbnail of a thumbnail
        output_path = os.path.join(
            os.path.dirname(input_path), THUMBNAIL_OUTPUT_PREXIF + os.path.basename(input_path))
        if os.path.isfile(output_path):
            continue  # assume existing thumnail was correctly generated
        try:
            image = Image.open(input_path)
            size = [image.size[0] * THUMBNAIL_COMPRESSION_RATIO,
                    image.size[1] * THUMBNAIL_COMPRESSION_RATIO]
            image.thumbnail(size, Image.ANTIALIAS)
            image.save(output_path, 'JPEG')
            num_thumbnails_generated += 1
        except IOError:
            print(f'cannot create thumbnail for "{input_path}"')

    print(f'Photos: Generated {num_thumbnails_generated} thumbnail images.')


if __name__ == "__main__":
    main()
