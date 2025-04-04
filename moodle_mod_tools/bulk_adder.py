"""Bulk adder module for Moodle backups."""

import json
from .section_adder import add_section_to_backup
from .page_adder import add_page_to_backup


def bulk_add_from_tar(
    input_tar: str,
    output_tar: str,
    config_file: str
) -> None:
    from .mbz_packager import with_extracted_tar
    with with_extracted_tar(input_tar, output_tar) as extracted_dir:
        bulk_add_from_json(
            input_backup=extracted_dir,
            output_backup=extracted_dir,
            config_file=config_file
        )

def bulk_add_from_json(input_backup, output_backup, config_file):
    """Adds sections/pages in bulk from a JSON config."""
    with open(config_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for section in data:
        section_name = section.get('section_name')
        section_id = section.get('section_id')

        # If no explicit section_id, create a new section by passing None
        created_section_id = add_section_to_backup(
            input_backup=input_backup,
            output_backup=output_backup,
            section_name=section_name,
            section_id=section_id
        )
        
        # Fall back to the newly created ID if original was None
        if not section_id:
            section_id = created_section_id

        # Add pages
        for page in section.get('pages', []):
            add_page_to_backup(
                extracted_backup_dir=output_backup,
                section_id=str(section_id),
                page_title=page.get('page_title', 'Untitled Page'),
                page_description=page.get('page_description', ''),
                page_content=page.get('page_content', ''),
                output_dir=None
            )
