# -*- coding: utf-8 -*-
#
# mercurial_bitbucketize: create and update bitbucket repos from cmdline
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

"""Create and administer BitBucket repositories without using web interface.

See README.rst (web copy: https://foss.heptapod.net/mercurial/mercurial-bitbucketize )
for details.
"""

# pylint: disable=invalid-name,broad-except,too-many-arguments,line-too-long

import re
import os
import sys
import textwrap
import pprint
from mercurial import error
from mercurial.i18n import _



def import_meu():
    """Importing mercurial_extension_utils so it can be found also outside
    Python PATH (support for TortoiseHG/Win and similar setups)"""
    try:
        import mercurial_extension_utils
    except ImportError:
        my_dir = os.path.dirname(__file__)
        sys.path.extend([
            # In the same dir (manual or site-packages after pip)
            my_dir,
            # Developer clone
            os.path.join(os.path.dirname(my_dir), "extension_utils"),
            # Side clone
            os.path.join(os.path.dirname(my_dir), "mercurial-extension_utils"),
        ])
        try:
            import mercurial_extension_utils
        except ImportError:
            raise error.Abort(_("""Can not import mercurial_extension_utils.
Please install this module in Python path.
See Installation chapter in https://foss.heptapod.net/mercurial/mercurial-dynamic_username/ for details
(and for info about TortoiseHG on Windows, or other bundled Python)."""))
    return mercurial_extension_utils

meu = import_meu()


def import_pybitbucket(submodule):
    """demandimport-resistant import of pybitbucket.bitbucket
    Returns imported module"""
    module_name = 'pybitbucket.' + submodule
    return meu.direct_import(module_name, [
        'ssl', 'urllib3'])


# Disabling notorious ssl warnings which require upgrade to python 2.7.9,
# and are often not possible for the user in charge. As Mercurial itself
# is less picky, we may shut up too.
# https://urllib3.readthedocs.org/en/latest/security.html#insecureplatformwarning
# https://urllib3.readthedocs.org/en/latest/security.html#snimissingwarning
if sys.version_info < (2, 7, 9):
    try:
        import urllib3
        urllib3.disable_warnings()
    except Exception:
        pass


############################################################
# BitBucket-API related utility functions
############################################################

CONFIG_SECTION = b'bitbucketize'

# Regexp for bitbucket paths. We allow the following forms:
#    mercurial-bitbucketize
#    Mekk/mercurial-bitbucketize
#    bitbucket.org/Mekk/mercurial-bitbucketize
#    https://foss.heptapod.net/mercurial/mercurial-bitbucketize
# and a few similar variations
re_path = re.compile(b'''
^
    # http prefix and host
    (?:
        (?: https?:// )?
        (?:www\\.)? bitbucket\\.org /
    )?
    # Username
    (?:
        (?P<user> [^/]+ )  /
    )?
    # name
    (?P<name> [^/]+ )
$
''', re.VERBOSE)


def calculate_user_and_repo(ui, repo, name):
    """Calculates BitBucket username and repository name, according to
    configuration, current repo and params.

    Returns USER, LOGIN, REPO_NAME, ALIAS where:

        - USER is short account name (like "Mekk"), used in repository
          paths, and user-related repository calls (user setting
          deduced from [bitbucketize] config section),

        - LOGIN is Atlassian account name/email (like
          "Marcin.Kasperski@far.away.com"), used to login to Atlassian
          account via HTTP (in particular, in browser)

        - REPO_NAME is repository name (like "mercurial-bitbucketize"),
          given as command line param or deduced from current
          repository

        - ALIAS is symbolic remote alias for bitbucket (path_alias
          from [bitbucketize] config section)
    """
    user = ui.config(CONFIG_SECTION, b'user')
    if not user:
        raise error.Abort(
            _('BitBucket username not set. ' +
              'Please, set user= option in [bitbucketize] section (to short Bitbucket username))'))

    login = ui.config(CONFIG_SECTION, b'login')
    if not login:
        raise error.Abort(
            _('BitBucket login not set. ' +
              'Please, set login= option in [bitbucketize] section (to Atlassian username you use for browser login, usually it\'s your email))'))

    alias = None
    if not name:
        # User did not specify bitbucket name on the command line
        if not repo:
            raise error.Abort(_("""BitBucket repository name not specified
(it is required when command is executed outside any repository"""))
        alias = ui.config(CONFIG_SECTION, b'path_alias')
        if not alias:
            raise error.Abort(_("""BitBucket repository name not specified
(specify it or configure path_alias in [bitbucketize] section to deduce)"""))
        # name = ui.expandpath(alias)  # No, we don't want default or alias
        name = ui.config(b'paths', alias)
        if not name:
            raise error.Abort(_(b"""Alias %s can not be resolved
(either specify BitBucket repository name as parameter, or define %s path)""") %
                              (alias, alias))
    else:
        name = meu.pycompat.bytestr(name)

    match = re_path.search(name)
    if not match:
        raise error.Abort(_("""Invalid BitBucket path: %(name)s
Expected one of the following:
    https://bitbucket.org/%(user)s/repo-name
    bitbucket.org/%(user)s/repo-name
    %(user)s/repo-name
    repo-name
""") % {'name': name, 'user': user})

    match_user, match_name = match.group('user'), match.group('name')
    if match_user:
        if match_user != user:
            raise error.Abort(_("""Username inconsistency.
You configured your BitBucket username (user in [bitbucketize]) as %s,
but given path %s belongs to %s""") % (user, name, match_user))

    return user, login, match_name, alias


