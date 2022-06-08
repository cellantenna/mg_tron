import setuptools

from gui.helpers import VERSION

with open(
    "/home/djhunter67/Documents/work_worK_woRk_wOrk_Work/mg_tron/CHANGELOG.md",
    "r",
    encoding="utf-8",
) as fh:
    long_description = fh.read()

setuptools.setup(
    name="mgtron",
    version=VERSION,
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
        "Programming Language :: Python :: 3.10.5",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Hardware :: Universal Serial Bus (USB)",
        "Topic :: Terminals :: Serial",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=["dearpygui"],
    entry_points={
        "console_scripts": [
            "mgtron=gui:mg_tron_gui",
        ],
    },
    python_requires=">=3.10",
)
