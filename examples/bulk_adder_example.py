#!/usr/bin/env python3
"""
Example usage of functions from bulk_adder.
"""

import os
import json
from moodle_mod_tools.bulk_adder import bulk_add_from_tar, bulk_add_from_json

if __name__ == "__main__":
    # Create a sample config JSON.
    config_data = [
            {
                "title": "New Section",
                "pages": [
                    {"title": "Page Title", "content": "<p>Page Content</p>"}
                ]
            }
        ]
    with open("config.json", "w") as f:
        json.dump(config_data, f)

    # Example tar usage.
    # Suppose input_backup.tar and output_backup.tar are existing tar paths.
    input_tar = "input_backup.tar"
    output_tar = "output_backup.tar"

    if not os.path.exists(input_tar):
        # Just for example, create an empty tar.
        open(input_tar, "wb").close()

    bulk_add_from_tar(input_tar, output_tar, "config.json")

    # Example JSON usage.
    # Suppose input_backup.mbz and output_backup.mbz are existing .mbz files.
    input_backup = "input_backup.mbz"
    output_backup = "output_backup.mbz"

    if not os.path.exists(input_backup):
        open(input_backup, "wb").close()

    bulk_add_from_json(input_backup, output_backup, "config.json")