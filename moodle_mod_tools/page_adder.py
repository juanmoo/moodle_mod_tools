#!/usr/bin/env python3
"""Module for adding pages to a Moodle backup."""

import os
import sys
import xml.etree.ElementTree as ET
import shutil
import re


def add_page_to_backup(extracted_backup_dir: str, section_id: str, page_title: str, page_description: str = "Placeholder description", page_content: str = "Placeholder content", output_dir: str = None) -> None:
    """Adds a new page to the specified section in an extracted Moodle backup."""
    # 
    if output_dir:
        if os.path.exists(output_dir):
            print(f"Error: output directory '{output_dir}' already exists.")
            sys.exit(1)
        print(f"Copying '{extracted_backup_dir}' to '{output_dir}'...")
        shutil.copytree(extracted_backup_dir, output_dir)
        backup_dir = output_dir
    else:
        backup_dir = extracted_backup_dir
    
    section_path = os.path.join(backup_dir, "sections", f"section_{section_id}")
    if not os.path.isdir(section_path):
        print(f"Error: section {section_id} does not exist.")
        sys.exit(1)

    backup_xml_path = os.path.join(backup_dir, "moodle_backup.xml")
    if not os.path.isfile(backup_xml_path):
        print("Error: moodle_backup.xml not found.")
        sys.exit(1)

    backup_tree = ET.parse(backup_xml_path)
    backup_root = backup_tree.getroot()

    activities_path = os.path.join(backup_dir, "activities")
    max_id = 0
    if os.path.isdir(activities_path):
        for item in os.listdir(activities_path):
            if item.startswith("page_"):
                try:
                    existing_id = int(item.split("_")[1])
                    if existing_id > max_id:
                        max_id = existing_id
                except ValueError:
                    pass
    new_module_id = max_id + 1

    page_dir = f"page_{new_module_id}"
    new_page_path = os.path.join(activities_path, page_dir)
    os.makedirs(new_page_path, exist_ok=True)

    # Add page.xml
    context_id = 13
    page_xml = f'''<?xml version="1.0" encoding="UTF-8"?>\n<activity id="{new_module_id}" moduleid="{new_module_id + 1}" modulename="page" contextid="{context_id}">\n  <page id="{new_module_id}">\n    <name>{page_title}</name>\n    <intro>{page_description}</intro>\n    <introformat>1</introformat>\n    <content>{page_content}</content>\n    <contentformat>1</contentformat>\n    <legacyfiles>0</legacyfiles>\n    <legacyfileslast>$@NULL@$</legacyfileslast>\n    <display>5</display>\n    <displayoptions>a:2:{{s:10:"printintro";s:1:"0";s:17:"printlastmodified";s:1:"1";}}</displayoptions>\n    <revision>1</revision>\n    <timemodified>1743729253</timemodified>\n  </page>\n</activity>\n'''
    with open(os.path.join(new_page_path, "page.xml"), "w", encoding="UTF-8") as f:
        f.write(page_xml)

    # Add module.xml
    module_xml = f'''<?xml version="1.0" encoding="UTF-8"?>\n<module id="{new_module_id + 1}" version="2024100700">\n  <modulename>page</modulename>\n  <sectionid>{section_id}</sectionid>\n  <sectionnumber>1</sectionnumber>\n  <idnumber></idnumber>\n  <added>1743729253</added>\n  <score>0</score>\n  <indent>0</indent>\n  <visible>1</visible>\n  <visibleoncoursepage>1</visibleoncoursepage>\n  <visibleold>1</visibleold>\n  <groupmode>0</groupmode>\n  <groupingid>0</groupingid>\n  <completion>0</completion>\n  <completiongradeitemnumber>$@NULL@$</completiongradeitemnumber>\n  <completionpassgrade>0</completionpassgrade>\n  <completionview>0</completionview>\n  <completionexpected>0</completionexpected>\n  <availability>$@NULL@$</availability>\n  <showdescription>0</showdescription>\n  <downloadcontent>1</downloadcontent>\n  <lang></lang>\n  <tags></tags>\n</module>\n'''
    with open(os.path.join(new_page_path, "module.xml"), "w", encoding="UTF-8") as f:
        f.write(module_xml)

    # placeholders
    placeholders = {
        "inforef.xml": """<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<inforef>\n  <fileref/>\n  <graderef/>\n  <groupref/>\n  <groupingref/>\n  <userref/>\n</inforef>\n""",
        "roles.xml": """<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<roles></roles>\n""",
        "grades.xml": """<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<activity_grade_graders></activity_grade_graders>\n""",
        "grade_history.xml": """<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<activity_grade_history></activity_grade_history>\n"""
    }
    for filename, content in placeholders.items():
        with open(os.path.join(new_page_path, filename), "w", encoding="UTF-8") as f:
            f.write(content)

    # Insert <activity> block in moodle_backup.xml
    info_elem = backup_root.find("./information")
    if info_elem is not None:
        contents_elem = info_elem.find("contents")
        if contents_elem is None:
            contents_elem = ET.SubElement(info_elem, "contents")
        acts_elem = contents_elem.find("activities")
        if acts_elem is None:
            acts_elem = ET.SubElement(contents_elem, "activities")
        new_act = ET.SubElement(acts_elem, "activity")

        moduleid_elem = ET.SubElement(new_act, "moduleid")
        moduleid_elem.text = str(new_module_id + 1)

        sectionid_elem = ET.SubElement(new_act, "sectionid")
        sectionid_elem.text = str(section_id)

        modulename_elem = ET.SubElement(new_act, "modulename")
        modulename_elem.text = "page"

        title_elem = ET.SubElement(new_act, "title")
        title_elem.text = page_title

        directory_elem = ET.SubElement(new_act, "directory")
        directory_elem.text = f"activities/page_{new_module_id}"

        insub_elem = ET.SubElement(new_act, "insubsection")
        insub_elem.text = ""

        import io
        buffer = io.BytesIO()
        backup_tree.write(buffer, encoding="UTF-8", xml_declaration=True, short_empty_elements=False)
        content = buffer.getvalue().decode("UTF-8")
        content = content.replace('\'', '"')
        with open(backup_xml_path, "w", encoding="UTF-8") as f:
            f.write(content)
    else:
        print("Warning: <information> block not found in moodle_backup.xml, skipping activity insertion.")

    # Update <sequence>
    section_xml_path = os.path.join(section_path, "section.xml")
    if not os.path.isfile(section_xml_path):
        print("Error: section.xml not found.")
        sys.exit(1)

    s_tree = ET.parse(section_xml_path)
    s_root = s_tree.getroot()
    seq_elem = s_root.find("sequence")
    if seq_elem is None:
        print("Error: no <sequence> found in section.xml")
        sys.exit(1)
    existing_seq = seq_elem.text.strip() if seq_elem.text else ""
    if existing_seq:
        new_seq = f"{existing_seq},{new_module_id}"
    else:
        new_seq = str(new_module_id)
    seq_elem.text = new_seq
    s_tree.write(section_xml_path, encoding="UTF-8", xml_declaration=True, short_empty_elements=False)

    print(f"Added page with ID={new_module_id}, Title='{page_title}', Section={section_id}.")


def cli_main():
    import argparse
    parser = argparse.ArgumentParser(description="Add a new Page to an existing Moodle backup directory.")
    parser.add_argument("extracted_backup_dir")
    parser.add_argument("section_id")
    parser.add_argument("page_title")
    parser.add_argument("--page_description", default="Placeholder description")
    parser.add_argument("--page_content", default="Placeholder content")
    parser.add_argument("--output_dir", default=None)
    args = parser.parse_args()

    add_page_to_backup(
        extracted_backup_dir=args.extracted_backup_dir,
        section_id=args.section_id,
        page_title=args.page_title,
        page_description=args.page_description,
        page_content=args.page_content,
        output_dir=args.output_dir
    )

def add_page_from_tar(
    input_tar: str,
    output_tar: str,
    section_id: str,
    page_title: str,
    page_description: str = "Placeholder description",
    page_content: str = "Placeholder content"
) -> None:
    from .mbz_packager import with_extracted_tar
    with with_extracted_tar(input_tar, output_tar) as extracted_dir:
        add_page_to_backup(
            extracted_backup_dir=extracted_dir,
            section_id=section_id,
            page_title=page_title,
            page_description=page_description,
            page_content=page_content,
            output_dir=None
        )

if __name__ == "__main__":
    cli_main()
