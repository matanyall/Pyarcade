from setuptools import setup

# This script informs pip/conda/python how to install our package when requested.
# The important part is the entry_point. This informs the installer to make the run_pyarcade
# function of the start.py file in the pyarcade package to be callable via "pyarcade"
setup(
    name='pyarcade',
    version='0.0.1',
    description='',
    packages=["pyarcade", "pyarcade.games"],
    entry_points={"console_scripts": ["pyarcade = pyarcade.start:run_pyarcade"]},
    test_suite="tests"
)