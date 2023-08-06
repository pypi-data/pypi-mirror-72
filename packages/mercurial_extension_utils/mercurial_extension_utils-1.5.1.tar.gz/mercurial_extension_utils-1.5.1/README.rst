.. -*- mode: rst -*-

====================================
Mercurial Extension Utils
====================================

This module contains group of reusable functions, which I found useful
while writing various Mercurial extensions. 

.. contents::
   :local:
   :depth: 2

.. sectnum::

For Mercurial users
===========================

This module is of no direct use for you. It is internally used by various
Mercurial extensions  (like `Keyring`_,  `Dynamic Username`_ or `Path Pattern`_).

In most cases it should be installed automatically while you install
one of those extensions. See below for installation instructions in
more tricky cases (in particular, for information about installation
on Windows).

.. note::

   This document uses `Dynamic Username`_ in examples, but the
   same method should work for any other extension
   which requires ``mercurial_extension_utils``.

Installing on Linux/Unix
-------------------------------------------------------

In typical case ``mercurial_extension_utils`` should be installed
automatically, without requiring your attention, by commands like
``pip install mercurial_dynamic_username``. 

If for some reason it did not work, just install from PyPi with::

      pip install --user mercurial_extension_utils

or system-wide with::

      sudo pip install mercurial_extension_utils 

If you don't have ``pip``, try::

      sudo easy_install mercurial_extension_utils  

Upgrade to newer version using the same commands with ``--upgrade``
option added, for example::

      pip install --user --upgrade mercurial_extension_utils   

If you miss both ``pip``, and ``easy_install``, follow
recipe from `Installing for development`_ section.

Installing on Windows
-------------------------------------------------------

Windows Mercurial distributions (including most popular - and well
deserving that - TortoiseHg_) are not using system Python (in fact,
one may use Mercurial without installing Python at all), and
installing into bundled Python path is uneasy. To remedy that,
extensions utilizing this module handle additional methods of locating
it.

The following two methods of installation are available:

1. If you have some Python installed, you may still install both this module,
   and extension using it, from PyPi. For example::

      pip install mercurial_extension_utils   
      pip install mercurial_dynamic_username

   This will not (yet) make the module visible to your Mercurial, but
   you will get all the necessary files installed on your computer.

   Then activate the actual extension in charge by specifying it's
   path, for example by writing in your ``Mercurial.ini``::

     [extensions]
     mercurial_dynamic_username = C:/Python27/Lib/site-packages/mercurial_dynamic_username.py

   .. note:: 

      This works because ``mercurial_dynamic_username.py`` checks for
      ``mercurial_extension_utils.py`` saved in the same directory (and
      ``pip`` installs both modules in the same place). You can get
      the same effect by manually downloading all files into the same
      directory (using ``pip`` is more handy as it tracks dependencies
      and supports upgrades).

   Upgrade with ``pip`` by adding ``--upgrade`` to it's options.

2. If you don't have any Python, clone both the extension(s)
   repository and ``mercurial_extension_utils``` and put them in the same
   place, for example::

     cd c:\MercurialPlugins
     hg clone https://foss.heptapod.net/mercurial/mercurial-extension_utils/
     hg clone https://foss.heptapod.net/mercurial/mercurial-dynamic_username/

   Update repositories to newest tagged versions (untagged versions
   may be unstable or not working).   

   Activate the actual extension by specifying it's path, for example
   by writing in ``Mercurial.ini``::

     [extensions]
     mercurial_dynamic_username = C:/MercurialPlugins/mercurial-dynamic_username/mercurial_dynamic_username.py

   .. note::

      Directory names matter. This works because
      ``mercurial_dynamic_username.py`` checks for
      ``mercurial_extension_utils.py`` in
      ``../mercurial_extension_utils`` and ``../extension_utils``
      (relative to it's own location).

   To upgrade to new version, simply pull and update to newer tag.


.. _Installing for development:

Installing for development (or when everything else fails)
-----------------------------------------------------------

On Windows use second variant from the previous chapter (clone and activate
by path).

On Linux/Unix do the same. Clone all the necessary repositories, for example::

     cd ~/sources/
     hg clone https://foss.heptapod.net/mercurial/mercurial-extension_utils/
     hg clone https://foss.heptapod.net/mercurial/mercurial-dynamic_username/

then either make it visible to Python by repeating in every repo::

     pip install --user -e .

or activate the extension(s) by full path, by writing in ``~/.hgrc``
something like::

     [extensions]
     mercurial_dynamic_username = ~/sources/mercurial-dynamic_username/mercurial_dynamic_username.py


For Mercurial extensions developers
====================================

Available API
------------------------

Provided functions are mostly tiny utilities related to configuration
processing or location matching. They either extend Mercurial APIs a
bit (like function to iterate config items which match regexp), or
support tasks which aren't strictly Mercurial related, but happen
repeatably during extension writing (like matching repository root
against set of paths defined in the configuration).

Noticeable part of the library handles various incompatibilities
between Mercurial versions.

See docstrings for details.

Tests
-----------------------

Unit-tests can be run by::

    python -m unittest discover tests/

(against current version) or::

    tox

(against various versions of mercurial and python).

History
==================================================

See `HISTORY.rst`_

Repository, bug reports, enhancement suggestions
===================================================

Development is tracked on HeptaPod, see 
https://foss.heptapod.net/mercurial/mercurial-extension_utils/

Use issue tracker there for bug reports and enhancement
suggestions.

Thanks to Octobus_ and `Clever Cloud`_ for hosting this service.

Additional notes
====================================================

Check also `Mercurial extensions I wrote`_.



.. _Octobus: https://octobus.net/
.. _Clever Cloud: https://www.clever-cloud.com/


.. _Mercurial extensions I wrote: http://code.mekk.waw.pl/mercurial.html
.. _Mercurial: http://mercurial.selenic.com
.. _Dynamic Username: https://foss.heptapod.net/mercurial/mercurial-dynamic_username/
.. _Path Pattern: https://foss.heptapod.net/mercurial/mercurial-path_pattern/
.. _Keyring: https://foss.heptapod.net/mercurial/mercurial-keyring/
.. _HISTORY.rst: https://foss.heptapod.net/mercurial/mercurial-extension_utils/src/tip/HISTORY.rst

.. _TortoiseHg: http://tortoisehg.bitbucket.org/

