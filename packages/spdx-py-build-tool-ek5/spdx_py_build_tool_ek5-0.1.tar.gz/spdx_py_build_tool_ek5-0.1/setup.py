
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import imp, os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("LICENSE", "r") as fh:
    license_description = fh.read()

setup_dict = dict(
    name='spdx_py_build_tool_ek5',
    version='0.1',
    author='Ekong Obie Philip',
    author_email='ekongobiephilip@gmail.com',
    maintainer='Ekong Obie Philip',
    maintainer_email='ekongobiephilip@gmail.com',
    url='https://github.com/spdx/',
    description='Support a continuous integration (CI) generation of SPDX files by creating a plugins or extensions to build tools',
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
