import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="moodle_mod_tools",
    version="0.1.0",
    author="Your Name",
    author_email="you@example.com",
    description="A suite of tools for manipulating Moodle MBZ backups",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
)