__author__ = 'noescobar,rass,anaguirre'


import sys
import os.path

filename = sys.argv[1]
outfile = os.path.splitext(filename)[0] + ".s"


import mpasparse

top = mpasparse.compilar()

if top:
    import mpasgen
    outf = open(outfile,"w")
    mpasgen.generate(outf,top)
    outf.close()

