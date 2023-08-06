# BOTLIB - the bot library !
#
#

import threading

from .krn import k
from .obj import Cfg, Object
from .hdl import Event
from .shl import setcompleter
from .thr import launch

def __init__():
    return ("Cfg", "Console", "init")

def init(kernel):
    c = Console()
    c.start()
    return c

class Cfg(Cfg):

    pass

class Console(Object):

    def __init__(self):
        super().__init__(self)
        self.ready = threading.Event()

    def announce(self, txt):
        pass

    def input(self):
        while 1:
            event = self.poll()
            event.orig = repr(self)
            k.queue.put(event)
            event.wait()
        self.ready.set()

    def poll(self):
        e = Event()
        e.speed = "fast"
        e.txt = input("> ")
        return e

    def raw(self, txt):
        print(txt.rstrip())

    def say(self, channel, txt):
        self.raw(txt)

    def start(self):
        setcompleter(k.cmds)
        launch(self.input)

    def wait(self):
        self.ready.wait()
