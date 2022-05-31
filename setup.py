import setuptools

with open("CHANGELOG.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mgtron",
    version="0.9.0",
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
        "Programming Language :: Python :: 3",
        "License :: Proprietary",
        "Operating System :: Linux",
        "Framework :: DearPyGUI",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.10",
)