#!/usr/bin/env python3
"""
Demonstrates usage of section_adder functions.
"""

import os
from moodle_mod_tools.section_adder import (
    add_section_to_backup,
    find_section_id_by_name,
    add_section_from_tar,
)

if __name__ == "__main__":
    # Example usage of add_section_to_backup
    input_backup = "course_backup.mbz"
    output_backup = "course_backup_with_section.mbz"

    if not os.path.exists(input_backup):
        open(input_backup, "wb").close()

    section_name = "New Section"
    add_section_to_backup(input_backup, output_backup, section_name)

    # Example usage of find_section_id_by_name
    # For a real usage, pass an extracted backup directory.
    # For now, assume there's a folder "extracted_backup".
    extracted_backup_dir = "extracted_backup"
    os.makedirs(extracted_backup_dir, exist_ok=True)
    found_id = find_section_id_by_name(extracted_backup_dir, "New Section")
    print("Found section ID:", found_id)

    # Example usage of add_section_from_tar
    input_tar = "course_backup.tar"
    output_tar = "course_backup_with_section.tar"
    if not os.path.exists(input_tar):
        open(input_tar, "wb").close()

    add_section_from_tar(input_tar, output_tar, section_name)