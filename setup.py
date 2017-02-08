#! coding: utf-8
import sys
try:
    from setuptools import setup
except ImportError:
    from distribute_setup import use_setuptools
    use_setuptools()
    from setuptools import setup


py_version = sys.version_info[:2]



if py_version < (2, 7):
  print('google-api-python-client requires python version >= 2.7.',
        file=sys.stderr)
  sys.exit(1)

if (3, 1) <= py_version < (3, 3):
  print('google-api-python-client requires python3 version >= 3.3.',
        file=sys.stderr)
  sys.exit(1)

# All versions
install_requires = [
    'google-api-python-client',
    'setuptools'
]

if py_version < (3, 2):
    install_requires += [
        'futures',
        'configparser',
    ]

if py_version in [(2, 6), (3, 0)]:
    install_requires += [
        'importlib',
        'ordereddict',
    ]


setup(
    name='Translate',
    version = '0.0.1',
    description = 'Program to translate Android xml file.',
    author = [],
    author_email = 'computationalcore@gmail.com',
    url = '',
    packages = [],
    install_requires = install_requires,
)
