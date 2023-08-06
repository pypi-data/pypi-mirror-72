# BOTLIB - the bot library !
#
#

import os, time

import bot.obj

from .dbs import Db, last
from .fil import cdir
from .irc import Cfg
from .krn import k, starttime, __version__
from .obj import Object, tostr, get_type, save
from .prs import parse
from .tms import elapsed, fntime

def __dir__():
    return ("cfg", "cmds", "find", "fl", "krn", "mods", "up", "v")

def cfg(event):
    c = Cfg()
    last(c)
    parse(event, event.txt)
    if event.sets:
        c.update(event.sets)
        save(c)
    event.reply(tostr(c))

def cmds(event):
    event.reply("|".join(sorted(k.cmds)))

def find(event):
    if not event.args:
        wd = os.path.join(bot.obj.workdir, "store", "")
        cdir(wd)
        fns = os.listdir(wd)
        fns = sorted({x.split(os.sep)[0] for x in fns})
        if fns:
            event.reply("|".join(fns))
        return
    db = Db()
    target = db.all
    otype = event.args[0]
    try:
        match = event.args[1]
        target = db.find_value
    except IndexError:
        match = None
    try:
        args = event.args[2:]
    except ValueError:
        args = None
    nr = -1
    for o in target(otype, match):
        nr += 1
        event.display(o, str(nr), args or o.keys())
    if nr == -1:
        event.reply("no %s found." % otype)

def fl(event):
    try:
        index = int(event.args[0])
        event.reply(str(k.fleet.bots[index]))
        return
    except (TypeError, ValueError, IndexError):
        pass
    event.reply([get_type(x) for x in k.fleet])

def krn(event):
    event.reply(k)

def mods(event):
    from .tbl import names
    event.reply("|".join({x.split(".")[-1] for x in names.values()}))

def up(event):
    event.reply(elapsed(time.time() - starttime))

def v(event):
    event.reply("%s %s" % ("BOTLIB", __version__))
