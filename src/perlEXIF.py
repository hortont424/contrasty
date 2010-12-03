from json import loads
from subprocess import Popen, PIPE

def readEXIFData(fn):
    exifJSON = Popen(["exiftool", "-j", fn], stdout=PIPE)
    return loads(exifJSON.communicate()[0])[0]