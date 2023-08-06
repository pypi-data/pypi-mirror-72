# -*- coding: utf-8 -*-
#
# mercurial extension utils: library supporting mercurial extensions
# writing
#
# Copyright (c) 2015 Marcin Kasperski <Marcin.Kasperski@mekk.waw.pl>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. The name of the author may not be used to endorse or promote products
#    derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# See README.rst for more details.

"""
Utility functions useful during Mercurial extension writing

Mostly related to configuration processing, path matching and similar
activities.  I extracted this module once I noticed a couple of my
extensions need the same or similar functions.

Part of this module is about wrapping some incompatibilities between
various Mercurial versions.

Note: file-related functions defined here use / as path separator,
even on Windows.  Backslashes in params should usually work too, but
returned paths are always /-separated.

Documentation examples in this module use Unix paths and Python3
syntax, see tests/*doctests.py for versions with Python2 and/or
Windows examples.

On Python3 we mostly follow Mercurial's own idea of using binary
strings, wrapped as bytestr where useful.
"""

from __future__ import print_function  # For doctests
from mercurial.i18n import _
import re
import os
import sys
import types
from collections import deque

# pylint: disable=line-too-long,invalid-name

###########################################################################
# Tiny py2/py3 compatibility layer (used internally)
###########################################################################

# We mostly defer to Mercurial's own compatibility layer - if we are
# on py3, it exists (elsewhere no chances for working hg, versions
# without meecurial.pycompat don't install on py3), if we are on py2
# it may exist or not depending on Mercurial version. It it doesn't or
# is incomplete, we fix missing parts.

# Trick to avoid separate file craetion
_compat_name = 'mercurial_extension_utils.pycompat'
pycompat = types.ModuleType(_compat_name)
# pycompat = imp.new_module(_compat_name)
sys.modules[_compat_name] = pycompat

pycompat.identity = lambda a: a

try:
    from mercurial import pycompat as _pycompat

    for func in [           # py2      / py3
            'ispy3',        # False    / True
            'bytestr',      # str      / bytes subclass with some glue to make it more py2str-like
                            #            and smart constructor which accepts bytestr, bytes and str
            'unicode',      # unicode  / str
            'bytechr',      # chr      / chr(x).encode()  (more efficient equiv)
            'maybebytestr', # identity / upgrade bytes to bytestr, on nonbytes identity
            'sysbytes',     # identity / x.encode(utf-8)
            'sysstr',       # identity / make it native str, safely (convert bytes to str, leave str)
            'strkwargs',    # identity / if any key is bytes, make it str
            'byteskwargs',  # identity / if nay key is str, make it bytes
    ]:
        if hasattr(_pycompat, func):
            setattr(pycompat, func, getattr(_pycompat, func))
except ImportError:
    pass

if not hasattr(pycompat, 'ispy3'):
    pycompat.ispy3 = (sys.version_info[0] >= 3)
if not pycompat.ispy3:
    # Only on py2 we can be on old mercurial where pycompat doesn't exist,
    # or has less functions. Here we fix missing bits (that's mostly copy
    # and paste from pycompat in modern mercurial).
    if not hasattr(pycompat, 'bytechr'):
        pycompat.bytechr = chr
    if not hasattr(pycompat, 'bytestr'):
        pycompat.bytestr = str
    if not hasattr(pycompat, 'maybebytestr'):
        pycompat.maybebytestr = pycompat.identity
    if not hasattr(pycompat, 'iterbytestr'):
        pycompat.iterbytestr = iter
    if not hasattr(pycompat, 'strkwargs'):
        pycompat.strkwargs = pycompat.identity
    if not hasattr(pycompat, 'byteskwargs'):
        pycompat.byteskwargs = pycompat.identity
    if not hasattr(pycompat, 'sysbytes'):
        pycompat.sysbytes = pycompat.identity
    if not hasattr(pycompat, 'sysstr'):
        pycompat.sysstr = pycompat.identity
    if not hasattr(pycompat, 'unicode'):
        pycompat.unicode = unicode

if pycompat.ispy3:

    def dict_iteritems(dic):
        return dic.items()

    if sys.version_info < (3, 7):

        def re_escape(txt):
            # Pythons 3.5 and 3.6 fail on bytestrings. Let's fix it similarly to 3.7 fix
            if isinstance(txt, str):
                return re.escape(txt)
            else:
                v = str(txt, 'latin1')
                return re.escape(v).encode('latin1')

    else:

        def re_escape(txt):
            return re.escape(txt)

else:

    def dict_iteritems(dic):
        return dic.iteritems()

    def re_escape(txt):
        return re.escape(txt)


###########################################################################
# Logging support
###########################################################################

if pycompat.ispy3:
    def _log_normalize(args):
        return tuple(pycompat.bytestr(arg) for arg in args)
else:
    _log_normalize = pycompat.identity


def ui_string(message, *args):
    """
    Idiomatically equivalent to::

        return _(message) % args

    but handles idiosyncracies of mercurial.ui logging under py3 where
    bytestring and byteargs are expected, and None's and normal strings
    cause problems.

    Typical use (replace debug with any other method):

    >>> import mercurial.ui; ui = mercurial.ui.ui()
    >>> ui.debug(ui_string("Simple text"))
    >>> ui.debug(ui_string(b"Simple binary"))
    >>> ui.debug(ui_string("This is %s and %s and %s", b'bin', u'txt', None))
    >>> ui.debug(ui_string(b"This is %s and %s and %s", b'bin', u'txt', None))

    This works because we reasonably create binary strings, as ui expects:

    >>> ui_string("Simple text")
    b'Simple text'
    >>> ui_string(b"Simple binary")
    b'Simple binary'
    >>> ui_string("This is %s and %s and %s", b'bin', u'txt', None)
    b'This is bin and txt and None'
    >>> ui_string(b"This is %s and %s and %s", b'bin', u'txt', None)
    b'This is bin and txt and None'
    """
    # _ seems to handle normalization, so we don't have to.
    return _(message) % _log_normalize(args)



###########################################################################
# Directory matching in various shapes
###########################################################################


