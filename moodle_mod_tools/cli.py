#!/usr/bin/env python3
"""CLI tool to unify all moodle_mod_tools functionality"""
import argparse
import sys
from .page_adder import add_page_to_backup
from .section_adder import add_section_to_backup

def main():
    parser = argparse.ArgumentParser(description="CLI for Moodle mod tools")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommand adding page
    parser_page = subparsers.add_parser("add-page", help="Add a new page")
    parser_page.add_argument("extracted_backup_dir")
    parser_page.add_argument("section_id")
    parser_page.add_argument("page_title")
    parser_page.add_argument("--page_description", default="Placeholder description")
    parser_page.add_argument("--page_content", default="Placeholder content")
    parser_page.add_argument("--output_dir", default=None)

    # Subcommand adding section
    parser_section = subparsers.add_parser("add-section", help="Add a new section")
    parser_section.add_argument("--input", required=True)
    parser_section.add_argument("--output", required=True)
    parser_section.add_argument("--section_name", required=True)
    parser_section.add_argument("--section_id", type=int, default=None)

    # Subcommand packaging MBZ
    parser_package = subparsers.add_parser("package-mbz", help="Package directory into MBZ archive")
    parser_package.add_argument("source_dir", help="Directory to package")
    parser_package.add_argument("output_file", help="Desired .mbz archive file name")

    # Subcommand depackaging MBZ
    parser_depackage = subparsers.add_parser("depackage-mbz", help="Extract MBZ archive into directory")
    parser_depackage.add_argument("archive_path", help="Path to the .mbz archive")
    parser_depackage.add_argument("output_dir", help="Directory to extract the archive into")

    # Subcommand bulk add
    parser_bulk_add = subparsers.add_parser("bulk-add", help="Bulk add sections and pages from config")
    parser_bulk_add.add_argument("--input_tar", required=True, help="Input tar archive")
    parser_bulk_add.add_argument("--output_tar", required=True, help="Output tar archive")
    parser_bulk_add.add_argument("--config_file", required=True, help="JSON configuration file for bulk adding")

    args = parser.parse_args()
    if args.command == "add-page":
        add_page_to_backup(
            extracted_backup_dir=args.extracted_backup_dir,
            section_id=args.section_id,
            page_title=args.page_title,
            page_description=args.page_description,
            page_content=args.page_content,
            output_dir=args.output_dir
        )
    elif args.command == "add-section":
        add_section_to_backup(
            input_backup=args.input,
            output_backup=args.output,
            section_name=args.section_name,
            section_id=args.section_id
        )
    elif args.command == "package-mbz":
        from .mbz_packager import package_mbz
        package_mbz(args.source_dir, args.output_file)
    elif args.command == "depackage-mbz":
        from .mbz_packager import decompress_mbz
        decompress_mbz(args.archive_path, args.output_dir)
    elif args.command == "bulk-add":
        from .bulk_adder import bulk_add_from_tar
        bulk_add_from_tar(
            input_tar=args.input_tar,
            output_tar=args.output_tar,
            config_file=args.config_file
        )
    

if __name__ == "__main__":
    main()
