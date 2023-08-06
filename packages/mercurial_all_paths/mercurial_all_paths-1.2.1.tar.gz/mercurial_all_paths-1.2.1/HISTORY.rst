
1.2.1
~~~~~~~~~~~~

Fixing various links as Atlassian killed Bitbucket.
Testing against hg 5.3 and 5.4.

1.2.0
~~~~~~~~~~~~

Should work under python3-based Mercurial installs (without breaking
python2 support). 

Tested against hg 5.1 and 5.2. 

1.1.4
~~~~~~~~~~~~

Tested against hg 4.8 (no changes needed).

1.1.3
~~~~~~~~~~~~~

Tested against 4.7. Bumping meu dep version to one which fully
supports 4.7 (although the change is not really critical for this module)

1.1.2
~~~~~~~~~~~~~

Tested against 4.5 and 4.6. A few fixes to actually make it work there
in all cases (error reporting problems on 4.6…), and a few testfixes.

1.1.1
~~~~~~~~~~~~~

Fixed various errors in code which reported problems with
mercurial_extension_utils import (various crashes instead
of proper error message or import from sibling directory).

1.1.0
~~~~~~~~~~~~~

Fixed to work with Mercurial >= 4.1

Formally tested against Mercurial 4.1 and 4.2

Updated doc links after bitbucket changes.

Note: since this version mercurial_extension_utils is required
(for meu.command, compatibility layer for command definition
working against various mercurial versions).

1.0.2
~~~~~~~~~~~~~

Some unimportant test tweaks (tests were failing in some environments).

1.0.1
~~~~~~~~~~~~~

Tests fixed to work on mecurial 4.0 … and 2.7.

1.0.0
~~~~~~~~~~~~~

Functional changes:

1. It is possible to configure aliases which should be ignored by `hg
   pushall' or `hg pullall` - by ignore config setting.

2. It is possible to configure preferred ordering (for example to pull
   from nearby servers first) - by prioritize config setting.

3. Added alternative configuration syntax for groups: group.«NAME» =
   list of aliases. This avoids naming conflicts, avoids repetition if
   path is to be used both in group and individually, and makes it
   possible to define groups globally (not only on repo level).

Example config snippet:

   [all_paths]
   prioritize = devel master bitssh
   ignore = production bitbucket
   group.share = devel bitssh

Non-functional changes:

4. Extension is now unit-tested, passed tests against wide range
   of mercurial versions (and has nice drone badge).

5. Improved README, some help texts tweaks.

0.6.0
~~~~~~~~~~~~~

Release by Marcin Kasperski

Added hg pullall, hg incomingall, hg outgoingall

Internals reworked so all push options work (also --insecure, --ssh)

Added setup.py, PyPi release.

Renamed to mercurial_all_paths (to make PyPi conflicts less likely). 

*
~~~~~~~~~~~~~

Initial release by Ludovic Chabant. 

   hg pushall

command, and

   hg pushall -g ‹group›
