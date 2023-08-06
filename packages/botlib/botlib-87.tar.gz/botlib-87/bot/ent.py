# BOTLIB - the bot library !
#
#

from .dbs import Db
from .obj import Object, save

def __init__():
    return ("Log", "TOdo", "done", "log", "todo") 

class Log(Object):

    def __init__(self):
        super().__init__()
        self.txt = ""

class Todo(Object):

    def __init__(self):
        super().__init__()
        self.txt = ""

def done(event):
    if not event.args:
        event.reply("done <match>")
        return
    selector = {"txt": event.args[0]}
    db = Db()
    for o in db.find("bot.ent.Todo", selector):
        o._deleted = True
        save(o)
        event.reply("ok")
        break

def log(event):
    if not event.rest:
        db = Db()
        res = db.find("bot.ent.Log", {"txt": ""})
        nr = 0
        for o in res:
            event.reply("%s %s %s" % (str(nr), o.txt, elapsed(time.time() - fntime(o._path))))
            nr += 1
        if not nr:
            event.reply("log what ?")
        return
    l = Log()
    l.txt = event.rest
    save(l)
    event.reply("ok")

def todo(event):
    db = Db()
    if not event.rest:
        res = db.find("bot.ent.Todo", {"txt": ""})
        if not res:
            return
        nr = 0
        for o in res:
            event.reply("%s %s %s" % (str(nr), o.txt, elapsed(time.time() - fntime(o._path))))
            nr += 1
        if not nr:
            event.reply("do what ?")
        return
    o = Todo()
    o.txt = event.rest
    save(o)
    event.reply("ok")
