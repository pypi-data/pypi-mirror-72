# -*- coding: utf-8 -*-
#
# onremote: execute some Mercurial command on remote peer.
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

"""Execute some Mercurial command in remote repository.

For example::

    hg onremote production update -r 3.7.4

For more information, see
    https://foss.heptapod.net/mercurial/mercurial-on_remote/
"""

# pylint:disable=fixme,line-too-long,invalid-name
#   (invalid-name because of ui and cmdtable)

from mercurial import commands, util, dispatch, error, fancyopts, sshpeer
try:
    from mercurial.utils import procutil
except ImportError:
    # hg < 5
    from mercurial import util as procutil
from mercurial.i18n import _
import os
import sys


def import_meu():
    """
    Import mercurial_extension_utils.

    Handles some corner cases related to TortoiseHg@Win and similar installations.
    """
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
See Installation chapter in https://foss.heptapod.net/mercurial/mercurial-on_remote/ for details
(and for info about TortoiseHG on Windows, or other bundled Python)."""))
    return mercurial_extension_utils


meu = import_meu()

###########################################################################
# Constants
###########################################################################

ON_REMOTE_COMMAND = meu.pycompat.bytestr(b"onremote")

# Options actually handled on the local side (-e/--ssh and --remotecmd and irrelevant --insecure).
try:
    from mercurial.cmdutil import remoteopts as REMOTE_OPTS
    # In hg 3.* we may happen to get unloaded module here, and strange errors
    # during cmdtable population below
    if 'demandmod' in type(REMOTE_OPTS).__name__:
        raise ImportError("mercurial.cmdutil")
except ImportError:
    try:
        from mercurial.commands import remoteopts as REMOTE_OPTS
    except ImportError:
        # This shouldn't really happen, but to be safe…
        REMOTE_OPTS = [
            (b'e', b'ssh', b'', _(b'specify ssh command to use'), _(b'CMD')),
            (
                b'',
                b'remotecmd',
                b'',
                _(b'specify hg command to run on the remote side'),
                _(b'CMD'),
            ),
        ]



###########################################################################
# Compatibility
###########################################################################

# Wrapper for fancyopts.fancyopts. We try to use "early" if possible
# (to get more suitable errors and accomodate more options ordering) ,
# but it was available only since hg 4.5
def call_partial_fancyopts(args, options, state):
    if 'early' in fancyopts.fancyopts.__code__.co_varnames:
        return fancyopts.fancyopts(args, options, state, gnu=True, early=True)
    else:
        # Old mercurial. We have no way to use fancyopts to parse full args
        # as it will likely grok on any --option specific to command
        # called (we don't have early=True). So we try to truncate args until
        # we succeed. This won't handle some orderings but in typical cases
        # (where we have hg «globals» onremote «onremote opts» command «commandopts»
        # will usually do.
        parse_to_pos = len(args)
        while parse_to_pos > 0:
            try:
                # fancyopts edits argument, therefore we must preserve it.
                parsed_args = args[:parse_to_pos]
                ret = fancyopts.fancyopts(parsed_args, options, state, gnu=True)
                return ret + args[parse_to_pos:]
            except Exception as err:
                if type(err).__name__ in ['GetoptError', 'CommandError']:
                    parse_to_pos -= 1
                else:
                    raise error.CommandError(None, err.args[0])
        # Raczej nie powinniśmy tu dojść ale dla pewności
        raise error.CommandError(None, "Incorrect arguments")


def call_checksafessh(path):
    try:
        return util.checksafessh(path)
    except AttributeError:
        pass


# API below is incomplete, only args we use!
def call_system(ui, cmd, environ=None, cwd=None, blockedtag=None):
    if 'blockedtag' in fancyopts.fancyopts.__code__.co_varnames:
        return ui.system(cmd, environ=environ, cwd=cwd, blockedtag=blockedtag)
    else:
        # py3.* compat
        if environ is None:
            environ = {}
        return ui.system(cmd, environ=environ, cwd=cwd)


def call_getpath(ui, remote):
    # This could open way to using default path, but breaks on hg3.*
    # remote_path = ui.paths.getpath(remote, default=(b'default-push', b'default'))
    remote_path = ui.paths.getpath(remote)

    if not remote_path:
        # Old Mercurials didn't handle dire/ctories or ssh://addr/esses here.
        # Current behaviour started from 3.6. Accidentally at the same moment
        # pushloc attribute was introduced which we also need to patch…
        from mercurial.ui import path as uipath
        if 'pushloc' not in uipath.__init__.__code__.co_varnames:
            # Let's emulate, at least some bits… (people needing #branch urls may upgrade hg)
            # On newer hg's line below will crash due to lack of ui=None
            remote_path = uipath(name=None, rawloc=remote)
            # To be truly in sync we should raise here if path has invalid syntax,
            # and isn't remote but doesn't point to local dir. But it will cause similar
            # errors later.
        else:
            # Shouldn't happen but to make sure…
            raise error.Abort(
                _(b'Can\'t resolve remote %s!') % remote,
                hint=_(b"see 'hg paths' for available remotes"),
            )

    # Another old hg compat, here just missing attribute we test…
    if not hasattr(remote_path, 'pushloc'):
        remote_path.pushloc = None
        # Minimal validation in case of local path, to throw an error here
        # instead of waiting for called sub-hg to fail. Rough translation
        # of ui.path constructor from hg >= 3.6, but we must change exception
        u = util.url(remote_path.loc)
        if u.fragment:
            remote_path.branch = u.fragment
            u.fragment = None
        remote_path.loc = str(u)
        if not remote_path.name and not u.scheme:
            if not os.path.isdir(os.path.join(remote_path.loc, b'.hg')):
                raise error.Abort(
                    b'repository %s not found (expected alias, URL, or path to local repo)'
                    % remote_path.loc)

    return remote_path


def call_shellenviron(environ=None):
    # This function was introduced in hg 4.1
    try:
        return procutil.shellenviron(environ)
    except AttributeError:
        # hg <= 4.0. sshenv isn't likely to be foudn there, so let's just shut it up
        return {}


############################################################
# Mercurial monkeypatching
#
# We wish to capture all options and args in commands
# like
#     hg onremote sauter up -r 1.3.2
# and predeclaring them all seems difficult and unpleasant.
#
# Pro and cons at the same time: we validate arguments
# locally before issuing the command on the remote.
# This generally saves some time, but may forbid option
# which is available remotely but missing locally.
############################################################

@meu.monkeypatch_function(dispatch)
def _parse(lui, args):
    """Monkeypathed Mercurial own parse.

    Modifies parsing behaviour in case onremote command is being
    handled. We generally need to accept various commands with
    their options, and wish to forward them to the backend mercurial.

    Still, we wish to handle „local” options like ``--debug``
    or ``--verbose``, or even ``--ssh``. We also need to resolve
    shortened command (``onrem``). Finally, we'd like to handle
    ``--ssh``/``-e`` and ``--remotecmd``, just like push does.

    And of course we need to backtrack if any other command happens
    to be executed.

    Mercurial`s ``_parse`` returns 5-tuple (and we must preserve
    the API):

    - command name (resolved),
    - command function callback,
    - args (positional arguments)
    - options (dictionary of resolved mercurial global flags, like quiet or debug)
    - cmdoptions (dictionary of resolved command-specific, declared options)

    In our case, if we detect ``onremote`` command, we return:

    - ``'onremote'``
    - actual onremote callback (``cmd_onremote``)
    - two args: remote name, and actual command name
    - global options as resolved
    - cmdoptions which may contain resolved ``ssh`` or ``remotecmd``
      but where we also add ``remote_full_args`` with full list
      of all remote command arguments (ordered as written)
    """
    # Even when we run under --debug, lui does not (yet) know about that
    # (it is normally set inside _dispatch, after parse). To get debugging here…
    if b'--debug' in args:
        lui.debugflag = True

    lui.debug(meu.ui_string("on_remote: _parse called with args %r\n",
                            args))

    # First stage: we parse according to „normal rules” (normal specs).
    # This parse will in particular detect which command we execute after all.
    # 
    # If it is not onremote, we will simply return obtained result (or forward
    # obtained exception).
    #
    # If we execute onremote, parsing may succeed (in simple cases) or fail
    # due to unknown options (like due to -m in case of `hg remote sth commit -m "…"`).
    # In both cases we will know that we execute our command nevertheless.
    # Then we are to remove onremote, remote path, and possible ssh/remotecmd
    # arguments from the command line before reparsing it as final command
    # to validate the arguments.
    try:
        parsed = _parse.orig(lui, args)
        if parsed[0] is None:
            # User typed hg, hg --help or sth similar
            lui.debug(meu.ui_string("on_remote: _parse found no command\n"))
            return parsed
        if parsed[0] != ON_REMOTE_COMMAND:
            # Some other command is handled, we silently withdraw.
            lui.debug(meu.ui_string("on_remote: _parse found another command %s\n",
                                    parsed[0]))
            return parsed
        # First parse succeeded (no unknown options happened), good, no need to reparse
        lui.debug(meu.ui_string("on_remote: initial parse succeeded, no options conflict\n"))
        p_args, p_global_opts, p_local_opts = parsed[2], parsed[3], parsed[4]
        onrem_idx = 0  # See below
    except error.CommandError as e:
        if e.args[0] != ON_REMOTE_COMMAND:
            # Some other command got bad options, let it be handled normally
            raise
        # We handle onremote but parse failed due to unknown options.
        lui.debug(meu.ui_string("on_remote: normal parse failed but detected onremote, fixing up (%s)\n",
                                e))
        # We parse global options and „local side” options
        p_global_opts, p_local_opts = {}, {}
        p_args = call_partial_fancyopts(args, commands.globalopts + REMOTE_OPTS,
                                        p_global_opts)
        for opt in REMOTE_OPTS:   # Moving ssh/remotecmd out of previous global
            opt_name = opt[1]
            if opt_name in p_global_opts:
                p_local_opts[opt_name] = p_global_opts.pop(opt_name)

        # In this case p_args may contain --options, we used early

        # We have to drop our command and first positional arg from args
        # There is also tiny risk some --option stayed before it, so
        # we look there carefully.
        onrem_idx = 0
        # Testing just first letter to accomodate shortcuts. And patching things for py3
        lead_letter = ON_REMOTE_COMMAND[0]
        if sys.version_info >= (3, 0):
            lead_letter = ord(lead_letter)
        while onrem_idx < len(p_args):
            if p_args[onrem_idx][0] == lead_letter:
                break
            onrem_idx += 1
        if onrem_idx >= len(p_args):
            raise error.Abort(meu.ui_string(
                "onremote: Can not find command name in parsed arguments. Please, contact the extension author. Args: %s",
                p_args))
        p_args = p_args[:onrem_idx] + p_args[onrem_idx + 1:]

    # import pdb; pdb.set_trace()

    # Whichever way we got here, we should have remote name in p_args just after
    # onremote itself. We kept in onrem_idx the latter pos.
    if len(p_args) < onrem_idx + 1:
        raise error.CommandError(ON_REMOTE_COMMAND, _(b'invalid arguments (missing remote name)'))
    remote = p_args.pop(0)
    if (not remote) or (remote[0] in [b'-', ord(b'-')]):  # b'-' vs 111 for py3-compat
        raise error.CommandError(ON_REMOTE_COMMAND, _(b'invalid arguments (option %s instead of remote name)') % remote)

    # Parsing actual command to make sure it is correct before sending. This in particular
    # verifies the options before spending time on the connection.
    lui.debug(meu.ui_string("onremote: parsing stripped arguments %s\n", p_args))
    try:
        cmdparsed = _parse.orig(lui, p_args)
    except error.CommandError as err:
        # If we have no command in exception, we likely got sth like "hg onremote -l".
        # Let's patch it to avoid dumpling full Mercurial command list
        if err.args[0] is None:
            raise error.CommandError(ON_REMOTE_COMMAND, _(b'invalid arguments (%s)') % err.args[1])
        raise

    if cmdparsed[0] is None:
        raise error.CommandError(ON_REMOTE_COMMAND, _(b'command to run not specified'))

    lui.debug(meu.ui_string("on_remote: finished parsing. Returning wrapper for %s command\n",
                            cmdparsed[0]))
    return (
        ON_REMOTE_COMMAND,
        cmd_onremote,
        [remote, cmdparsed[0]],
        p_global_opts,   # From first parse, second didn't get options
        {
            # 'cmd': cmdparsed[0],
            b'cmdfunc': cmdparsed[1],
            b'cmdargs': cmdparsed[2],
            b'cmdoptions': p_local_opts,   # NOT cmdparsed[4],
            b'fullargs': args,
            b'options': p_global_opts,
            b'remote_args': p_args,
        }
    )


############################################################
# Mercurial extension hooks
############################################################

# def extsetup(ui):
#    """Setup extension: load patterns definitions from config"""
#    pass
#

############################################################
# Commands
############################################################

cmdtable = {}
command = meu.command(cmdtable)


@command(ON_REMOTE_COMMAND,
         REMOTE_OPTS,
         b"REMOTE-NAME ANY-MERCURIAL-COMMAND [COMMAND-ARGS]",
         inferrepo=True)
def cmd_onremote(ui, repo, remote, *args, **opts):
    """
    Execute given Mercurial command on remote repository
    """
    # print "UI", ui
    # print "REPO", repo
    # print "CMDNAME", cmdname
    # import pprint; print "OPTS", pprint.pformat(opts)

    # Provided by monkey-patched _parse
    cmdfunc = opts['cmdfunc']
    # actual function to call - status, log, update, …
    cmdargs = opts['cmdargs']
    # positional command args - whichever were given
    cmdoptions = opts['cmdoptions']
    # ssh, remotecmd  - our named options
    options = opts['options']
    # Global options - debug, verbose, encoding…
    fullargs = opts['fullargs']
    # Original args including onremote word and all args
    remote_args = opts['remote_args']
    # Everything for remote, including the command itself ['log', '-l', '3', '.']
    # This is what we actually use below.

    # Resolving remote alias (will raise if unknown path is given)
    remote_path = call_getpath(ui, remote)

    remote_dest = remote_path.pushloc or remote_path.loc

    # Inspecting obtained path
    remote_url = util.url(remote_dest, parsequery=False, parsefragment=False)
    if (not remote_url.scheme) and remote_url.path:
        # Remote is local directory
        using_ssh = False
    elif remote_url.scheme == b'ssh' and remote_url.host and remote_url.path:
        using_ssh = True
    else:
        raise error.RepoError(_(b"onremote: unsupported remote location type (expected ssh or local directory): %s") % remote_dest)

    # We are to call ['hg'] + remote_args either directly, or via ssh. In the latter case
    # we must calculate both ssh target, and various options.

    if using_ssh:
        # Calculating ssh command. Similar to sshpeer.
        call_checksafessh(remote_url.path)
        sshcmd = cmdoptions[b'ssh'] or ui.config(b'ui', b'ssh') or b'ssh'
        remotecmd = cmdoptions[b'remotecmd'] or ui.config(b'ui', b'remotecmd') or b'hg'
        sshaddenv = dict(ui.configitems(b'sshenv'))
        sshenv = call_shellenviron(sshaddenv)
        remotepath = remote_url.path or b'.'
        sshargs = procutil.sshargs(sshcmd, remote_url.host, remote_url.user, remote_url.port)
        cmd = b'%s %s %s' % (
            sshcmd,
            sshargs,
            procutil.shellquote(
                b' '.join([
                    sshpeer._serverquote(remotecmd),   # "hg"
                    b'-R',
                    sshpeer._serverquote(remotepath),  # "kata/log",
                ] + [
                    sshpeer._serverquote(item) for item in remote_args
                ])
            ),
        )
        ui.debug(b'on_remote: running %s\n' % cmd)
        res = call_system(ui, cmd, blockedtag=b'on_remote', environ=sshenv)
        if res != 0:
            raise error.RepoError(_(b'on_remote: could not spawn ssh command (%s)') % cmd)
    else:
        cmd = b' '.join([procutil.shellquote(item) for item in [
            procutil.hgexecutable(),
            b"-R",
            remote_url.path,
        ] + remote_args])
        ui.debug(b'on_remote: running %s\n' % cmd)
        res = call_system(ui, cmd, blockedtag=b'on_remote')
        if res != 0:
            raise error.RepoError(_(b'on_remote: could not spawn command (%s)') % cmd)

    return 0


############################################################
# Extension setup
############################################################

testedwith = '3.4 3.5 3.6 3.7 3.8 4.0 4.1 4.3 4.5 4.6 4.7 4.8 4.9 5.0'
buglink = 'https://foss.heptapod.net/mercurial/mercurial-on_remote/issues'
