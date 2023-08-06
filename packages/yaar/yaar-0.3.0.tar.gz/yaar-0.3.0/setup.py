# -*- coding: utf-8 -*-

from setuptools import setup


def get_version_from_file():
    # get version number from __init__ file
    # before module is installed

    fname = 'yaar.py'
    with open(fname) as f:
        fcontent = f.readlines()
    version_line = [l for l in fcontent if 'VERSION' in l][0]
    return version_line.split('=')[1].strip().strip("'").strip('"')


def get_long_description_from_file():
    # content of README will be the long description

    fname = 'README.md'
    with open(fname) as f:
        fcontent = f.read()
    return fcontent


DESCRIPTION = """
Yet Another Asyncio Requets
""".strip()


setup(name='yaar',
      version=get_version_from_file(),
      author='Juca Crispim',
      author_email='juca@poraodojuca.net',
      url='https://pypi.python.org/pypi/yaar',
      description=DESCRIPTION,
      long_description=get_long_description_from_file(),
      long_description_content_type='text/markdown',
      py_modules=['yaar'],
      license='GPL',
      include_package_data=True,
      install_requires=['aiohttp>=3.5.4'],
      test_suite='tests',
      provides=['yaar'],)