def normalize_path(path):
    """
    Converts given path to absolute, /-separated form. That means:
    - expanding ~
    - converting to absolute
    - (on Windows) converting backslash to slash
    - dropping final slash (if any)

    >>> normalize_path("~/src")
    '/home/lordvader/src'
    >>> normalize_path("/some/where")
    '/some/where'
    >>> normalize_path("/some/where/")
    '/some/where'
    >>> normalize_path("../../../some/where")
    '/home/lordvader/some/where'

    In case of python3, result is also forced to bytestr if not in such
    form yet:

    >>> type(normalize_path("~/src"))
    <class 'mercurial.pycompat.bytestr'>
    >>> type(normalize_path(b"~/src"))
    <class 'mercurial.pycompat.bytestr'>

    This way bytes input is also properly handled:

    >>> normalize_path(b"~/src")
    '/home/lordvader/src'
    >>> normalize_path(b"/some/where/")
    '/some/where'
    """
    reply = pycompat.bytestr(
        os.path.abspath(os.path.expanduser(path)))
    if os.name == 'nt':
        reply = reply.replace(b'\\', b'/')
    return pycompat.bytestr(reply.rstrip(b'/'))


def belongs_to_tree(child, parent):
    """Checks whether child lies anywhere inside parent directory tree.

    Child should be absolute path, parent will be tlida expanded and
    converted to absolute path (this convention is caused by typical
    use case, where repo.root is compared against some user-specified
    directory).

    On match, matching parent is returned (it matters if it was
    sanitized).

    >>> belongs_to_tree("/tmp/sub/dir", "/tmp")
    '/tmp'
    >>> belongs_to_tree("/tmp", "/tmp")
    '/tmp'
    >>> belongs_to_tree("/tmp/sub", "/tmp/sub/dir/../..")
    '/tmp'

    On mismatch None is returned.

    >>> belongs_to_tree("/usr/sub", "/tmp")

    Tilda expressions are allowed in parent specification:

    >>> home_work_src = os.path.join(os.environ["HOME"], "work", "src")
    >>> belongs_to_tree(home_work_src, "~/work")
    '/home/lordvader/work'
    >>> belongs_to_tree("/home/lordvader/devel/webapps", "~lordvader/devel")
    '/home/lordvader/devel'

    Note: even on Windows, / is used as path separator (both on input,
    and on output).

    On Python3 both kinds of strings are handled as long as arguments are compatible
    and result is forced to bytestr:

    >>> x = belongs_to_tree(b"/tmp/sub/dir", b"/tmp")
    >>> x
    '/tmp'
    >>> type(x)
    <class 'mercurial.pycompat.bytestr'>
    >>> x = belongs_to_tree(b"/usr/sub", b"/tmp")
    >>> x

    >>> x = belongs_to_tree(b"/home/lordvader/devel/webapps", b"~lordvader/devel")
    >>> x
    '/home/lordvader/devel'
    >>> type(x)
    <class 'mercurial.pycompat.bytestr'>

    :param child: tested directory (preferably absolute path)
    :param parent: tested parent (will be tilda-expanded, so things
        like ~/work are OK)

    :return: expanded canonicalized parent on match, None on mismatch
    """
    parent = normalize_path(parent)
    child = normalize_path(child)
    # os.path.commonprefix is case-sensitive, on Windows this makes things crazy
    # pfx = normalize_path(os.path.commonprefix([child, parent]))
    # return pfx == true_parent and true_parent or None
    if os.name != 'nt':
        matches = child == parent or child.startswith(parent + b'/')
    else:
        lower_child = child.lower()
        lower_parent = parent.lower()
        matches = lower_child == lower_parent or lower_child.startswith(lower_parent + b'/')
    return matches and parent or None


def belongs_to_tree_group(child, parents):
    """
    Similar to belongs_to_tree, but handles list of candidate parents.

    >>> belongs_to_tree_group("/tmp/sub/dir", ["/bin", "/tmp"])
    '/tmp'
    >>> belongs_to_tree_group("/tmp", ["/tmp"])
    '/tmp'
    >>> belongs_to_tree_group("/tmp/sub/dir", ["/bin", "~/src"])

    Returns longest match if more than one parent matches.

    >>> belongs_to_tree_group("/tmp/sub/dir", ["/tmp", "/bin", "/tmp", "/tmp/sub"])
    '/tmp/sub'

    where length is considered after expansion

    >>> belongs_to_tree_group("/home/lordvader/src/apps", ["~/src", "/home/lordvader"])
    '/home/lordvader/src'

    Note: even on Windows, / is used as path separator (both on input,
    and on output).

    On Py3 both kinds of strings are handled as long as arguments are compatible:

    >>> x = belongs_to_tree_group(b"/tmp/sub/dir", [b"/bin", b"/tmp"])
    >>> x
    '/tmp'
    >>> type(x)
    <class 'mercurial.pycompat.bytestr'>

    >>> belongs_to_tree_group(b"/home/lordvader/src/apps", [b"~/src", b"/home/lordvader"])
    '/home/lordvader/src'

    :param child: tested directory (preferably absolute path)
    :param parents: tested parents (list or tuple of directories to
        test, will be tilda-expanded)
    """
    child = normalize_path(child)
    longest_parent = pycompat.bytestr(b'')
    for parent in parents:
        canon_path = belongs_to_tree(child, parent)
        if canon_path:
            if len(canon_path) > len(longest_parent):
                longest_parent = canon_path
    return longest_parent and longest_parent or None