def err_means_missing_repo(err):
    """Checks whether given exception means missing repository"""
    err_tn = type(err).__name__
    if err_tn == 'HTTPError':
        if hasattr(err, 'response') and \
           hasattr(err.response, 'status_code') and \
           err.response.status_code == 404:
            return True
    return False


def _setup_passwordmgr(ui):
    """Compatibility layer for passwordmgr object creation"""
    # In Mercurial 2c019aac6b99 (published in 3.9) passwordmgr
    # constructor changed (separate parameter for password database).
    # As the change changed base class at the same time, let's use
    # this to test
    import mercurial.url as url
    if url.passwordmgr.__bases__[0] == object:
        # New version, 2-param constructor
        pwmgr = url.passwordmgr(ui,
                                url.urlreq.httppasswordmgrwithdefaultrealm())
    else:
        pwmgr = url.passwordmgr(ui)
    return pwmgr


def bb_connect(ui, user, login, repo_name):
    """Setup Bb connection and return client object"""

    bitbucket = import_pybitbucket('bitbucket')
    auth = import_pybitbucket('auth')
    pwmgr = _setup_passwordmgr(ui)

    # Calculating bitbucket repo url.
    # user, login, repo are taken from config, so in hg50+py3 they are
    # bytestr,  therefore we use bytes 
    bb_url = b"https://%(login)s@bitbucket.org/%(user)s/%(name)s" % {
        b'login': login, b'user': user, b'name': repo_name}
    # … but find_user_password expects str, so we normalize
    bb_url = meu.pycompat.sysstr(bb_url)

    # Extracting authorization data.
    # This should utilize mercurial_keyring, if enabled.
    http_user, http_pwd = pwmgr.find_user_password(
        "BitBucket.org", bb_url)

    return bitbucket.Client(
        auth.BasicAuthenticator(http_user, http_pwd, user)
    )


def bb_load_details(ui, bb_client, bb_user, bb_repo_name):
    """Load and returns details of given repo.
    If it is not found, or can't be loaded, prints appropriate
    warnings and returns None"""
    BitbucketRepository = import_pybitbucket('repository').Repository
    try:
        bb_repo = BitbucketRepository.find_repository_by_name_and_owner(
            owner=bb_user, repository_name=bb_repo_name, client=bb_client)
        if isinstance(bb_repo, type({})):
            # Raw dictionary returned. pybitbucket so far works this way,
            # I am not sure why but let's fix it up
            data = bb_repo
            bb_repo = BitbucketRepository(data=data, client=bb_client)
        return bb_repo
    except Exception as e:
        if err_means_missing_repo(e):
            ui.warn(meu.ui_string("\nRepository %s/%s does not exist on BitBucket\n",
                                  bb_user, bb_repo_name))
        else:
            ui.traceback()   # Print traceback if --traceback given
            ui.warn(meu.ui_string("\nFailed to load repository data: %s: %s\n",
                                  type(e).__name__, str(e)))


# At the moment repository.put is supported only on 1.0 API.
# I leave the code for 2.0 to enable it if it happens.
API_V2_SUPPORTS_MODIFY = False


