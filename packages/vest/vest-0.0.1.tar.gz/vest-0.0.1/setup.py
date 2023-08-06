from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='vest',
    version='0.0.1',
    author='mattf1n',
    long_description=long_description,
    url='https://github.com/mattf1n/vest',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'robin_stocks',
    ],
    entry_points='''
        [console_scripts]
        vest=vest.cli:cli
    ''',
)