class DirectoryPattern(object):
    """
    Represents directory name pattern, like ``~/src/{suffix}``, or
    ``/opt/repos/(group)/{suffix}``, and let's match agains such pattern.

    Pattern mini-language:
    - tildas (``~`` and ``~user``) are expanded
    - ``(something)`` matches any part which does not contain directory separator
    - ``{something}`` greedily matches anything, including directory separators

    Constructed pattern can be used to match against, succesfull match extracts
    all marked fragments.

    On Windows comparison is case-insensitive, on Unix/Linux case matters.

    >>> pat = DirectoryPattern('~/src/{suffix}')
    >>> pat.is_valid()
    True
    >>> pat.search("/opt/repos/abcd")
    >>> pat.search("~/src/repos/in/tree")
    {'suffix': 'repos/in/tree'}
    >>> pat.search("/home/lordvader/src/repos/here" if os.system != 'nt' else "c:/users/lordvader/src/repos/here")
    {'suffix': 'repos/here'}
    >>> pat.search("/home/lordvader/src")

    >>> pat = DirectoryPattern('~lordvader/devel/(item)')
    >>> pat.search("/opt/repos/abcd")
    >>> pat.search("~/devel/libxuza")
    {'item': 'libxuza'}
    >>> pat.search("~/devel/libs/libxuza")
    >>> pat.search("/home/lordvader/devel/webapp")
    {'item': 'webapp'}
    >>> pat.search("/home/lordvader/devel")

    >>> from pprint import pprint  # Help pass doctests below

    >>> pat = DirectoryPattern('/opt/repos/(group)/{suffix}')
    >>> pat.search("/opt/repos/abcd")
    >>> pprint(pat.search("/opt/repos/libs/abcd"))
    {'group': 'libs', 'suffix': 'abcd'}
    >>> pprint(pat.search("/opt/repos/apps/mini/webby"))
    {'group': 'apps', 'suffix': 'mini/webby'}

    >>> pat = DirectoryPattern('/opt/repos/(group/{suffix}')
    >>> pat.is_valid()
    False
    >>> pat.search('/opt/repos/some/where')

    Fixed strings can also be used and work reasonably:

    >>> pat = DirectoryPattern('~/dev/acme')
    >>> pat.is_valid()
    True
    >>> pat.search('/home/lordvader/dev/acme')
    {}
    >>> pat.search('/home/lordvader/dev/acme/')
    {}
    >>> pat.search('/home/lordvader/dev/acme/subdir')
    >>> pat.search('/home/lordvader/dev')

    On Py3 binary strings can be used as well (and results are wrapped
    as bytestr)::

    >>> pat = DirectoryPattern(b'~/src/{suffix}')
    >>> pat.is_valid()
    True
    >>> pat.search(b"/opt/repos/abcd")
    >>> x = pat.search(b"~/src/repos/in/tree")
    >>> x
    {'suffix': 'repos/in/tree'}
    >>> type(x['suffix'])
    <class 'mercurial.pycompat.bytestr'>
    >>> [type(t) for t in x.keys()]
    [<class 'str'>]

    >>> pat.search(b"/home/lordvader/src/repos/here" if os.system != 'nt' else b"c:/users/lordvader/src/repos/here")
    {'suffix': 'repos/here'}
    >>> pat.search(b"/home/lordvader/src")

    >>> pat = DirectoryPattern(b'~lordvader/devel/(item)')
    >>> pat.search(b"/opt/repos/abcd")
    >>> pat.search(b"~/devel/libxuza")
    {'item': 'libxuza'}
    >>> pat.search(b"~/devel/libs/libxuza")
    >>> pat.search(b"/home/lordvader/devel/webapp")
    {'item': 'webapp'}
    >>> pat.search(b"/home/lordvader/devel")

    """

    # Regexps used during pattern parsing
    _re_pattern_lead = re.compile(b' ^ ([^{}()]*)   ([({]) (.*) $', re.VERBOSE)
    _re_closure = {b'{': re.compile(b'^ ([a-zA-Z_]+) [}]    (.*) $', re.VERBOSE),
                   b'(': re.compile(b'^ ([a-zA-Z_]+) [)]    (.*) $', re.VERBOSE)}
    # (text inside (braces) or {braces} is restricted as it is used within regexp

    # Regexp snippets used to match escaped parts
    _re_match_snippet = {b'{': b'.+',
                         b'(': b'[^/\\\\]+'}

    def __init__(self, pattern_text, ui=None):
        """Parses given pattern. Doesn't raise, in case of invalid patterns
        creates object which does not match anything and warns.

        :param pattern_text: parsed pattern
        :param ui: (optional) mercurial ui object, if given, used for debugging
        """
        self.pattern_text = text = normalize_path(pattern_text)
        self._pattern_re = None    # Will stay such if we fail somewhere here

        # Convert pattern to regexp
        rgxp_text = b'^'
        while text:
            match = self._re_pattern_lead.search(text)
            if match:
                prefix, open_char, text = match.group(1), match.group(2), match.group(3)
                match = self._re_closure[open_char].search(text)
                if not match:
                    if ui:
                        ui.warn(ui_string("Invalid directory pattern: %s\n",
                                           pattern_text))
                    return
                group_name, text = match.group(1), match.group(2)
                rgxp_text += re_escape(prefix)
                rgxp_text += b'(?P<' + group_name + b'>' + self._re_match_snippet[open_char] + b')'
            else:
                rgxp_text += re_escape(text)
                text = b''
        rgxp_text += b'$'
        if ui:
            ui.debug(ui_string("meu: Pattern %s translated into regexp %s\n",
                                pattern_text, rgxp_text))
        try:
            self._pattern_re = re.compile(rgxp_text, os.name == 'nt' and re.IGNORECASE or 0)
        except:     # pylint:disable=bare-except
            if ui:
                ui.warn(ui_string("Invalid directory pattern: %s\n",
                                   pattern_text))

    def is_valid(self):
        """Can be used to check whether object was properly constructed"""
        return bool(self._pattern_re)

    def search(self, tested_path):
        """
        Matches given directory against the pattern.  On match,
        returns dictionary of all named elements.  On mismatch,
        returns None

        :param tested_path: path to check, will be tilda-expanded and
            converted to abspath before comparison
        :return: Dictionary mapping all ``{brace}`` and ``(paren)`` parts to matched
            items (on py3 represented as bytestr).
        """
        if not self._pattern_re:
            return
        exp_tested_path = normalize_path(tested_path)
        match = self._pattern_re.search(exp_tested_path)
        if match:
            return dict((key, pycompat.maybebytestr(value))
                        for key, value in dict_iteritems(match.groupdict()))
            # return match.groupdict()
        else:
            return None


###########################################################################
# Text substitution
###########################################################################

