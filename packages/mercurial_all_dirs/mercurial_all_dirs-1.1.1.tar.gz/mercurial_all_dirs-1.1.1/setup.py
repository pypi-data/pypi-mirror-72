"""Setup for mercurial_all_dirs."""

from setuptools import setup

VERSION = '1.1.1'
LONG_DESCRIPTION = open("README.rst").read()

setup(
    name="mercurial_all_dirs",
    version=VERSION,
    author='Marcin Kasperski',
    author_email='Marcin.Kasperski@mekk.waw.pl',
    url='https://foss.heptapod.net/mercurial/mercurial-all_dirs',
    description='Mercurial All Dirs Extension',
    long_description=LONG_DESCRIPTION,
    license='BSD',
    py_modules=[
        'mercurial_all_dirs',
    ],
    install_requires=[
        'mercurial_extension_utils>=1.5.0',
    ],
    keywords="mercurial subdirs multi alias",
    classifiers=[
        'Development Status :: 4 - Beta',
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
