.. -*- mode: rst; compile-command: "rst2html README.rst README.html" -*-

=======================================================
Mercurial BitBucketize
=======================================================

Publish your next repo to bitbucket without clicking through the web
interface. Also switch it easily from private to public (or back), set
description, enable or disable wiki and issue tracker…

.. contents::
   :local:
   :depth: 2

.. sectnum::

Synopsis
=======================================================

In simplest configuration extension works just as generic BitBucket_
client::

   hg bitbucket_create acme-toolkit --wiki --private --forks=private

   hg bitbucket_modify acme-toolkit --public -m "THE toolkit above all toolkits"

   hg bitbucket_status acme-toolkit

   hg bitbucket_delete acme-toolkit

   hg bitbucket_goto acme-toolkit

Those commands operate on ``https://bitbucket.org/«USER»/acme-toolkit``
where ``«USER»`` is your BitBucket username (configured in extension
configuration).

Paired with `Path Pattern`_ it can also deduce *appropriate name*
for the current repository::

   # Create private bitbucket clone of current repo
   hg bitbucket_create
   # ... or maybe public one
   hg bitbucket_create --issues --public -l python -m "Webapp for nowhere.com"

   hg bitbucket_status

   hg bitbucket_modify --language=perl

   hg bitbucket_goto --issues

   hg bitbucket_delete

To save typing, all commands have shorter aliases (``hg bb_create``,
``hg bb_status``, etc).

Enabling and configuring the extension
=======================================================

Install the extension as described below (see
`Installation`_ section). Then enable it and configure a few crucial
parameters by writing in ``~/.hgrc``::

    [extensions]
    mercurial_bitbucketize = 

    [bitbucketize]
    user = John
    login = johny@gmail.com
    path_alias = bitbucket

Here: ``user`` is your short BitBucket username (the name present in
URLs of your repositories) and ``login`` is your Atlassian login (the
username you enter while performing browser login), 

The ``path_alias`` is optional and means, that in case such alias
(here: ``bitbucket``) is defined for current repository, it can be
used to deduce the name of BitBucket repository to operate on. That
works great if you install and enable `Path Pattern`_ and define
appropriate pattern, for example::

    [extensions]    
    mercurial_bitbucketize = 
    mercurial_path_pattern = 

    [bitbucketize]
    user = John
    login = johny@gmail.com
    path_alias = bitbucket

    [path_pattern]
    bitbucket.local = ~/devel/{below}
    bitbucket.remote = https://bitbucket.org/John/{below:/=-}
    