class TextFiller(object):
    r'''
    Handle filling patterns like 'some/{thing}/{else}' with values.
    Comparing to standard library ``.format`` offers a bit different
    syntax, related to actual extension-writing problems, and different
    ways of error handling.

    In simplest form, it just replaces any ``{name}`` with value of ``name``, as-is

    >>> tf = TextFiller('{some}/text/to/{fill}')
    >>> tf.fill(some='prefix', fill='suffix')
    'prefix/text/to/suffix'
    >>> tf.fill(some='/ab/c/d', fill='x')
    '/ab/c/d/text/to/x'

    Values can be repeated and unnecessary keys are ignored:

    >>> tf = TextFiller('{some}/text/to/{some}')
    >>> tf.is_valid()
    True
    >>> tf.fill(some='val')
    'val/text/to/val'
    >>> tf.fill(some='ab/c/d', fill='x')
    'ab/c/d/text/to/ab/c/d'

    It is also possible to perform simple substitutions, for example
    ``{name:/=-} takes value of ``name``, replaces all slashes with
    minuses, and fills output with the resulting value

    >>> tf = TextFiller('{prefix:_=___}/goto/{suffix:/=-}')
    >>> tf.fill(prefix='some_prefix', suffix='some/long/suffix')
    'some___prefix/goto/some-long-suffix'

    Substitution can be also used to replace multi-character sequences,
    and replacement can be empty:

    >>> tf = TextFiller('{prefix:/home/=}/docs/{suffix:.txt=.html}')
    >>> tf.fill(prefix='/home/joe', suffix='some/document.txt')
    'joe/docs/some/document.html'

    and chained to replace more than one thing:

    >>> tf = TextFiller(r'/goto/{item:/=-:\=_}/')
    >>> tf.fill(item='this/is/slashy')
    '/goto/this-is-slashy/'
    >>> tf.fill(item=r'this\is\back')
    '/goto/this_is_back/'
    >>> tf.fill(item=r'this/is\mixed')
    '/goto/this-is_mixed/'

    The same parameter can be used in various substitutions:

    >>> tf = TextFiller(r'http://go.to/{item:/=-}, G:{item:/=\}, name: {item}')
    >>> print(tf.fill(item='so/me/thing'))
    b'http://go.to/so-me-thing, G:so\\me\\thing, name: so/me/thing'

    Errors are handled by returning None (and warning if ui is given), both
    in case of missing key:

    >>> tf = TextFiller('{some}/text/to/{fill}')
    >>> tf.fill(some='prefix', badfill='suffix')

    and of bad pattern:

    >>> tf = TextFiller('{some/text/to/{fill}')
    >>> tf.is_valid()
    False
    >>> tf.fill(some='prefix', fill='suffix')

    >>> tf = TextFiller('{some}/text/to/{fill:}')
    >>> tf.is_valid()
    False
    >>> tf.fill(some='prefix', fill='suffix')

    On Py3 binary strings are in fact used and preferred:

    >>> tf = TextFiller(b'{some}/text/to/{fill}')
    >>> tf.fill(some=b'prefix', fill=b'suffix')
    'prefix/text/to/suffix'
    >>> tf.fill(some=b'/ab/c/d', fill=b'x')
    '/ab/c/d/text/to/x'

    >>> tf = TextFiller(b'{some}/text/to/{some}')
    >>> tf.is_valid()
    True
    >>> tf.fill(some=b'val')
    'val/text/to/val'
    >>> tf.fill(some=b'ab/c/d', fill=b'x')
    'ab/c/d/text/to/ab/c/d'

    '''

    # Regexps used during parsing
    _re_pattern_lead = re.compile(b' ^ ([^{}]*) [{] (.*) $', re.VERBOSE)
    _re_pattern_cont = re.compile(b'''
    ^  ([a-zA-Z][a-zA-Z0-9_]*)          # name (leading _ disallowed on purpose)
       ((?: : [^{}:=]+ = [^{}:=]* )*)   # :sth=else  substitutions
       [}]
       (.*)                        $ ''', re.VERBOSE)
    _re_sub = re.compile(b'^ : ([^{}:=]+) = ([^{}:=]*)  (.*)  $', re.VERBOSE)

    def __init__(self, fill_text, ui=None):
        def percent_escape(val):
            """Escape %-s in given text by doubling them."""
            return pycompat.bytestr(val.replace(b'%', b'%%'))

        text = self.fill_text = pycompat.bytestr(fill_text)
        # Replacement text. That's just percent 'some %(abc)s text' (we use % not '{}' to
        # leave chances of working on python 2.5). Empty value means I am broken
        self._replacement = None
        # List of substitutions, tuples:
        #   result synthetic name,
        #   base field name
        #   [(from, to), (from, to), ...]   list of substitutions to make
        self._substitutions = []

        replacement = pycompat.bytestr('')
        synth_idx = 0
        while text:
            match = self._re_pattern_lead.search(text)
            if match:
                replacement += percent_escape(match.group(1))
                text = pycompat.bytestr(match.group(2))
                match = self._re_pattern_cont.search(text)
                if not match:
                    if ui:
                        ui.warn(ui_string("Bad replacement pattern: %s\n",
                                           fill_text))
                    return
                name, substs, text = pycompat.bytestr(match.group(1)), pycompat.bytestr(match.group(2)), pycompat.bytestr(match.group(3))
                if substs:
                    fixups = []
                    while substs:
                        match = self._re_sub.search(substs)
                        if not match:
                            if ui:
                                ui.warn(ui_string("Bad replacement pattern: %s\n",
                                                   fill_text))
                            return
                        src, dest, substs = pycompat.bytestr(match.group(1)), pycompat.bytestr(match.group(2)), pycompat.bytestr(match.group(3))
                        fixups.append((src, dest))
                    synth_idx += 1
                    synth = b"_" + pycompat.bytestr(str(synth_idx))
                    self._substitutions.append((synth, name, fixups))
                    name = synth
                replacement += b'%(' + name + b')s'
            else:
                replacement += percent_escape(text)
                text = b''
        # Final save
        if ui:
            ui.debug(ui_string("meu: Replacement %s turned into expression %s\n",
                                fill_text, replacement))
        self._replacement = replacement

    def is_valid(self):
        """Returns whether object is in correct state, or broken"""
        return bool(self._replacement)

    def fill(self, **kwargs):
        """Fills text with given arguments. If something is broken (missing key, broken pattern)
        returns None"""
        if not self._replacement:
            return None

        # TODO: maybe byteskwargs?
        bstr_args = dict((pycompat.bytestr(key), pycompat.bytestr(value))
                         for key, value in dict_iteritems(kwargs))

        try:
            for made_field, src_field, fixups in self._substitutions:
                value = bstr_args[src_field]
                for src, dest in fixups:
                    value = value.replace(src, dest)
                bstr_args[made_field] = value
            return pycompat.bytestr(self._replacement % bstr_args)
        except:  # pylint:disable=bare-except
            return None


###########################################################################
# Config support
###########################################################################

