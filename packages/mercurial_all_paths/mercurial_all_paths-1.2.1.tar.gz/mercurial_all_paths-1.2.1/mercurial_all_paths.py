# -*- coding: utf-8 -*-
#
# allpaths.py - execute commands on multiple paths
#
# This software may be used and distributed according to the terms of
# the GNU General Public License version 2 or any later version.

'''execute commands on multiple paths'''

from mercurial import commands, cmdutil
from mercurial.error import Abort
import sys
import os
from mercurial.i18n import _


def import_meu():
    """Importing mercurial_extension_utils so it can be found also outside
    Python PATH (support for TortoiseHG/Win and similar setups)"""
    try:
        import mercurial_extension_utils
    except ImportError:
        my_dir = os.path.abspath(os.path.dirname(__file__))
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
            raise Abort(_("""Can not import mercurial_extension_utils.
Please install this module in Python path.
See Installation chapter in https://foss.heptapod.net/mercurial/mercurial-all_paths/ for details
(and for info about TortoiseHG on Windows, or other bundled Python)."""))

    if not hasattr(mercurial_extension_utils, 'command'):
        raise Abort(_("""Your mercurial_extension_utils is outdated.
See Installation chapter in https://foss.heptapod.net/mercurial/mercurial-all_paths/ for details."""))

    return mercurial_extension_utils


meu = import_meu()


# pylint:disable=invalid-name,broad-except,line-too-long

def _find_all_paths(ui, skip_ignored=False, sort_by_priority=False):
    """
    Finds all paths defined for repo
    :return: list of pairs (alias, path)
    """
    paths = ui.configitems(b"paths")
    if not paths:
        raise Abort(_('No paths defined for repository'))

    if skip_ignored:
        ignored = ui.configlist(b"all_paths", b"ignore")
        if ignored:
            paths = [(alias, path) for alias, path in paths if alias not in ignored]
            if not paths:
                raise Abort(_('All paths defined for this repository are ignored'))

    if sort_by_priority:
        prior = ui.configlist(b"all_paths", b"prioritize")
        if prior:
            prior_val = {}
            for idx, item in enumerate(prior):
                prior_val[item] = idx
            higher = len(prior)
            paths.sort(key = lambda it: prior_val.get(it[0], higher))

    return paths


def _find_paths(ui, group=None):
    """
    Finds and returns all paths defined in given group, or all paths
    (sans config) if group is not specified.

    :param ui: repository ui
    :param group: group name or None for all paths
    :return: list of pairs (alias, path)
    """
    if not group:
        return _find_all_paths(ui, skip_ignored=True, sort_by_priority=True)

    # „Modern” syntax
    grp_def = ui.configlist(b"all_paths", b"group." + group)
    if grp_def:
        all_paths = dict(_find_all_paths(ui))
        paths = []
        for item in grp_def:
            if item in all_paths:
                paths.append((item, all_paths[item]))
        if not paths:
            raise Abort(_('None of the paths from group %s is defined in this repository') % group)

        return paths

    # „Legacy” syntax, used also for all paths
    paths = ui.configitems(group)
    if not paths:
        raise Abort(_('No paths defined in section %s') % group)
    return paths


def _iter_over_paths(command, ui, repo, add_sep, **opts):
    """execute given command on multiple paths"""
    # Extract our options and filter them out
    group = opts.pop('group', None)
    ignore_errors = opts.pop('ignore_errors', None)

    # Get the paths to push to.
    paths = _find_paths(ui, group)

    # Used to avoid handling duplicate paths twice
    handled = {}
    # Used to add extra newline between items
    sep = b''

    # Act!
    for alias, path in paths:
        if path in handled:
            ui.status(sep + meu.ui_string("Skipping %s as path %s was already handled\n",
                                          alias, handled[path]))
            sep = b'\n'
        else:
            ui.status(sep)
            sep = b'\n' if add_sep else b''
            handled[path] = alias
            try:
                command(ui, repo, path, **opts)
            except Exception as e:
                if not ignore_errors:
                    raise
                ui.warn(meu.ui_string('error handling %s: %s\n',
                                      alias, e))
                sep = b'\n'


EXT_OPTS = [
    (b'g', b'group', b'', _(b'use a named group instead of all paths')),
    (b'', b'ignore-errors', None, _(b'continue execution despite errors')),
]


def _original_options(cmdname):
    """Gets list of given command options as specified in Mercurial core"""
    _, spec = cmdutil.findcmd(cmdname, commands.table)
    return spec[1]


cmdtable = {}
command = meu.command(cmdtable)


@command(b"pushall",
         EXT_OPTS + _original_options(b'push'),
         _(b'[-g GROUP] [--ignore-errors] <push options>'))
def pushall(ui, repo, **opts):
    """execute push on multiple paths"""
    _iter_over_paths(commands.push, ui, repo, True, **opts)


@command(b"pullall",
         EXT_OPTS + _original_options(b'pull'),
         _(b'[-g GROUP] [--ignore-errors] <pull options>'))
def pullall(ui, repo, **opts):
    """execute pull on multiple paths"""
    _iter_over_paths(commands.pull, ui, repo, True, **opts)


@command(b"incomingall",
         EXT_OPTS + _original_options(b'incoming'),
         _(b'[--group GROUP] [--ignore-errors] <incoming options>'))
def incomingall(ui, repo, **opts):
    """execute incoming on multiple paths"""
    _iter_over_paths(commands.incoming, ui, repo, False, **opts)


@command(b"outgoingall",
         EXT_OPTS + _original_options(b'outgoing'),
         _(b'[--group GROUP] [--ignore-errors] <outgoing options>'))
def outgoingall(ui, repo, **opts):
    """execute outgoing on multiple paths"""
    _iter_over_paths(commands.outgoing, ui, repo, False, **opts)


testedwith = '2.7 2.9 3.0 3.3 3.6 3.7 3.8 4.0 4.1 4.2 4.3 4.5 4.6 4.7 4.8 5.0'
buglink = 'https://foss.heptapod.net/mercurial/mercurial-all_paths/issues'
