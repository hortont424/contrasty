import time
import termcolor

class Priority:
    FATAL = 4
    HIGH = 3
    NORMAL = 2
    LOW = 1

    @classmethod
    def getColor(cls, priority):
        return {cls.FATAL: "red", cls.HIGH: "yellow", cls.NORMAL: "green", cls.LOW: "white"}[priority]

def log(str, priority=Priority.NORMAL):
    if not hasattr(log, "logMessageCount"):
        log.logMessageCount = 0

    log.logMessageCount += 1

    logString = "[{0:6d}] ".format(log.logMessageCount) + termcolor.colored(str, Priority.getColor(priority))

    if priority >= Priority.LOW:
        print logString

    return log.logMessageCount

def logCall():
    def installLogging(f):
        def wrapper(*args, **keywords):
            startID = log("{0}()".format(f.func_name))
            startTime = time.clock()
            f(*args, **keywords)
            duration = (time.clock() - startTime) * 1000
            log("{0}() [{1}] done in {2}ms".format(f.func_name, startID, duration))
        return wrapper
    return installLogging