(with such settings ``bitbucketize`` will know that ``~/devel/libs/acme``
should be paired with ``https://bitbucket.org/John/libs-acme`` on BitBucket).

It is also strongly recommended that you install Keyring_ to avoid
being repeatably prompted for BitBucket password (``bitbucketize``
happily uses `Keyring`_ to save password in secure storage). 

.. note::

   In case you happen to issue ``hg pull bitbucket`` or ``hg push bitbucket``
   over HTTP (instead of ssh), you will likely want to add::

      [auth]
      bitbucket.prefix = https://bitbucket.org
      bitbucket.username = John.Smith@some.where.com

   Those settings are irrelevant from the Bitbucketize point of view,
   but one usually wants to keep them in sync with ``bitbucketize``
   settings.


Commands
=======================================================

Standard help is available for all commands (``hg help bitbucket_create``,
etc), check it out for detailed list of all options.

All commands have shorter aliases prefixed with ``bb_`` (instead of
``hg bitbucket_modify`` you can type ``hg bb_modify``).

------------------------------------------------------------
Creating BitBucket repository (``hg bitbucket_create``)
------------------------------------------------------------

Creates new repository on BitBucket. You can give the name::

    hg bitbucket_create tinyapps-acme

(then the command is context-less) or rely on deduction::

    hg bitbucket_create

(the latter depends on proper ``path_alias`` configuration).

By default repository is private, has no wiki, no issue
tracker, and no description. Some of those can be specified,
for example::

    hg bb_create --wiki --issues --descr="My repo" --public

.. note::

    I usually prefer to create repository as private, push the code,
    verify README appearance, and later, when I am generally happy and
    ready for the release, switch to public.

The ``bitbucket_create`` command does not push the code (created
repository is empty). This is done on purpose, to let you verify
the name and settings before you push.

------------------------------------------------------------
Toggling repository features (``hg bitbucket_modify``)
------------------------------------------------------------

Use ``bitbucket_modify`` command to modify repository features.

It can be used to switch it to public::

    hg bitbucket_modify --public

or back to private::

    hg bitbucket_modify --private

and correct metadata::

    hg bitbucket_modify --lang=Perl --descr="TIMTOWTDI"

Examples above operated on *deduced* repository. Of course
specifying the name is also possible::

    hg bitbucket_modify tinylibs-acme --public --wiki

Similarly toggle wiki and issues::

    hg bitbucket_modify --wiki
    hg bitbucket_modify --no-wiki
    hg bitbucket_modify --issues
    hg bitbucket_modify --no-issues

.. warning::

   Disabling wiki or issue tracker is destructive, dangerous
   operation. At the moment there is no additional warning or prompt
   (I plan to add one in the future).


------------------------------------------------------------
Checking repository status (``hg bitbucket_status``)
------------------------------------------------------------

Use ``bitbucket_status`` command to check whether 
repository exists, and print it's metadata::

   hg bitbucket_status

or::

    hg bitbucket_status tinylibs-acme

------------------------------------------------------------
Deleting the BitBucket clone (``hg bitbucket_delete``)
------------------------------------------------------------

Use ``bitbucket_delete`` to remove BitBucket clone::

   hg bitbucket_delete

or, to delete repository with specific name::

    hg bitbucket_delete acme

.. warning::

   This is irrecoverable operation. Even if you still have the code
   (and can push it back), there is no way to recover issues, wiki,
   downloads, or permissions.

   Use this command to delete temporary ad hoc repos, for more serious
   removals consider web interface.

------------------------------------------------------------
Visiting BitBucket web pages (``hg bitbucket_goto``)
------------------------------------------------------------

Simple shortcut to open respository related web pages on BitBucket.

To visit overview::

    hg bitbucket_goto tinylibs-acme

or (with name deduction)::

    hg bb_goto

To visit specific page::

    hg bitbucket_goto tinylibs-acme --issues

or (with name deduction)::

    hg bb_goto -l

(see ``hg help bb_goto`` for list of all pages supported).

Default system browser is used (established according to various
system-specific conventions). If that guess is incorrect, it
can be configured in ``.hgrc``. Either by something like::

    [browser]
    type = firefox

where ``type`` is one of webbrowser_ supported values (``firefox``,
``chrome``, ``safari``, ``opera``, ``konqueror``, …) or::

    [browser]
    command = /usr/bin/firefox

(the former is slightly preferable as it can give browser incentive
to raise the window).


Installation
=======================================================

------------------------------------------------------------
Linux/Unix
------------------------------------------------------------

Installing from PyPi
------------------------------------------------------------

To install for the first time, just::

   pip install --user mercurial_bitbucketize

This should install both the extension itself, and all it's
dependencies. Of course other methods of installing Python
packages work too (like ``sudo easy_install mercurial_bitbucketize``). 

Activate by writing in ``~/.hgrc``::

    [extensions]
    mercurial_bitbucketize =

To upgrade::

   pip install --upgrade --user mercurial_bitbucketize

As I already said, it is strongly recommended that you install also
Keyring_ and `Path Pattern`_.


Installing for development
------------------------------------------------------------

Clone the extension itself, and it's dependencies
(PyBitBucket_ and `mercurial_extension_utils`_)::

   hg clone git+https://bitbucket.org/atlassian/python-bitbucket.git
   # Or git clone https://bitbucket.org/atlassian/python-bitbucket.git

   hg clone https://foss.heptapod.net/mercurial/mercurial-extension_utils   

   hg clone https://foss.heptapod.net/mercurial/mercurial-bitbucketize

Update to newest tags if you prefer to work on stable versions. 

Install them for development (dependencies first)::

   pip install --user --edit python-bitbucket
   pip install --user --edit mercurial-extension_utils
   pip install --user --edit mercurial-bitbucketize

Activate as usual::

    [extensions]
    mercurial_bitbucketize =

To upgrade just pull changes and update in appropriate repositories.



------------------------------------------------------------
Windows
------------------------------------------------------------

If you have Python installed, install necessary modules with ``pip``,
just like on Linux::

   pip install --user mercurial_bitbucketize

As Mercurial (whether taken from TortoiseHg_, or own package)
uses it's own bundled Python, you must activate by specifying the path::

    [extensions]
    mercurial_bitbucketize = C:/Python27/Lib/site-packages/mercurial_bitbucketize.py
    ;; Or wherever pip installed it

Extension will take care of finding necessary modules.

If you don't have Python, you may try the method described above in
`Installing for development`_, but I suspect you will face missing
dependencies. So preferably install Python.


Related extensions
=======================================================

Mercurial wiki quotes BitbucketExtension_. Original repository
seems gone, but some copy lives on as hgbb_. 

That extension seems concentrated on different parts of BitBucket_
(making aliases, fork management) than BitBucketize (which is mostly
about creating repositories and maintaining their metadata).

Also Bitbucketize is using mostly 2.0 BitBucket API while hgbb_ so far
sticks to 1.0 version. This shows up in lack of some
fields/attributes.

.. _BitbucketExtension: https://www.mercurial-scm.org/wiki/BitbucketExtension

.. _hgbb: https://bitbucket.org/seanfarley/hgbb


History
=======================================================

See `HISTORY.rst`_


Repository, bug reports, enhancement suggestions
=======================================================

Development is tracked on HeptaPod, see 
https://foss.heptapod.net/mercurial/mercurial-bitbucketize/

Use issue tracker there for bug reports and enhancement
suggestions.

Thanks to Octobus_ and `Clever Cloud`_ for hosting this service.


Known problems
=======================================================

-------------------------------------------------------
``Value error`` on repository creation
-------------------------------------------------------

If ``hg bitbucket_create`` ends with::

   ValueError: dictionary update sequence element #0 has length 1; 2 is required

you observe effect of recurring bug in ``pybitbucket``. 

Upgrading ``pybitbucket`` to version 0.6.1 or newer should resolve
the problem.

If this is not feasible at the moment, you can also ignore the error
(failure happens after repository was created, it's only consequence
is that you do not see the confirmation message). Use ``hg bitbucket_details``
to check whether repository state is correct.


Additional notes
=======================================================

Information about this extension is also available
on Mercurial Wiki: http://mercurial.selenic.com/wiki/BitBucketizeExtension

Check also `other Mercurial extensions I wrote`_.

.. _Octobus: https://octobus.net/
.. _Clever Cloud: https://www.clever-cloud.com/

.. _other Mercurial extensions I wrote: http://code.mekk.waw.pl/mercurial.html

.. _Mercurial: http://mercurial.selenic.com
.. _HISTORY.rst: https://foss.heptapod.net/mercurial/mercurial-update_version/src/tip/HISTORY.rst
.. _mercurial_extension_utils: https://foss.heptapod.net/mercurial/mercurial-extension_utils/
.. _TortoiseHg: http://tortoisehg.bitbucket.org/
.. _PyBitBucket: https://bitbucket.org/atlassian/python-bitbucket
.. _BitBucket: https://bitbucket.org
.. _Path Pattern: https://foss.heptapod.net/mercurial/mercurial-path_pattern
.. _Keyring: https://foss.heptapod.net/mercurial/mercurial_keyring
.. _BitBucket: https://bitbucket.org
.. _webbrowser: https://docs.python.org/2/library/webbrowser.html
.. _my pybitbucket fork: https://bitbucket.org/Mekk/python-bitbucket
