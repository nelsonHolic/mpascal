__author__ = 'noescobar,rass,anaguirre'

def generate(file,top):
    print >>file, "! Creado por Nelson Escobar Ceballos, Richard Andrey Salazar, Angelica Aguirre"
    print >>file, "! Compiladores I , IS744 (2014-2)"
    print >>file, '    .section ".text"'
    top.codeGenerator(file)