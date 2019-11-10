#!/usr/bin/env python
"""
Setup script for docserver
=========================================

Call from command line as::

    python setup.py --help

to see the options available.
"""
from setuptools import setup
from setuptools import find_packages
from pkg_resources import parse_version, parse_requirements

try:
    import versioneer
    __version__ = versioneer.get_version()
    cmdclass = versioneer.get_cmdclass()
except AttributeError:
    __version__ = '0.0.0'
    cmdclass = None

__author__ = 'David Pugh'
__email__ = 'djpugh@gmail.com'

description = 'Document server using fastapi, starlett and uvicorn'
version = parse_version(__version__)
if parse_version(__version__) < parse_version('0.2.0'):
    development_status = 'Development Status :: 2 - Pre-Alpha'
elif parse_version(__version__).is_prerelease:
    development_status = 'Development Status :: 4 - Beta'
elif parse_version(__version__) >= parse_version('0.5.0'):
    development_status = 'Development Status :: 5 - Production/Stable'
elif parse_version(__version__) >= parse_version('1.0.0'):
    development_status = 'Development Status :: 6 - Mature'
elif parse_version(__version__) > parse_version('0.2.0'):
    development_status = 'Development Status :: 4 - Beta'
else:
    development_status = 'Development Status :: 1 - Planning'


with open('README.rst') as f:
    readme = f.read()
    f.close()

with open('requirements.txt') as f:
    install_requires = [u.name for u in parse_requirements(f.read())]

# We are going to take the approach that the requirements.txt specifies
# exact (pinned versions) to use but install_requires should only
# specify package names
# see https://caremad.io/posts/2013/07/setup-vs-requirement/
# install_requires should specify abstract requirements e.g.::
#
#   install_requires = ['requests']
#
# whereas the requirements.txt file should specify pinned versions to
# generate a repeatable environment

kwargs = dict(name='docsclient',
              version=__version__,
              author=__author__,
              author_email=__email__,
              packages=find_packages('src'),
              package_dir={'': 'src'},
              requires=[],
              install_requires=install_requires,
              provides=['docsclient'],
              test_suite='tests',
              url='https://github.com/djugh/docserver-client/',
              license="MIT",
              entry_points={},
              classifiers=[
                    development_status,
                    "Programming Language :: Python :: 3",
                    "License :: OSI Approved :: MIT License",
                    "Topic :: Software Development :: Documentation",
                    "Operating System :: OS Independent",
                    "Programming Language :: Python :: Implementation :: CPython"
                ],
              description=description,
              long_description=readme,
              package_data={'': []},
              project_urls={
                    'Source': 'https://github.com/djugh/docserver-client/',
                    'Tracker': 'https://github.com/djugh/docserver-client/issues'}
              )

if cmdclass is not None:
    kwargs['cmdclass'] = cmdclass

setup(**kwargs)