def setconfig_item(ui, section, name, value):
    """
    Mostly equivalent to ```ui.setconfig(section, name, value)```, but
    under Py3 avoids errors raised if any of the params is unicode.

    >>> import mercurial.ui; ui = mercurial.ui.ui()
    >>> setconfig_item(ui, b"s1", b'a', b'va')
    >>> setconfig_item(ui, b"s1", b'b', 7)
    >>> setconfig_item(ui, "s2", 'a', 'v2a')
    >>> setconfig_item(ui, "s2", 'b', 8)

    >>> ui.config(b"s1", b'a')
    b'va'
    >>> ui.config(b"s1", b'b')
    7
    >>> x = ui.config(b"s2", b'a')
    >>> x
    'v2a'
    >>> type(x)
    <class 'mercurial.pycompat.bytestr'>
    >>> ui.config(b"s2", b'b')
    8
    """
    if isinstance(value, pycompat.unicode):
        value = pycompat.bytestr(value)
    ui.setconfig(pycompat.bytestr(section),
                 pycompat.bytestr(name),
                 value)


def setconfig_dict(ui, section, items):
    """
    Set's many configuration items with one call. Defined mostly
    to make some code (including doctests below) a bit more readable.

    Note that binary strings are mostly used, in sync with Mercurial 5.0
    decision to use those as section names and keys in ui.config…

    >>> import mercurial.ui; ui = mercurial.ui.ui()
    >>> setconfig_dict(ui, b"sect1", {b'a': 7, b'bbb': 'xxx', b'c': b'-'})
    >>> setconfig_dict(ui, b"sect2", {b'v': 'vvv'})
    >>> ui.config(b"sect1", b'a')
    7
    >>> x = ui.config(b"sect2", b'v')
    >>> x
    'vvv'
    >>> type(x)
    <class 'mercurial.pycompat.bytestr'>

    … but we support some reasonable conversions:

    >>> setconfig_dict(ui, "sect11", {'aa': 7, 'bbbb': 'xxx', 'cc': '-'})
    >>> setconfig_dict(ui, "sect22", {'vv': 'vvv'})
    >>> ui.config(b"sect11", b'aa')
    7
    >>> x = ui.config(b"sect22", b'vv')
    >>> x, type(x)
    ('vvv', <class 'mercurial.pycompat.bytestr'>)

    :param section: configuration section tofill
    :param items: dictionary of items to set
    """
    section = pycompat.bytestr(section)

    for key, value in dict_iteritems(items):
        setconfig_item(ui, section, key, value)


def setconfig_list(ui, section, items):
    """
    Alternative form of setting many configuration items with one call.
    Here items are given as list of key,value pairs. Contrary to
    setconfig_dict, this guarantees ordering.

    >>> import mercurial.ui; ui = mercurial.ui.ui()
    >>> setconfig_list(ui, b"sect1",
    ...     [(b'a', 7), (b'bbb', b'xxx'), (b'c', b'-'), (b'a', 8)])
    >>> setconfig_list(ui, b"sect2", [(b'v', b'vvv')])
    >>> ui.config(b"sect1", b'a')
    8
    >>> ui.config(b"sect2", b'v')
    b'vvv'

    We also support normal strings to some degree:

    >>> import mercurial.ui; ui = mercurial.ui.ui()
    >>> setconfig_list(ui, "sect11",
    ...     [('a', 7), ('bbb', 'xxx'), ('c', '-'), ('a', 8)])
    >>> setconfig_list(ui, "sect22", [('v', 'vvv')])
    >>> ui.config(b"sect11", b'a')
    8
    >>> x = ui.config(b"sect22", b'v')
    >>> x
    'vvv'
    >>> type(x)
    <class 'mercurial.pycompat.bytestr'>

    :param section: configuration section tofill
    :param items: dictionary of items to set
    """
    section = pycompat.bytestr(section)

    for key, value in items:
        setconfig_item(ui, section, key, value)


def rgxp_config_items(ui, section, rgxp):
    r'''
    Yields items from given config section which match given regular
    expression.

    >>> import mercurial.ui; ui = mercurial.ui.ui()
    >>> setconfig_list(ui, "foo", [
    ...         ("pfx-some-sfx", "ala, ma kota"),
    ...         ("some.nonitem", "bela nie"),
    ...         ("x", "yes"),
    ...         ("pfx-other-sfx", 4)
    ... ])
    >>> setconfig_list(ui, "notfoo", [
    ...         ("pfx-some-sfx", "bad"),
    ...         ("pfx-also-sfx", "too"),
    ... ])
    >>>
    >>> for name, value in rgxp_config_items(
    ...         ui, "foo", re.compile(b'^pfx-(\\w+)-sfx$')):
    ...    print(name, value)
    b'some' b'ala, ma kota'
    b'other' 4

    :param ui: mercurial ui, used to access config
    :param section: config section name
    :param rgxp: tested regexp, should contain single (group)

    :return: yields pairs (group-match, value) for all matching items
    '''
    for key, value in ui.configitems(pycompat.bytestr(section)):
        match = rgxp.search(pycompat.bytestr(key))
        if match:
            yield pycompat.maybebytestr(match.group(1)), pycompat.maybebytestr(value)


def rgxp_configlist_items(ui, section, rgxp):
    r'''
    Similar to rgxp_config_items, but returned values are read using
    ui.configlist, so returned as lists.

    >>> import mercurial.ui; ui = mercurial.ui.ui()
    >>> setconfig_list(ui, "foo", [
    ...         ("pfx-some-sfx", "ala, ma kota"),
    ...         ("some.nonitem", "bela nie"),
    ...         ("x", "yes"),
    ...         ("pfx-other-sfx", "sth"),
    ... ])
    >>> setconfig_list(ui, "notfoo", [
    ...         ("pfx-some-sfx", "bad"),
    ...         ("pfx-also-sfx", "too"),
    ... ])
    >>>
    >>> for name, value in rgxp_configlist_items(
    ...         ui, "foo", re.compile(b'^pfx-(\\w+)-sfx$')):
    ...    print(name, value)
    b'some' [b'ala', b'ma', b'kota']
    b'other' [b'sth']

    :param ui: mercurial ui, used to access config
    :param section: config section name
    :param rgxp: tested regexp, should contain single (group) and be binary-string based

    :return: yields pairs (group-match, value-as-list) for all
             matching items
    '''
    section = pycompat.bytestr(section)
    for key, _unneeded_value in ui.configitems(section):
        key = pycompat.bytestr(key)
        match = rgxp.search(key)
        if match:
            yield pycompat.maybebytestr(match.group(1)), ui.configlist(section, key)


