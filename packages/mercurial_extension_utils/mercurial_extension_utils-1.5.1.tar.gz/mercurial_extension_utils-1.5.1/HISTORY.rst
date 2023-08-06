1.5.1
~~~~~~~~~~~~

Fixing various links as Atlassian killed Bitbucket.

1.5.0
~~~~~~~~~~~~

Polished support for python3 (tested with py 3.5-3.7 and with
mercurial 5.0-5.2). Seems to work as expected, yet to be verified
against all extensions.

Added ui_string function, helper to safely format argument
for ui.debug, ui.status etc.

1.4.0
~~~~~~~~~~~~

Preliminary support for python3 (with mercurial 5.0).
Exact APIs are yet to be verified (bstr/str decisions)
but (adapted) tests pass.

Tested against hg 5.0 and hg 4.9.

1.3.7
~~~~~~~~~~~~

Tested against hg 4.8 (no changes needed).

1.3.6
~~~~~~~~~~~~

Fixed problems with hg 4.7 (accomodating changed demandimport APIs).

1.3.5
~~~~~~~~~~~~

Formally tested with hg 4.5 and 4.6. 

Dropping test badges which don't work anymore from docs.

1.3.4
~~~~~~~~~~~~~

In-advance preparation for cmdutil.commands → registrar.commands
migration in core Mercurial API (see 46ba2cdda476 in hg-stable, likely
to be released in 4.3).

1.3.3
~~~~~~~~~~~~~

Updated links after bitbucket changes.

hg 4.1 and 4.2 added to tested versions.

1.3.2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

find_repositories_below doesn't fail in case some subdirectory is
unreadable. Instead, it simply skips it and continues to work
(realistic use-case: lost+found doesn't crash it anymore, but is
skipped…)

1.3.1
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Some tests were failing on mercurial 3.8, even more on 4.0
(actual code worked properly, just tests were faiing).

1.3.0
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Added enable_hook function (which detects whether hook is already
installed and withdraws in such a case).

Added inside_tortoisehg function (detecting that „we're running under
Tortoise”).

1.2.0
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Added meu.command (compatibility wrapper for cmdutil.command).


1.1.2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Added setconfig_list.

Various test improvements (including tox tests configured
to check various mercurial versions)


1.1.1
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Tests should work on any machine. Started Drone.io autotests.
Added some requirement.s

1.1.0
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

New functions: direct_import, direct_import_ext, and disable_logging.
Mostly taken from mercurial_keyring, but improved:
- imports handle dotted.modules
- disable_logging actually works for py2.6

1.0.1
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Test fixes, minor code cleanups.

1.0.0
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Documentation updates.

0.11.0
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Works on Windows (and handles normalizing paths to /-separator)

0.10.0
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

find_repositories_below

0.9.0
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

monkeypatch_method and monkeypatch_function

0.8.1
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Bugfix: TextFiller was hanging if run on pattern
not ending with {item}. Effectively mercurial hanged
while loading path patterns, for example. 

0.8.0
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``rgxp_configbool_items``
- ``suffix_configbool_items``

0.7.0
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``setconfig_dict``, 
- ``DirectoryPattern``
- ``TextFiller``

Actually used to simplify and improve ``mercurial_path_pattern``.

0.6.1
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Extra config support:
- ``suffix_config_items``,
- ``suffix_configlist_items``.

Actually used to simplify ``mercurial_dynamic_username``.

0.6.0
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

First public release:
- ``belongs_to_tree``, 
- ``belongs_to_tree_group``,
- ``rgxp_config_items``, 
- ``rgxp_configlist_items``
