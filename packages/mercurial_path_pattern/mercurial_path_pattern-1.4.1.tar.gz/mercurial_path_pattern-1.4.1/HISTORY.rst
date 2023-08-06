1.4.1
~~~~~~~~~~~~

Fixing various links as Atlassian killed Bitbucket.
Testing against hg 5.3 and 5.4.

1.4.0
~~~~~~~~~~~~

Should work under python3-based Mercurial installs (without breaking
python2 support). 

Tested against hg 5.1 and 5.2. 

1.3.7
~~~~~~~~~~~~

Tested against hg 4.8 (no changes needed).

1.3.6
~~~~~~~~~~~~~

Tested with hg 4.7. Bumped mercurial_extension_utils dependency to
version which fully works on 4.7 (not really necessary as here we
don't use problematic direct_import_ext, but better be safe…)


1.3.5
~~~~~~~~~~~~~

Tested with hg 4.5 and 4.6, small 4.6-related fixes (error handling)

1.3.3
~~~~~~~~~~~~~

Updated links after bitbucket changes.

hg 4.1 and 4.2 added to tested versions.

1.3.2
----------------------

Symbolic names used in path-patterns can use '-' character, for example
    official.some-thing.local = …
    official.some-thing.remote = …
works properly (so far those entries were ignored as they did not match
expected format).

1.3.1
----------------------

Formally testing with hg 4.0 (no problems detected).

Added some missing newlines in --debug notes..

1.3.0
----------------------

Introduced new, shorter syntax for alternative paths:

    alias.sth.local = ...
    alias.sth.remote = ...

Documentation updates.

1.2.0
----------------------

Forward-compatibility with Mercurial 3.8.0 (migrated to up to modern
command definition API).

Wider Mercurial versions tested.

Added test for list_path_patterns and some testfixes (hg paths does not
always guarantee sort order).

Meu >= 1.2.0 required.

1.1.1
----------------------

Drop path_pattern.py (reminder about name change).

Automatic testing cross various Mercurial versions.


1.1.0
----------------------

Bugfix: patterns without any {variable} in .local part did not work.

In case more than one pattern matches local url giving the same alias,
most specific one is used (previously the one positioned last in hgrc
won, by accident). See README for details.

Noticeable documentation updates.

1.0.0
----------------------

Implemented «pfx».alias. Introduced so more than one pattern can
introduce the same name.

Module renamed from path_pattern to mercurial_path_pattern, to be
less invasive on python installation.

0.10.0
-----------------------

Works on Windows, including Tortoise-bundled Mercurial.

0.9.0
-----------------------

Pattern can be configured to win over repo-level paths:

   pattern.enforce = true

0.8.0
-----------------------

Handling of simple substitutions like {item:/=-} or {item:\=/}.
Main use-case is translating / into - for Bitbucket.
    [path_pattern]
    bb.local = ~/DEV_hg/{below}
    bb.remote = ssh://hg@bitbucket.org/Mekk/{below:/=-}

Handling of (limited) groups (passing no more than one path segment).
For example ~/sources/(group)/{rest}.

Internally uses ``mercurial_extension_utils``.

0.7.0
-----------------------

Added ``hg cloneto`` command.

0.6.1
------------------------

First public release. Working path patterns implementation.
