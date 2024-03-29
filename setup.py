from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='darktree',
    version='0.1.0',
    description='Yosys JSON Netlist Hierarchical Viewer',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/nturley/darktree',
    author='Neil Turley',
    author_email='neilpturley@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Digital Hardware Engineers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='netlist yosys hierarchy',
    packages=find_packages(exclude=['doc', 'test']),
    python_requires='>=3.0',
    install_requires=['QDarkStyle', 'PySide2'],
    package_data={
        'darktree': ['main.ui'],
    },
    entry_points={
        'console_scripts': [
            'darktree=darktree:main.main',
        ],
    },
)
