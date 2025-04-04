# Moodle Mod Tools

This project provides utilities for managing content within Moodle course backups (.mbz packages). It bundles command-line interfaces that generate new pages, sections, or bulk additions without requiring manual Moodle interactions.

## Features
- Bulk addition of modules to your Moodle course.
- Automatically generate new sections and pages.
- Pack and unpack .mbz Moodle backup files.
- Command-line usage for quick, script-friendly workflows.

## Installation
1. Install Python 3.7+.
2. Clone or download the code.
3. Run the following to install:
   ```bash
   pip install -e .
   ```

## Usage
- **bulk_adder.py**: Add multiple activities or resources in one go.
- **section_adder.py**: Create sections in a course.
- **page_adder.py**: Insert multiple pages with specified content.
- **mbz_packager.py**: Package or parse Moodle .mbz files.
- **cli.py**: Provides an interactive command-line interface to various subcommands.

Run each script with `-h` or `--help` for usage details and command arguments.

### CLI Usage
You can launch the main CLI by running:
```bash
python -m moodle_mod_tools.cli --help
```

## Example
```bash
python bulk_adder.py --input activities.csv --course backup.mbz
python section_adder.py --count 3 --title "Week" --course backup.mbz
python page_adder.py --pages pages.json --course backup.mbz
```

## Contributing
Contributions are welcome. Open an issue or submit a pull request.

## License
This project is open-source. See LICENSE for details.

## Support
For questions or help, please open an issue in this repository.
