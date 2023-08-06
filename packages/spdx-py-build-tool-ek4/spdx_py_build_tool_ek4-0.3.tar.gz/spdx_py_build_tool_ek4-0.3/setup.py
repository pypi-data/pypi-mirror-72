
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import imp, os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

metadata = imp.load_source(
    'metadata', os.path.join(ROOT_DIR, 'metadata.py'))

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("LICENSE", "r") as fh:
    license_description = fh.read()

setup_dict = dict(
    name=metadata.package,
    version=metadata.version,
    author=metadata.authors[0],
    author_email=metadata.emails[0],
    maintainer=metadata.authors[0],
    maintainer_email=metadata.emails[0],
    url=metadata.url,
    description=metadata.description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    license=license_description,
    entry_points={
        'console_scripts': [
            'spdx-build = build_tool.tool:entry_point',
        ],
    }
)


def main():
    setup(**setup_dict)


if __name__ == '__main__':
    main()
