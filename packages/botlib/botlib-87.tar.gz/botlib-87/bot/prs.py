# BOTLIB - the bot library
#
#

import os, sys
import bot.obj

from .obj import Cfg, Default, Object

def __dir__():
    return ("parse", "parse_cli")

class Token(Object):

    def __init__(self, txt):
        super().__init__()
        self.txt = txt

class Option(Default):

    def __init__(self, txt):
        super().__init__()
        if txt.startswith("--"):
            self.opt = txt[2:]
        if txt.startswith("-"):
            self.opt = txt[1:]

class Getter(Object):

    def __init__(self, txt):
        super().__init__()
        try:
            pre, post = txt.split("==")
        except ValueError:
            pre = post = ""
        if pre:
            self[pre] = post

class Setter(Object):

    def __init__(self, txt):
        super().__init__()
        try:
            pre, post = txt.split("=")
        except ValueError:
            pre = post = ""
        if pre:
            self[pre] = post

def getwd():
    if root():
        return "/var/lib/botd"
    return os.path.expanduser("~/.bot")

def parse(o, txt):
    args = []
    opts = []
    o.origtxt = txt
    o.gets = Default()
    o.opts = Default()
    o.sets = Default()
    for token in [Token(txt) for txt in txt.split()]:
        g = Getter(token.txt)
        if g:
            o.gets.update(g)
            continue
        s = Setter(token.txt)
        if s:
            o.sets.update(s)
            o.update(s)
            continue
        opt = Option(token.txt)
        if opt.opt:
            o.opts[opt.opt] = True
            continue
        args.append(token.txt)
    if not args:
        return o
    o.cmd = args[0]
    o.args = args[1:]
    o.txt = " ".join(args)
    o.rest = " ".join(args[1:])
    return o

def parse_cli():
    if len(sys.argv) <= 1:
        return Cfg()
    c = Cfg()
    parse(c, " ".join(sys.argv[1:]))
    setwd(c.wd or getwd())
    return c

def root():
    if os.geteuid() != 0:
        return False
    return True

def setwd(wd):
    bot.obj.workdir = wd
