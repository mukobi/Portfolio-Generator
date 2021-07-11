"""Writes the dimensions of each image in Albums as a suffix in the filename.
"""

import os
from PIL import Image
from colorthief import ColorThief

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

    # append the average color

    num_files_renamed = 0
    for file_path in image_file_paths:
        if os.path.basename(file_path).startswith(THUMBNAIL_OUTPUT_PREXIF):
            continue  # ignore existing thumbnails

        split_dot = os.path.basename(file_path).split('.')
        if len(split_dot) == 4 and len(split_dot[1]) == 6:
            continue  # ignore already renames images

        # append the dominant color of the image
        dominant_color = '%02x%02x%02x' % ColorThief(file_path).get_color(10)

        # append the image dimensions as 'widthxheight' into the name of each file
        with Image.open(file_path) as img:
            width, height = img.size
            dimension_string = f'{width}x{height}'
        base_name, file_extension = os.path.splitext(file_path)
        if not base_name.endswith(dimension_string):
            new_file_path = f'{base_name}.{dominant_color}.{dimension_string}{file_extension}'
            print(f'Processed {new_file_path}')
            os.rename(file_path, new_file_path)
            num_files_renamed += 1
    print(f'Photos: Renamed {num_files_renamed} images.')


if __name__ == "__main__":
    main()