def rgxp_configbool_items(ui, section, rgxp):
    r'''
    Similar to rgxp_config_items, but returned values are read using
    ui.configbool, so returned as booleans.

    >>> import mercurial.ui; ui = mercurial.ui.ui()
    >>> setconfig_list(ui, "foo", [
    ...         ("pfx-some-sfx", "true"),
    ...         ("some.nonitem", "bela nie"),
    ...         ("x", "yes"),
    ...         ("pfx-other-sfx", "false"),
    ... ])
    >>> setconfig_dict(ui, "notfoo", {
    ...         "pfx-some-sfx": "1",
    ...         "pfx-also-sfx": "0",
    ...         })
    >>>
    >>> for name, value in rgxp_configbool_items(
    ...         ui, "foo", re.compile(b'^pfx-(\\w+)-sfx$')):
    ...    print(name, value)
    b'some' True
    b'other' False

    :param ui: mercurial ui, used to access config
    :param section: config section name
    :param rgxp: tested regexp, should contain single (group)

    :return: yields pairs (group-match, value-as-list) for all
             matching items
    '''
    section = pycompat.bytestr(section)
    for key, _unneeded_value in ui.configitems(section):
        key = pycompat.bytestr(key)
        match = rgxp.search(key)
        if match:
            yield pycompat.maybebytestr(match.group(1)), ui.configbool(section, key)


def suffix_config_items(ui, section, suffix):
    """
    Yields items from given config section which match pattern '«sth».suffix'

    >>> import mercurial.ui; ui = mercurial.ui.ui()
    >>> setconfig_list(ui, "foo", [
    ...         ("some.item", "ala, ma kota"),
    ...         ("some.nonitem", "bela nie"),
    ...         ("x", "yes"),
    ...         ("other.item", 4),
    ... ])
    >>> setconfig_dict(ui, "notfoo", {
    ...         "some.item": "bad",
    ...         "also.item": "too",
    ...         })
    >>>
    >>> for name, value in suffix_config_items(
    ...         ui, "foo", 'item'):
    ...    print(name, value)
    ...    print(type(name), type(value))
    b'some' b'ala, ma kota'
    <class 'mercurial.pycompat.bytestr'> <class 'mercurial.pycompat.bytestr'>
    b'other' 4
    <class 'mercurial.pycompat.bytestr'> <class 'int'>
    >>>
    >>> for name, value in suffix_config_items(
    ...         ui, b"foo", b'item'):
    ...    print(name, value)
    ...    print(type(name), type(value))
    b'some' b'ala, ma kota'
    <class 'mercurial.pycompat.bytestr'> <class 'mercurial.pycompat.bytestr'>
    b'other' 4
    <class 'mercurial.pycompat.bytestr'> <class 'int'>


    :param ui: mercurial ui, used to access config
    :param section: config section name
    :param suffix: expected suffix (without a dot)

    :return: yields pairs (prefix, value) for all matching items, values are lists
    """
    esc_suffix = pycompat.bytestr(re_escape(suffix))
    rgxp = re.compile(b'^(\\w+)\\.' + esc_suffix)
    for key, value in rgxp_config_items(ui, section, rgxp):
        yield key, value


def suffix_configlist_items(ui, section, suffix):
    """
    Similar to suffix_config_items, but returned values are read using
    ui.configlist, so returned as lists.

    >>> import mercurial.ui; ui = mercurial.ui.ui()
    >>> setconfig_list(ui, b"foo", [
    ...         (b"some.item", b"ala, ma kota"),
    ...         (b"some.nonitem", b"bela nie"),
    ...         (b"x", b"yes"),
    ...         (b"other.item", b"kazimira"),
    ... ])
    >>> setconfig_dict(ui, b"notfoo", {
    ...         b"some.item": "bad",
    ...         b"also.item": "too",
    ...         })
    >>>
    >>> for name, value in suffix_configlist_items(
    ...         ui, b"foo", b"item"):
    ...    print(name, value)
    b'some' [b'ala', b'ma', b'kota']
    b'other' [b'kazimira']

    Attempts to handle native strings:

    >>> for name, value in suffix_configlist_items(
    ...         ui, "foo", "item"):
    ...    print(name, value)
    b'some' [b'ala', b'ma', b'kota']
    b'other' [b'kazimira']

    :param ui: mercurial ui, used to access config
    :param section: config section name
    :param suffix: expected suffix (without a dot)

    :return: yields pairs (group-match, value-as-list) for all
             matching items, values are boolean
    """
    esc_suffix = pycompat.bytestr(re_escape(suffix))
    rgxp = re.compile(b'^(\\w+)\\.' + esc_suffix)
    for key, value in rgxp_configlist_items(ui, section, rgxp):
        yield key, value


def suffix_configbool_items(ui, section, suffix):
    """
    Similar to suffix_config_items, but returned values are read using
    ui.configbool, so returned as booleans.

    >>> import mercurial.ui; ui = mercurial.ui.ui()
    >>> setconfig_list(ui, "foo", [
    ...         ("true.item", "true"),
    ...         ("false.item", "false"),
    ...         ("one.item", "1"),
    ...         ("zero.item", "0"),
    ...         ("yes.item", "yes"),
    ...         ("no.item", "no"),
    ...         ("some.nonitem", "1"),
    ...         ("x", "yes"),
    ... ])
    >>> setconfig_dict(ui, "notfoo", {
    ...         "some.item": "0",
    ...         "also.item": "too",
    ...         })
    >>>
    >>> for name, value in suffix_configbool_items(
    ...         ui, "foo", "item"):
    ...    print(name, str(value))
    b'true' True
    b'false' False
    b'one' True
    b'zero' False
    b'yes' True
    b'no' False
    >>>
    >>> ui.setconfig(b"foo", b"text.item", b"something")
    >>> try:
    ...     for name, value in suffix_configbool_items(ui, "foo", "item"):
    ...          x = (name, str(value))
    ...     print("Strange, no error")
    ... except Exception as err:
    ...     print(repr(err)[:58])   # :58 augments py36-py37 diff
    ConfigError(b"foo.text.item is not a boolean ('something')

    :param ui: mercurial ui, used to access config
    :param section: config section name
    :param suffix: expected suffix (without a dot)

    :return: yields pairs (group-match, value) for all
             matching items
    """
    section = pycompat.bytestr(section)
    esc_suffix = pycompat.bytestr(re_escape(suffix))
    rgxp = re.compile(b'^(\\w+)\\.' + esc_suffix)
    for key, value in rgxp_configbool_items(ui, section, rgxp):
        yield key, value


###########################################################################
# Monkeypatching
###########################################################################