def bb_modify(ui, bb_repo,
              has_wiki=None, has_issues=None, is_private=None,
              fork_policy=None, description=None, language=None):
    """Applies given modifications to the repo.
    Returns reply (whatever it is)  if succeeded, None on failure (after logging the error)"""

    # Some docs:
    # https://confluence.atlassian.com/bitbucket/repositories-endpoint-1-0-296092719.html
    # https://confluence.atlassian.com/bitbucket/repository-resource-1-0-296095202.html#repositoryResource1.0-PUTarepositoryupdate

    def setstr(payload, name, value):
        if value is not None:
            payload[name] = value

    if API_V2_SUPPORTS_MODIFY:
        def setbool(payload, name, value):
            if value is not None:
                payload[name] = value
    else:
        def setbool(payload, name, value):
            if value is not None:
                payload[name] = "true" if value else "false"

    # pybitbucket doesn't have make_payload for repository, so ...
    payload = {}
    setbool(payload, "has_wiki", has_wiki)
    setbool(payload, "has_issues", has_issues)
    setbool(payload, "is_private", is_private)
    setstr(payload, "description", description)
    setstr(payload, "language", language)
    if fork_policy is not None:
        if API_V2_SUPPORTS_MODIFY:
            payload["fork_policy"] = fork_policy
        else:
            if fork_policy == 'allow_forks':
                payload['no_public_forks'] = "false"
                payload['no_forks'] = "false"
            elif fork_policy == 'no_public_forks':
                payload['no_public_forks'] = "true"
                payload['no_forks'] = "false"
            elif fork_policy == 'no_forks':
                payload['no_public_forks'] = "true"
                payload['no_forks'] = "true"

    if API_V2_SUPPORTS_MODIFY:
        ui.status(meu.ui_string("Applying BitBucket metadata changes (API v2)\n"))
    else:
        ui.status(meu.ui_string("Applying BitBucket metadata changes (API v1)\n"))
        payload['accountname'] = bb_repo.owner.username
        payload['repo_slug'] = bb_repo.name
        posted_url = bb_repo.links['self']['href']\
                            .replace('2.0', 'api/1.0')\
                            .replace('api.bitbucket.org', 'bitbucket.org')
        bb_repo.links['self']['href'] = posted_url
        ui.debug(meu.ui_string("PUT-ting %s\nPayload:\n%s\n",
                               posted_url, pprint.pformat(payload)))

    try:
        reply = bb_repo.put(payload)
    except Exception as err:
        detail = bb_unpack_error_details(ui, err)
        ui.warn(meu.ui_string("\nFailed to modify BitBucket repository: %s\n",
                              detail))
        return None

    ui.debug(meu.ui_string("put results: %s\n",
                           pprint.pformat(reply)))
    return reply


def bb_print_status(ui, bb_repo, raw=False):
    """Prints repository information

    :param bb_repo: repo data dictionary, as returned by load_bb_details
    """
    if raw:
        ui.status(meu.ui_string(pprint.pformat(bb_repo.__dict__) + "\n"))
    else:
        paths = u"\n".join([
            "    %-9s  %s" % ('(' + lnk['name'] + ')', lnk['href'])
            for lnk in bb_repo.links['clone']])
        if bb_repo.description:
            message = u"\n\n".join(
                textwrap.fill(
                    txt, width=65,
                    replace_whitespace=True, drop_whitespace=True,
                    initial_indent='    ', subsequent_indent='    ')
                for txt
                in bb_repo.description.replace('\r\n', '\n').split("\n\n"))
            descr = _('Description:\n') + message
        else:
            descr = _('No description')
        details = dict(
            full_name=bb_repo.full_name,
            scm=bb_repo.scm,
            language=bb_repo.language,
            access=bb_repo.is_private and "private" or "public",
            wiki=bb_repo.has_wiki and "yes" or "no",
            issues=bb_repo.has_issues and "yes" or "no",
            size="%0.1f kB" % (1.0 * bb_repo.size / 1024),
            forks=forks_api2opt(bb_repo.fork_policy),
            paths=paths,
            descr=descr,
            owner=bb_repo.owner.get('nickname', bb_repo.owner.get('username', u'')),
        )
        for name in details.keys():
            if isinstance(details[name], meu.pycompat.unicode):
                details[name] = details[name].encode("utf-8")
        ui.status(meu.ui_string(u"""
Repository: {full_name}  (scm: {scm}, size: {size})
Access: {access}   (owner: {owner})
Issues: {issues}, wiki: {wiki}, forks: {forks}, language: {language}
Paths:
{paths}
{descr}
""".encode("utf-8")).format(**details))


def enable_requests_debugging():
    """This enables console logging of final HTTP traffic"""
    import httplib
    import logging
    httplib.HTTPConnection.debuglevel = 2
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True


