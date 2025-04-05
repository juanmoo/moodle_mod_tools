#!/usr/bin/env python3
"""
Demonstrates usage of page_adder functions.
"""

import os
from moodle_mod_tools.page_adder import add_page_to_backup, add_page_from_tar

if __name__ == "__main__":
    extracted_backup_dir = "extracted_backup"
    os.makedirs(extracted_backup_dir, exist_ok=True)

    # Example usage of add_page_to_backup
    # Assume we have a valid extracted Moodle backup in extracted_backup_dir
    section_id = 1
    page_title = "Example Page"
    page_content = "<p>This is an example page</p>"

    add_page_to_backup(
        extracted_backup_dir,
        section_id,
        page_title,
        content_html=page_content
    )

    # Example usage of add_page_from_tar
    input_tar = "input_backup.tar"
    output_tar = "output_backup.tar"
    if not os.path.exists(input_tar):
        open(input_tar, "wb").close()

    add_page_from_tar(
        input_tar,
        output_tar,
        section_id,
        page_title,
        content_html=page_content
    )