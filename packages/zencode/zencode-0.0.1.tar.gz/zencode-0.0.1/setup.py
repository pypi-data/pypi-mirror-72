#/usr/bin/env python
import ast
import email.utils
import os
import re
import setuptools

here = os.path.dirname(__file__)

with open(os.path.join(here, 'README.md')) as readme:
    with open(os.path.join(here, 'CHANGES.md')) as changelog:
        long_description = readme.read() + '\n\n' + changelog.read()

# Copied from https://github.com/mgedmin/check-manifest/blob/master/setup.py
metadata = {}
with open(os.path.join(here, 'zencode.py')) as f:
    rx = re.compile('(__version__|__author__|__url__|__license__) = (.*)')
    for line in f:
        m = rx.match(line)
        if m:
            metadata[m.group(1)] = ast.literal_eval(m.group(2))
version = metadata['__version__']
author, author_email = email.utils.parseaddr(metadata['__author__'])
url = metadata['__url__']
license = metadata['__license__']

setuptools.setup(
    name='zencode',
    version=version,
    author=author,
    author_email=author_email,
    description='Z3-assisted x86 shellcode encoder',
    keywords=['z3', 'shellcode', 'x86 assembly'],
    license=license,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/jasperla/zencoder',
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Security',
    ],
    install_requires=[
        'z3-solver',
    ],
    extras_require={
        'dev': ['check-manifest''flake8'],
    },
    python_requires='>=3.6',
    py_modules=['zencode'],
    entry_points={
        'console_scripts': [
            'zencode = zencode:main',
        ],
    },
)
