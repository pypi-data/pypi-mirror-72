from setuptools import setup, find_packages
from io import open
from os import path

from filers2 import __version__

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

URL = 'https://github.com/matham/filers2'

setup(
    name='filers2',
    version=__version__,
    author='Matthew Einhorn',
    author_email='moiein2000@gmail.com',
    license='MIT',
    description=(
        'Video tools for recording experiments.'),
    long_description=long_description,
    url=URL,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    packages=find_packages(),
    install_requires=[
        'base_kivy_app', 'ffpyplayer', 'kivy', 'psutil', 'tree-config'],
    extras_require={
        'dev': ['pytest>=3.6', 'pytest-cov', 'flake8', 'sphinx-rtd-theme',
                'coveralls', 'trio', 'pytest-trio', 'pyinstaller'],
    },
    package_data={'filers2': ['*.kv', '**/*.kv']},
    project_urls={
        'Bug Reports': URL + '/issues',
        'Source': URL,
    },
    entry_points={
        'console_scripts': ['filers2=filers2.main:run_app']},
)
