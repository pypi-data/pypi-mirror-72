"""Setup for mercurial_all_paths."""

from setuptools import setup

VERSION = '1.2.1'
LONG_DESCRIPTION = open("README.rst").read()

setup(
    name="mercurial_all_paths",
    version=VERSION,
    author='Marcin Kasperski',
    author_email='Marcin.Kasperski@mekk.waw.pl',
    url='https://foss.heptapod.net/mercurial/mercurial-all_paths',
    description='Mercurial allpaths extension',
    long_description=LONG_DESCRIPTION,
    license='GNU General Public License v2 (GPLv2)',
    py_modules=[
        'mercurial_all_paths',
    ],
    install_requires=[
        'mercurial_extension_utils>=1.5.0',
    ],
    keywords="mercurial paths multi extension",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: DFSG approved',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Version Control'
        # 'Topic :: Software Development :: Version Control :: Mercurial',
    ],
    zip_safe=True)
