"""Setup form mercurial_extension_utils."""

from setuptools import setup

VERSION = '1.5.1'
LONG_DESCRIPTION = open("README.rst").read()
INSTALL_REQUIRES = []

setup(
    name="mercurial_extension_utils",
    version=VERSION,
    author='Marcin Kasperski',
    author_email='Marcin.Kasperski@mekk.waw.pl',
    url='https://foss.heptapod.net/mercurial/mercurial-extension_utils',
    description='Mercurial Extension Utils',
    long_description=LONG_DESCRIPTION,
    license='BSD',
    py_modules=['mercurial_extension_utils'],
    keywords="mercurial hg extension",
    install_requires=INSTALL_REQUIRES,
    # Giving up on python setup.py test, discovery too problematic
    # tests_require=TEST_REQUIRES,
    # test_suite='tests',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: DFSG approved',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Version Control',
        # 'Topic :: Software Development :: Version Control :: Mercurial',
    ],
    zip_safe=True)