def bb_unpack_error_details(ui, err):
    """Tries to extract error details from exception.
    Returns best description it can find"""
    bitbucket = import_pybitbucket('bitbucket')

    # BitbucketError is common base for BadRequestError and ServerError
    if isinstance(err, bitbucket.BitbucketError):
        if isinstance(err, bitbucket.BadRequestError):
            # Those are usually readable texts worth showing as-is
            prefix = ''
        else:
            # ServerError and similar
            prefix = type(err).__name__ + ': '
        # Some exceptions have json payload. pybitbucket parses it
        # and returns where possible. Let's try... The payload is like
        # {"error": {"message": "Repository already exists."}}
        try:
            return prefix + err.error['message']
        except:  # pylint: disable=bare-except
            pass
        # If not, mayhaps we have 1.0 horror like
        # <ul class="errorlist"><li>__all__<ul class="errorlist"><li>Public repositories must allow public forks.</li></ul></li></ul>
        if hasattr(err, 'text'):
            errtxt = err.text
            match = re.search(
                r'^<ul class="errorlist">.*?<li>([^<>]+)</li></ul>',
                errtxt)
            if match:
                return prefix + match.group(1)
            else:
                return errtxt
    # Fallback
    ui.traceback()   # Print traceback if --traceback given
    return "%s: %s" % (type(err).__name__, str(err))


############################################################
# Option validators/support
############################################################

# Mapping between --forks values and bb-api values
_BB_FORKS = [
    ('public', 'allow_forks'),           # unrestricted forking
    ('private', 'no_public_forks'),      # only private forks
    ('no', 'no_forks'),                  # deny all forking
]
_BB_FORKS_ALLOWED = meu.pycompat.bytestr(", ".join([v[0] for v in _BB_FORKS]))


def forks_opt2api(given_value, default=None):
    """Parses --forks value returning value for use in BB API.
    If default is given, fallbacks to it if value is missing, elsewhere fails"""
    if not given_value:
        if default:
            return default
    for mbval, apival in _BB_FORKS:
        if mbval == given_value:
            return apival
    raise error.Abort(_('Bad value of --forks: %s (expected one of: %s)') % (
        given_value, _BB_FORKS_ALLOWED))


def forks_opt2api_enum(given_value, default=None):
    """As above but wraps in expected enum"""
    repository = import_pybitbucket('repository')
    BbForkPolicy = repository.RepositoryForkPolicy
    return BbForkPolicy(forks_opt2api(given_value, default))


def forks_api2opt(api_value):
    """Converts BB API forks value into more readable one"""
    for mbval, apival in _BB_FORKS:
        if apival == api_value:
            return mbval
    return api_value  # fallback


############################################################
# Other utilities
############################################################


def open_browser(ui, url):
    """
    Spawns web browser on given url. Uses
        [browser]
    config section if present. There the browser itself can
    be specified either by sth like
        type = firefox
    where value is one of documented at
    https://docs.python.org/2/library/webbrowser.html
    (firefox, chrome, opera, safari, konqueror…) or just
    by:
        command = /usr/bin/firefox
    (the former is slightly preferable, if working, as it
    can autoraise window etc).

    If [browser] section is absent, falls back to system
    defaults (clickable settings, BROWSER variable etc).
    """
    ui.status(meu.ui_string("Opening web browser on %s\n",
                            url))
    import webbrowser
    cmd = ui.config('browser', 'command')
    if cmd:
        browser_type = 'hg-browser'
        webbrowser.register(browser_type, None, webbrowser.GenericBrowser(cmd))
    else:
        browser_type = ui.config('browser', 'type')
    try:
        browser_controller = webbrowser.get(browser_type)
    except webbrowser.Error:
        ui.traceback()   # Print traceback if --traceback given
        ui.warn(meu.ui_string(
            "Can not locate browser (bad type=%s in [browser] section). Using default.\n",
            browser_type))
        browser_controller = webbrowser.get()
    browser_controller.open(url, autoraise=True)


############################################################
# Commands
############################################################

cmdtable = {}
command = meu.command(cmdtable)

BB_REPO_FEATURE_OPTS = [
    # Third param is default, but also designates type
    (b'w', b'wiki', False, _(b'enable wiki')),
    (b'x', b'no-wiki', False, _(b'disable wiki')),
    (b'i', b'issues', False, _(b'enable issue tracker')),
    (b'j', b'no-issues', False, _(b'disable issues')),
    (b'p', b'public', False, _(b'make public')),
    (b'r', b'private', False, _(b'make private')),
    (b'f', b'forks', b'', _(b'forks approach: %s') % _BB_FORKS_ALLOWED),
    (b'm', b'descr', b'', _(b'repository description'), _(b'DESCRIPTION')),
    (b'l', b'language', b'', _(b'programming language')),
]


