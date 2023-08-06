"""Setup for mercurial_path_pattern."""

from setuptools import setup

VERSION = '1.4.1'
LONG_DESCRIPTION = open("README.rst").read()

setup(
    name="mercurial_path_pattern",
    version=VERSION,
    author='Marcin Kasperski',
    author_email='Marcin.Kasperski@mekk.waw.pl',
    url='https://foss.heptapod.net/mercurial/mercurial-path_pattern',
    description='Mercurial Path Pattern Extension',
    long_description=LONG_DESCRIPTION,
    license='BSD',
    py_modules=[
        'mercurial_path_pattern',
    ],
    install_requires=[
        'mercurial_extension_utils>=1.5.0',
    ],
    keywords="mercurial hg path alias",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: DFSG approved',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Version Control'
        # 'Topic :: Software Development :: Version Control :: Mercurial',
    ],
    zip_safe=True)