def monkeypatch_method(cls, fname=None):
    """
    Monkey-patches some method, replacing it with another
    implementation. Original method is preserved on ``.orig``
    attribute.

    >>> class SomeClass(object):
    ...    def meth(self, arg):
    ...        return "Original: " + arg
    >>>
    >>> @monkeypatch_method(SomeClass)
    ... def meth(self, arg):
    ...     return "Patched: " + meth.orig(self, arg)
    >>>
    >>> obj = SomeClass()
    >>> print(obj.meth("some param"))
    Patched: Original: some param

    It is also possible to use different name

    >>> class SomeClass(object):
    ...    def meth(self, arg):
    ...        return "Original: " + arg
    >>>
    >>> @monkeypatch_method(SomeClass, "meth")
    ... def another_meth(self, arg):
    ...     return "Patched: " + another_meth.orig(self, arg)
    >>>
    >>> obj = SomeClass()
    >>> print(obj.meth("some param"))
    Patched: Original: some param

    :param cls: Class being modified
    :param fname: Name of method being monkey-patched (if not given,
           name of decorated function is used)
    """
    def decorator(func):
        local_fname = fname
        if local_fname is None:
            local_fname = func.__name__
        setattr(func, "orig", getattr(cls, local_fname, None))
        setattr(cls, local_fname, func)
        return func
    return decorator


def monkeypatch_function(module, fname=None):
    """
    Monkey-patches some function, replacing it with another
    implementation. Original function is preserved on ``.orig``
    attribute.

    >>> import random
    >>> @monkeypatch_function(random)
    ... def seed(x=None):
    ...     print("Forcing random to seed with 0 instead of", x)
    ...     return seed.orig(0)
    >>>
    >>> random.seed()
    Forcing random to seed with 0 instead of None
    >>> random.randint(0, 10)
    6

    >>> import random
    >>> @monkeypatch_function(random, 'choice')
    ... def choice_first(sequence):
    ...    return sequence[0]
    >>> for x in range(0, 4): print(random.choice("abcdefgh"))
    a
    a
    a
    a

    :param module: Module being modified
    :param fname: Name of function being monkey-patched (if not given,
           name of decorated function is used)
    """
    # In fact implementation is the same. But it is more readable
    # to use two names
    return monkeypatch_method(module, fname)


###########################################################################
# Locating repositories
###########################################################################

def find_repositories_below(path, check_inside=False):
    """Finds all Mercurial repositories in given directory tree.

    Works as generator, yielding full paths of all repositories found,
    ordered alphabetically.  If initial path is itself some
    repository, it is included.

    By default function does not look for embedded repositories (if we
    scan from ~/src and both ~/src/somerepo and ~/src/somerepo/subrepo
    are repositories, only the former will be yielded).  This can be
    changed by check_inside param

    :param path: Initial path
    :param check_inside: Shall we look for embedded repos?
    :return: generator of full repo paths (paths are absolute and even
        on Windows /-separated)
    """
    # Impl. note: we do not use os.walk as it can be very costly
    # if some repo is big and deep.
    pending = deque([normalize_path(path)])
    while pending:
        checked = pending.popleft()
        if os.path.isdir(checked + b'/.hg'):
            yield checked
            if not check_inside:
                continue
        try:
            names = os.listdir(checked)
        except OSError:
            # Things like permission errors (say, on lost+found)
            # Let's ignorre this, better to process whatever we can
            names = []
        paths = [pycompat.bytestr(checked + b'/' + pycompat.bytestr(name))
                 for name in names if name != '.hg']
        dir_paths = [item
                     for item in paths if os.path.isdir(item)]
        pending.extendleft(sorted(dir_paths, reverse=True))


###########################################################################
# Compatibility layers
###########################################################################

def command(cmdtable):
    """
    Compatibility layer for mercurial.cmdtutil.command.

    For Mercurials >= 3.8 it's registrar.command

    For Mercurials >= 3.1 it's just synonym for cmdutil.command.

    For Mercurials <= 3.0 it returns upward compatible function
    (adding norepo, optionalrepo and inferrepo args which
    are missing there).

    Usage: just call ``meu.command(cmdtable)`` instead of
    ``cmdutil.command(cmdtable)``. For example:

    >>> cmdtable = {}
    >>> cmd = command(cmdtable)
    >>>
    >>> @cmd("somecmd", [], "somecmd")
    ... def mycmd(ui, repo, sth, **opts):
    ...    pass
    >>>
    >>> @cmd("othercmd", [
    ...             ('l', 'list', None, 'List widgets'),
    ...             ('p', 'pagesize', 10, 'Page size'),
    ...          ], "othercmd [-l] [-p 20]", norepo=True)
    ... def othercmd(ui, sth, **opts):
    ...    pass
    >>>
    >>> sorted(cmdtable.keys())
    ['othercmd', 'somecmd']
    >>> cmdtable['othercmd']    # doctest: +ELLIPSIS
    (<function othercmd at ...>, [('l', 'list', None, 'List widgets'), ('p', 'pagesize', 10, 'Page size')], 'othercmd [-l] [-p 20]')

    Below is uninteresting test that it really works in various mecurials:

    >>> from mercurial import commands
    >>> # Syntax changed in hg3.8, trying to accomodate
    >>> commands.norepo if hasattr(commands, 'norepo') else ' othercmd'    # doctest: +ELLIPSIS
    '... othercmd'
    >>> othercmd.__dict__['norepo'] if othercmd.__dict__ else True
    True
    >>> mycmd.__dict__['norepo'] if mycmd.__dict__ else False
    False

    """
    from mercurial import cmdutil, commands
    import inspect
    try:
        from mercurial import registrar
        command = registrar.command(cmdtable)
        return command
    except (ImportError, AttributeError):
        command = cmdutil.command(cmdtable)
    spec = inspect.getargspec(command)
    if 'norepo' in spec[0]:
        # Looks like modern mercurial with correct api, keeping
        # it's implementation
        return command

    # Old mecurial with only name, options, synopsis in data,
    # patching to get full signature. This is more or less copy
    # of current implementation, sans docs.

    def parsealiases(cmd):
        return cmd.lstrip("^").split("|")

    def fixed_cmd(name, options=(), synopsis=None,
                  norepo=False, optionalrepo=False, inferrepo=False):
        def decorator(func):
            if synopsis:
                cmdtable[name] = func, list(options), synopsis
            else:
                cmdtable[name] = func, list(options)
            if norepo:
                commands.norepo += ' %s' % ' '.join(parsealiases(name))
            if optionalrepo:
                commands.optionalrepo += ' %s' % ' '.join(parsealiases(name))
            if inferrepo:
                commands.inferrepo += ' %s' % ' '.join(parsealiases(name))
            return func
        return decorator
    return fixed_cmd


