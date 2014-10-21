args ="""-c -g3 -fPIC -O3 -D__ix86__ -D_ix86_ -D_MAC_OS_ -DMACOSX -D_REENTRANT -D_EMBED_ -DSOFTWARE -DTRACK_L2C"""

args+="-I./src"
args+="-I./pysys"
args+="-I/opt/local/include"

filename = "./src/rtklib.h"

from pyclang.json_to_ctypes import JSONToPyCTypesTLM
from pprint import pprint
import sys
#filename = sys.argv[1]

processor = JSONToPyCTypesTLM()
processor.lib_file = "rtklib.dylib"
processor.lib_name = 'rtklib'

processor.load(filename,args.split())


a = open('rtklib.py','w')

a.write( processor.GetTxt())

a.close()


