# BOTLIB - the bot library !
#
#

__version__ = 87

import threading, time

from .dbs import Db
from .hdl import Handler
from .isp import direct
from .obj import Cfg, Object, save, spl
from .prs import parse_cli
from .thr import launch

def __dir__():
    return ("ENOKERNEL", "ENOUSER", "Cfg", "Kernel", "Fleet", "User", "Users", "k")

starttime = time.time()

class ENOKERNEL(Exception):

    pass

class ENOUSER(Exception):

    pass

class Cfg(Cfg):

    pass

class Kernel(Handler):

    def __init__(self):
        super().__init__()
        self.ready = threading.Event()
        self.stopped = False
        self.cfg = Cfg()
        self.db = Db()
        self.fleet = Fleet()
        self.users = Users()
        self.fleet.add(self)

    def init(self, mns):
        mods = []
        thrs = []
        for mn in spl(mns):
            ms = "bot.%s" % mn
            mod = self.load_mod(ms)
            mods.append(mod)
            func = getattr(mod, "init", None)
            if func:
                thrs.append(launch(func, k))
        for thr in thrs:
            thr.join()
        return mods

    def say(self, channel, txt):
        print(txt)

    def stop(self):
        self.stopped = True
        self.queue.put(None)

    def wait(self):
        while not self.stopped:
            time.sleep(60.0)

class Fleet(Object):

    bots = []

    def __iter__(self):
        return iter(Fleet.bots)

    def add(self, bot):
        Fleet.bots.append(bot)

    def announce(self, txt, skip=None):
        for h in self.bots:
            if skip is not None and isinstance(h, skip):
                continue
            if "announce" in dir(h):
                h.announce(txt)

    def dispatch(self, event):
        for b in Fleet.bots:
            if repr(b) == event.orig:
                b.dispatch(event)

    def by_orig(self, orig):
        for o in Fleet.bots:
            if repr(o) == orig:
                return o

    def by_cls(self, otype, default=None):
        res = []
        for o in Fleet.bots:
            if isinstance(o, otype):
                res.append(o)
        return res

    def by_type(self, otype):
        res = []
        for o in Fleet.bots:
            if otype.lower() in str(type(o)).lower():
                res.append(o)
        return res

    def say(self, orig, channel, txt):
        for o in Fleet.bots:
            if repr(o) == orig:
                o.say(channel, str(txt))

class User(Object):

    def __init__(self):
        super().__init__()
        self.user = ""
        self.perms = []

class Users(Db):

    userhosts = Object()

    def allowed(self, origin, perm):
        perm = perm.upper()
        origin = self.userhosts.get(origin, origin)
        user = self.get_user(origin)
        if user:
            if perm in user.perms:
                return True
        return False

    def delete(self, origin, perm):
        for user in self.get_users(origin):
            try:
                user.perms.remove(perm)
                save(user)
                return True
            except ValueError:
                pass

    def get_users(self, origin=""):
        s = {"user": origin}
        return self.all("bot.usr.User", s)

    def get_user(self, origin):
        u = list(self.get_users(origin))
        if u:
            return u[-1]

    def meet(self, origin, perms=None):
        user = self.get_user(origin)
        if user:
            return user
        user = User()
        user.user = origin
        user.perms = ["USER", ]
        save(user)
        return user

    def oper(self, origin):
        user = self.get_user(origin)
        if user:
            return user
        user = User()
        user.user = origin
        user.perms = ["OPER", "USER"]
        save(user)
        return user

    def perm(self, origin, permission):
        user = self.get_user(origin)
        if not user:
            raise ENOUSER(origin)
        if permission.upper() not in user.perms:
            user.perms.append(permission.upper())
            user.save()
        return user

k = Kernel()
