#!/usr/bin/env python3
"""Module for adding sections to a Moodle backup."""

import os
import shutil
import argparse
import time
import re
import xml.etree.ElementTree as ET


def add_section_to_backup(input_backup: str, output_backup: str, section_name: str, section_id: int = None) -> int:
    """Copies an uncompressed Moodle backup folder, adds a new section, and updates moodle_backup.xml.
    Returns the newly created section ID.
    """
    if not os.path.exists(output_backup):
        shutil.copytree(input_backup, output_backup)

    sections_dir = os.path.join(output_backup, 'sections')
    existing_ids = []
    if os.path.isdir(sections_dir):
        for name in os.listdir(sections_dir):
            if name.startswith('section_'):
                attempt = name.split('_')[1]
                if attempt.isdigit():
                    existing_ids.append(int(attempt))
    new_id = 30
    if existing_ids:
        new_id = max(existing_ids) + 1


    new_section_path = os.path.join(sections_dir, f'section_{new_id}')
    os.makedirs(new_section_path, exist_ok=True)

    now = int(time.time())
    section_number = new_id - 8  # naive guess

    section_xml = f"""<?xml version="1.0" encoding="UTF-8"?>\n<section id="{new_id}">\n  <number>{section_number}</number>\n  <name>{section_name}</name>\n  <summary></summary>\n  <summaryformat>1</summaryformat>\n  <sequence></sequence>\n  <visible>1</visible>\n  <availabilityjson>$@NULL@$</availabilityjson>\n  <component>$@NULL@$</component>\n  <itemid>$@NULL@$</itemid>\n  <timemodified>{now}</timemodified>\n</section>\n"""
    with open(os.path.join(new_section_path, 'section.xml'), 'w', encoding='UTF-8') as f:
        f.write(section_xml)

    inforef_xml = """<?xml version="1.0" encoding="UTF-8"?>\n<inforef>\n</inforef>\n"""
    with open(os.path.join(new_section_path, 'inforef.xml'), 'w', encoding='UTF-8') as f:
        f.write(inforef_xml)

    backup_xml_path = os.path.join(output_backup, 'moodle_backup.xml')
    with open(backup_xml_path, 'r', encoding='UTF-8') as f:
        data = f.read()

    new_backup_name = os.path.basename(output_backup) + ".mbz"
    data = re.sub(r'<name>[^<]*</name>', f'<name>{new_backup_name}</name>', data, 1)
    data = re.sub(r'<value>[^<]*.mbz</value>', f'<value>{new_backup_name}</value>', data, 1)

    new_section_block = f"""
        <section>\n          <sectionid>{new_id}</sectionid>\n          <title>{section_name}</title>\n          <directory>sections/section_{new_id}</directory>\n          <parentcmid></parentcmid>\n          <modname></modname>\n        </section>\n    """.strip()

    x = data.find('</sections>')
    if x != -1:
        data = data[:x] + new_section_block + "\n" + data[x:]

    new_settings_block = f"""
      <setting>\n        <level>section</level>\n        <section>section_{new_id}</section>\n        <name>section_{new_id}_included</name>\n        <value>1</value>\n      </setting>\n      <setting>\n        <level>section</level>\n        <section>section_{new_id}</section>\n        <name>section_{new_id}_userinfo</name>\n        <value>0</value>\n      </setting>\n    """.strip()
    y = data.find('</settings>')
    if y != -1:
        data = data[:y] + new_settings_block + "\n" + data[y:]

    with open(backup_xml_path, 'w', encoding='UTF-8') as f:
        f.write(data)

    print(f"Section created with ID {new_id} and name '{section_name}'")
    return new_id


def find_section_id_by_name(backup_dir: str, name: str) -> int:
    """
    Searches moodle_backup.xml for a section with <title> == name
    and returns the <sectionid>. Returns -1 if not found.
    """
    backup_xml_path = os.path.join(backup_dir, 'moodle_backup.xml')
    if not os.path.isfile(backup_xml_path):
        return -1

    tree = ET.parse(backup_xml_path)
    root = tree.getroot()
    sections = root.findall("./contents/sections/section")
    for sect in sections:
        sec_id_elem = sect.find("sectionid")
        title_elem = sect.find("title")
        if sec_id_elem is not None and title_elem is not None:
            if title_elem.text == name:
                return int(sec_id_elem.text)
    return -1

def cli_main():
    parser = argparse.ArgumentParser(description="Add a new section to an uncompressed Moodle backup.")
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--section_name', required=True)
    parser.add_argument('--section_id', type=int, default=None)
    args = parser.parse_args()

    new_id = add_section_to_backup(
        input_backup=args.input,
        output_backup=args.output,
        section_name=args.section_name,
        section_id=args.section_id
    )
    print(f"Section with name {args.section_name} has ID = {new_id}")


def add_section_from_tar(
    input_tar: str,
    output_tar: str,
    section_name: str,
    section_id: int = None
) -> int:
    from .mbz_packager import with_extracted_tar
    with with_extracted_tar(input_tar, output_tar) as extracted_dir:
        new_id = add_section_to_backup(
            input_backup=extracted_dir,
            output_backup=extracted_dir,
            section_name=section_name,
            section_id=section_id
        )
    return new_id

if __name__ == "__main__":
    cli_main()