@command(b"bitbucket_create|bb_create",
         [
             item for item in BB_REPO_FEATURE_OPTS
             if item[1] not in [b'no-wiki', b'no-issues', b'private']
         ],
         _(b"[NAME] [--public] [--issues] [--wiki] [--descr='...'] [--lang=LANG]"),
         optionalrepo=True)
def cmd_bb_create(ui, repo, name=None, **opts):
    """create BitBucket clone of current repo

    Does not push, just creates properly named repository
    """
    repository = import_pybitbucket('repository')
    BbRepository = repository.Repository
    BbPayload = repository.RepositoryPayload
    BbRepoType = repository.RepositoryType

    bb_user, bb_login, bb_repo_name, bb_alias \
        = calculate_user_and_repo(ui, repo, name)
    ui.status(meu.ui_string("Creating BitBucket repo %s/%s\n",
                            bb_user, bb_repo_name))
    bb_client = bb_connect(ui, bb_user, bb_login, bb_repo_name)

    try:
        is_public = bool(opts.get('public'))
        payload = BbPayload() \
            .add_scm(BbRepoType.HG) \
            .add_fork_policy(forks_opt2api_enum(
                opts['forks'],
                default='allow_forks' if is_public else 'no_public_forks')) \
            .add_is_private(not is_public) \
            .add_description(opts.get('descr', '')) \
            .add_language(opts.get('language')) \
            .add_has_issues(opts.get('issues')) \
            .add_has_wiki(opts.get('wiki'))
        bb_repo = BbRepository.create(
            payload=payload,
            repository_name=bb_repo_name,
            owner=bb_user,
            client=bb_client)
        ui.status(meu.ui_string("Repository created\n"))
        ui.debug(meu.ui_string("Creation reply: %s",
                               pprint.pformat(bb_repo)))
        # create_repository returns seriously truncated and incompatible
        # repository details. So we can't really use it straight away,
        # instead let's check details
        bb_repo = bb_load_details(ui, bb_client, bb_user, bb_repo_name)
        bb_print_status(ui, bb_repo, raw=opts.get('raw'))
        bb_url = bb_repo.links['html']['href']
        ui.status(meu.ui_string("""
Now `hg push %s` to push the code
Visit %s to review details
""",
                                bb_alias or bb_url, bb_url))
    except Exception as e:
        detail = bb_unpack_error_details(ui, e)
        ui.warn(meu.ui_string("\nFailed to create BitBucket repository: %s\n",
                              detail))
        return True


@command(b"bitbucket_modify|bb_modify",
         BB_REPO_FEATURE_OPTS,
         _(b"[NAME] [--public|--private] [--issues|--no-issues] [--wiki|--no-wiki] [--descr=DESCR] [--lang=LANG]"),
         optionalrepo=True)
def cmd_bb_modify(ui, repo, name=None, **opts):   # pylint: disable=too-many-branches,too-many-statements
    """update BitBucket clone metadata"""
    bb_user, bb_login, bb_repo_name, __ \
        = calculate_user_and_repo(ui, repo, name)
    bb_client = bb_connect(ui, bb_user, bb_login, bb_repo_name)
    bb_repo = bb_load_details(ui, bb_client, bb_user, bb_repo_name)
    if not bb_repo:
        return True

    args = {}
    if opts.get('wiki'):
        args['has_wiki'] = True
    elif opts.get('no_wiki'):
        args['has_wiki'] = False
    if opts.get('issues'):
        args['has_issues'] = True
    elif opts.get('no_issues'):
        args['has_issues'] = False
    if opts.get('private'):
        args['is_private'] = True
    elif opts.get('public'):
        args['is_private'] = False
    if opts.get('forks'):
        args['fork_policy'] = forks_opt2api(opts['forks'])
    else:
        # BitBucket fails with 'public repositories must allow public forks'
        # if forks model is not public. So let's accomodate that as user
        # hasn't decided otherwise. For symmetry switch back when going priv
        if opts.get('public'):
            args['fork_policy'] = 'allow_forks'
        if opts.get('private'):
            args['fork_policy'] = 'no_public_forks'
    if opts.get('descr'):
        args['description'] = opts['descr']
    if opts.get('language'):
        args['language'] = opts['language']

    if not args:
        ui.warn(meu.ui_string("Nothing to change\n"))
        return False

    if not bb_modify(ui, bb_repo, **args):
        return True
    ui.status(meu.ui_string("Changes saved\n"))

    bb_repo = bb_load_details(ui, bb_client, bb_user, bb_repo_name)
    if not bb_repo:
        return True
    bb_print_status(ui, bb_repo)


