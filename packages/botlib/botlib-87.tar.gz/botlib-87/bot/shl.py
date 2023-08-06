# BOTLIB - the bot library !
#
#

import atexit, os, pwd, readline, sys, termios

import bot.obj

from .obj import Cfg
from .prs import parse
from .fil import cdir, touch

def __dir__():
    return ("bexec", "close_history", "drop", "enable_history", "execute", "get_completer", "termsave", "termreset", "writepid")

cmds = []
logfile = ""
resume = {}
HISTFILE = ""

def bexec(f, *args, **kwargs):
    try:
        return f(*args, **kwargs)
    except KeyboardInterrupt:
        print("")
    except PermissionError:
        print("you need root permissions.")

def close_history():
    global HISTFILE
    if bot.obj.workdir:
        if not HISTFILE:
            HISTFILE = os.path.join(bot.obj.workdir, "history")
        if not os.path.isfile(HISTFILE):
            cdir(HISTFILE)
            touch(HISTFILE)
        readline.write_history_file(HISTFILE)

def complete(text, state):
    matches = []
    if text:
        matches = [s for s in cmds if s and s.startswith(text)]
    else:
        matches = cmds[:]
    try:
        return matches[state]
    except IndexError:
        return None

def drop():
    ruid = pwd.getpwnam("botd")[2]
    os.setuid(ruid)
    os.umask(0o007)

def enable_history():
    assert bot.obj.workdir
    global HISTFILE
    HISTFILE = os.path.abspath(os.path.join(bot.obj.workdir, "history"))
    if not os.path.exists(HISTFILE):
        cdir(HISTFILE)
        touch(HISTFILE)
    else:
        readline.read_history_file(HISTFILE)
    atexit.register(close_history)

def execute(main):
    termsave()
    try:
        main()
    except KeyboardInterrupt:
        print("")
    except PermissionError:
        print("you need root permissions.")
    finally:
        termreset()

def get_completer():
    return readline.get_completer()

def root():
    if os.geteuid() != 0:
        return False
    return True

def setcompleter(commands):
    cmds = commands
    readline.set_completer(complete)
    readline.parse_and_bind("tab: complete")
    atexit.register(lambda: readline.set_completer(None))

def setup(fd):
    return termios.tcgetattr(fd)

def termreset():
    if "old" in resume:
        termios.tcsetattr(resume["fd"], termios.TCSADRAIN, resume["old"])

def termsave():
    try:
        resume["fd"] = sys.stdin.fileno()
        resume["old"] = setup(sys.stdin.fileno())
        atexit.register(termreset)
    except termios.error:
        pass

def writepid():
    assert bot.obj.workdir
    path = os.path.join(bot.obj.workdir, "pid")
    if not os.path.exists(path):
        cdir(path)
    f = open(path, 'w')
    f.write(str(os.getpid()))
    f.flush()
    f.close()
