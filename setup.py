import codecs
import logging
import os
import pathlib
import setuptools

ROOT = pathlib.Path(__file__).resolve().parent.parent
WORKING = ROOT / "mg_tron"
loggick = logging.getLogger(name=__name__)


with open("CHANGELOG.md", "r", encoding="utf-8",) as fh:
    long_description = fh.read()

with open('requirements.txt') as fp:
    install_requires = fp.read()


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('VERSION'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")

loggick.info(f"setup.py: version: {get_version(f'{WORKING}/src/gui/helpers.py')}")
setuptools.setup(
    name="mgtron",
    version=get_version(f"{WORKING}/src/gui/helpers.py"),
    author="Hunter, Christerpher",
    author_email="djhunter67@gmail.com",
    description="GUI for proprietary signal generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mg_tron",
    project_urls={
        "Bug Tracker": "https://github.com/mg_tron/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Hardware :: Universal Serial Bus (USB)",
        "Topic :: Terminals :: Serial",
    ],
    packages=setuptools.find_packages(where="src", exclude=["tests", ]),
    package_dir={"": "src"},
    package_data={
        "gui": [
            "fonts/*", "db/*",
            "_configs/*",
            "*.ico",
            "*.md",
            "*.txt",
            "*.cfg",
            "*.rst",
        ]
    },
    entry_points={"console_scripts": ["mgtron=src.gui:mg_tron_gui", ]},
    python_requires=">=3.10",
    install_requires=install_requires,
)
