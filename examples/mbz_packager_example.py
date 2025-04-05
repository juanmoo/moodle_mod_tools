#!/usr/bin/env python3
"""
Demonstrates usage of mbz_packager functions.
"""

import os
from moodle_mod_tools.mbz_packager import package_mbz, decompress_mbz, with_extracted_tar

if __name__ == "__main__":
    source_dir = "sample_course"
    output_file = "sample_course.mbz"

    # Ensure sample directory.
    if not os.path.exists(source_dir):
        os.makedirs(source_dir)
        with open(os.path.join(source_dir, "README.txt"), "w") as f:
            f.write("Sample course content.")

    package_mbz(source_dir, output_file)

    # Decompress the created MBZ
    extract_dir = "extracted_course"
    if not os.path.exists(extract_dir):
        os.makedirs(extract_dir)
    decompress_mbz(output_file, extract_dir)

    # Example usage of context manager with_extracted_tar
    input_tar = "example_backup.tar"
    output_tar = "modified_backup.tar"
    if not os.path.exists(input_tar):
        open(input_tar, "wb").close()

    with with_extracted_tar(input_tar, output_tar) as extracted_dir:
        # Do something with extracted_dir
        pass