###########################################################################
# Demandimport workarounds and other import-related functions
###########################################################################

def direct_import(module_name, blocked_modules=None):
    """
    Imports given module, working around Mercurial
    demandimport (so recursively imported modules are properly
    imported)

    >>> re = direct_import("re")
    >>> re.__name__
    're'
    >>> re.search("^(.)", "Ala").group(1)
    'A'

    Allows to block some modules from demandimport machinery,
    so they are not accidentally misloaded:

    >>> k = direct_import("dbm", ["dbm.gnu", "dbm.ndbm", "dbm.dumb"])
    >>> k.__name__
    'dbm'

    :param module_name: name of imported module
    :param blocked_modules: names of modules to be blocked from demandimport
         (list)
    :return: imported module
    """
    return direct_import_ext(module_name, blocked_modules)[0]


def direct_import_ext(module_name, blocked_modules=None):
    """
    Like direct_import, but returns info whether module was just
    imported, or already loaded.

    >>> m1, loaded = direct_import_ext("xml.sax.handler")
    >>> m1.__name__, loaded
    ('xml.sax.handler', True)

    >>> m2, loaded = direct_import_ext("xml.sax.handler")
    >>> m2.__name__, loaded
    ('xml.sax.handler', False)

    >>> m1 == m2
    True

    :param module_name: name of imported module
    :param blocked_modules: names of modules to be blocked from
        demandimport (list)

    :return: (imported module, was-it-imported-now?)
    """
    if module_name in sys.modules:
        return sys.modules[module_name], False

    from mercurial import demandimport
    if blocked_modules:
        for blocked_module in blocked_modules:
            if hasattr(demandimport, 'IGNORES'):
                # Mercurial 4.7 introduced set demandimport.IGNORES
                demandimport.IGNORES.add(blocked_module)
            else:
                # Earlier it was demandimport.ignore, a list
                if blocked_module not in demandimport.ignore:
                    demandimport.ignore.append(blocked_module)

    # Various attempts to define is_demandimport_enabled
    try:
        # Since Mercurial 2.9.1
        is_demandimport_enabled = demandimport.isenabled
    except AttributeError:
        def is_demandimport_enabled():
            """Checks whether demandimport is enabled at the moment"""
            return __import__ == demandimport._demandimport  # pylint: disable=protected-access

    # Temporarily disable demandimport to make the need of extending
    # the list above less likely.
    if is_demandimport_enabled():
        demandimport.disable()
        __import__(module_name)
        demandimport.enable()
    else:
        __import__(module_name)
    return sys.modules[module_name], True


def disable_logging(module_name):
    """
    Shut up warning about initialized logging which happens if some
    imported module logs (mercurial does not setup logging machinery)

    >>> disable_logging("keyring")

    :param module_name: Name of logger to disable
    """
    import logging
    if hasattr(logging, 'NullHandler'):
        null_handler = logging.NullHandler()
    else:
        class NullHandler(logging.Handler):
            """Emergency null handler"""
            def handle(self, record):
                pass
            def emit(self, record):
                pass
            def createLock(self):
                self.lock = None
        null_handler = NullHandler()
    logging.getLogger(module_name).addHandler(null_handler)


###########################################################################
# Context detection
###########################################################################

def inside_tortoisehg():
    """Detects tortoisehg presence - returning True if the function
    is called by some code which has TortoiseHg in the caller stack.

    This may be needed in some cases to accomodate specific TortoiseHg
    main loop behaviours (see enable_hook below for example)."""
    import inspect
    for item in inspect.stack():
        # item has 6 elems: the frame object, the filename, the line number of the current line, the function name, a list of lines of context from the source code, and the index of the current line within that list.
        module = inspect.getmodule(item[0])
        if module.__name__.startswith("tortoisehg."):
            return True
    return False


###########################################################################
# Hook support
###########################################################################

def enable_hook(ui, hook_name, hook_function):
    """
    Enables given (dynamic) hook.

    At the moment this is a simple wrapper for ui.setconfig, with the
    only exception: it checks whether the same function is already
    configured by name, and if so, doesn't do anything (so it may be
    used for *dynamically install hook unless it is already statically
    enabled* cases).

    :param hook_name: string like "pre-tag.my_function" (hook
        placement and symbolic name)
    :param hook_function: proper callable.  To handle presence
        detection, it should be top-level module function (not method,
        not lambda, not local function embedded inside another
        function).
    """
    hook_name = pycompat.bytestr(hook_name)

    # Detecting function name, and checking whether it seems publically
    # importable and callable from global module level
    if hook_function.__class__.__name__ == 'function' \
       and not hook_function.__name__.startswith('<') \
       and not hook_function.__module__.startswith('__'):

        hook_function_name = pycompat.bytestr('{module}.{name}'.format(
            module=hook_function.__module__, name=hook_function.__name__))
        hook_activator = pycompat.bytestr(b'python:' + hook_function_name)

        for key, value in ui.configitems("hooks"):
            if key == hook_name:
                if value == hook_activator:
                    ui.debug(ui_string("meu: Hook already statically installed, skipping %s: %s\n",
                                        hook_name, hook_function_name))
                    return
                if value == hook_function:
                    ui.debug(ui_string("meu: Hook already dynamically installed, skipping %s: %s\n",
                                        hook_name, hook_function_name))
                    return

    ui.debug(ui_string("meu: Enabling dynamic hook %s: %s\n",
                        hook_name, hook_function_name))

    # Standard way of hook enabling
    setconfig_item(ui, b"hooks", hook_name, hook_function)


###########################################################################
# Manual test support
###########################################################################

if __name__ == "__main__":
    import doctest
    # doctest.testmod()
    # doctest.run_docstring_examples(setconfig_dict, globals())
    # doctest.run_docstring_examples(setconfig_list, globals())
    # doctest.run_docstring_examples(rgxp_config_items, globals())
    # doctest.run_docstring_examples(suffix_configlist_items, globals())
    # doctest.run_docstring_examples(normalize_path, globals())
    doctest.run_docstring_examples(rgxp_configbool_items, globals())
    doctest.run_docstring_examples(rgxp_configlist_items, globals())
    doctest.run_docstring_examples(suffix_config_items, globals())
    doctest.run_docstring_examples(suffix_configbool_items, globals())