@command(b"bitbucket_status|bb_status",
         [
             (b'r', b'raw', False, _(b'dumb raw technical data')),
         ],
         _(b"[NAME] [--raw]"),
         optionalrepo=True)
def cmd_bb_status(ui, repo, name=None, **opts):
    """checks and prints BitBucket clone status"""
    bb_user, bb_login, bb_repo_name, __ \
        = calculate_user_and_repo(ui, repo, name)
    ui.status(meu.ui_string("Checking status of BitBucket repo %s belonging to %s\n",
                            bb_repo_name, bb_user))
    bb_client = bb_connect(ui, bb_user, bb_login, bb_repo_name)
    bb_repo = bb_load_details(ui, bb_client, bb_user, bb_repo_name)
    if bb_repo:
        bb_print_status(ui, bb_repo, raw=opts.get('raw'))
    else:
        return True


@command(b"bitbucket_delete|bb_delete",
         [
             (b'', b'force', False, _(b'do not prompt, delete repository straight away')),
         ],
         _(b"[NAME]"),
         optionalrepo=True)
def cmd_bb_delete(ui, repo, name=None, **opts):
    """delete BitBucket clone"""
    bb_user, bb_login, bb_repo_name, __ \
        = calculate_user_and_repo(ui, repo, name)
    bb_client = bb_connect(ui, bb_user, bb_login, bb_repo_name)
    bb_repo = bb_load_details(ui, bb_client, bb_user, bb_repo_name)
    if not bb_repo:
        return True
    bb_print_status(ui, bb_repo)
    if not opts.get('force'):
        val = ui.promptchoice(
            _('are you sure to delete this repository (Y/N)?'
              '$$ &Yes $$ &No'),
            default=1)
    else:
        val = 0
    if val == 0:
        ui.status(meu.ui_string("Deleting BitBucket clone %s\n",
                                bb_repo.full_name))
        bb_repo.delete()
        ui.status(meu.ui_string("BitBucket clone deleted\n"))
    else:
        ui.status(meu.ui_string("OK, not deleting\n"))


# List of bitbucket web pages inside repo. Used to construct
# and interpret bb_goto params. Every item has, in order:
# - short option
# - long option
# - url snippet
# - description
BB_SUB_PAGES = [
    (b'', b'overview', b'overview', _(b'goto overview')),
    (b's', b'source', b'src', _(b'goto source')),
    (b'l', b'log', b'commits', _(b'goto commits (history)')),
    (b'b', b'branches', b'branches', _(b'goto branches')),
    (b'p', b'pulls', b'pull-requests', _(b'goto pull-requests')),
    (b'd', b'downloads', b'downloads', _(b'goto downloads')),
    (b'a', b'admin', b'admin', _(b'goto admin')),
    (b'i', b'issues', b'issues?status=new&status=open', _(b'goto issues')),
]


@command(b"bitbucket_goto|bb_goto",
         [
             (bb_short, bb_long, False, bb_descr)
             for bb_short, bb_long, __, bb_descr in BB_SUB_PAGES
         ],
         _(b"[NAME] [" + b"|".join([b"--" + bb_p[1] for bb_p in BB_SUB_PAGES]) + b"]"),
         optionalrepo=True)
def cmd_bb_goto(ui, repo, name=None, **opts):
    """open web browser on BitBucket repository page"""
    bb_user, bb_login, bb_repo_name, __ \
        = calculate_user_and_repo(ui, repo, name)

    # Pick the page
    page_sfx = BB_SUB_PAGES[0][2]   # default
    for __, option, sfx, __ in BB_SUB_PAGES:
        if opts.get(option):
            page_sfx = sfx

    url = b'https://bitbucket.org/%s/%s/%s' % (bb_user, bb_repo_name, page_sfx)

    open_browser(ui, url)


############################################################
# Extension setup
############################################################

# testedwith = '3.0 3.1.2 3.3 4.7'
buglink = 'https://foss.heptapod.net/mercurial/mercurial-bitbucketize/issues'
