0.9.4
~~~~~~~~~~~~~

Fixing various links as Atlassian killed Bitbucket. This also means end of this
module but let's do this final release.

Partial work towards py3 support. Not everything works but at least extension
presence doesn't break py3 mercurial.

Some compatibility fixes related to pybitbucket changes.

0.9.3
~~~~~~~~~~~~

Tested against hg 4.8 (no changes needed).

0.9.2
~~~~~~~~~~

Compatibility with 4.7.


0.9.1
~~~~~~~~~~~

Testing with 4.5 and 4.6, small 4.6-releated fixes (arror reporting).

0.9.0
------------

Support for Mercurials >= 3.9 (updated for url/passwordmgr API changes)

Updated links after bitbucket changes.

hg 4.1 and 4.2 added to tested versions.

0.8.0
------------

Updated to work properly with Atlassian usernames (no longer the same
username is used for HTTP authorization and in urls). Without this
change extension in fact worked, but had issues cooperating with
mercurial_keyring (password saved twice for two usernames etc).

Updated to work with pybitbucket 0.12.0 (various API changes, especially
in repository creation).

0.7.0
-------------

Adapted to current pybitbucket API (tested with pybitbucket 0.10.0).
No functional changes.

0.6.4
-------------

Forward compatibility to incoming Mercurial 3.8 (movet to current
cmdtable API).

0.6.3
--------------

Depending on pybitbucket version which finally solved repository
creation bug.

0.6.2
--------------

Support for hg --traceback bb_create, hg --traceback bb_modify etc
(showing traceback of errors, would they happen)

0.6.0
--------------

Added bitbucket_goto (opening various pages)

Dropped workarounds necessary for pybitbucket < 0.6.0

0.5.1
--------------

Installation instructions and setup itself use the fact, that pybitbucket
is PyPi installable (0.6.0 at the moment).

0.5.0
--------------

First release. Working bb_create, bb_modify, bb_delete, bb_status.
Test suite for crucial commands.
