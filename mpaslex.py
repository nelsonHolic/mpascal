__author__ = 'noescobar,rass,anagui'


# ------------------------------------------------------------
# calclex.py
# *? not greedy statement
# algo nuevo 
# tokenizer for a simple expression evaluator for
# numbers and +,-,*,/
# ------------------------------------------------------------

import ply.lex as lex

import sys

sys.path.append("../..")

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

globalErrorLex = {'error' : False}


PALABRAS_RESERVADAS = (
    'INT',
    'FLOAT',
    'PRINT',
    'RETURN',
    'WHILE',
    'THEN',
    'DO',
    'BEGIN',
    'END',
    'SKIP',
    'BREAK',
    'FUN',
    'STRING',
    'ELSE',
    'IF',
    'READ',
    'WRITE',
    'OR',
    'AND',
    'NOT',
)

# List of token names.   This is always required
tokens = (
             'NUMBER',
             'ID',
             'GT',
             'GE',
             'LT',
             'LE',
             'EQ',
             'DI',
             'ASIGSIM',
             'FLOATInvalido',
             'NFLOAT',
             'INTinvalido',
             'NINT',
             'COMMENT',
             'COMMENTInvalidoL',
             'COMMENTInvalidoR',
         ) + PALABRAS_RESERVADAS


def t_COMMENT(t):
    r'/\* (.|\n)*? \*/'
    t.lexer.lineno += t.value.count('\n')


def t_COMMENTInvalidoL(t):
    r'/\* (.|\n)* '
    print (bcolors.FAIL+"Error lexico: \n\tSe ha detectado un comentario sin terminar en la linea " + str(t.lineno)+bcolors.ENDC)
    global globalErrorLex
    globalErrorLex['error'] = True


def t_COMMENTInvalidoR(t):
    r'\*/'
    print (bcolors.FAIL+"Error lexico: \n\tSe ha detectado un comentario mal formado en la linea " + str(t.lineno)+bcolors.ENDC)
    global globalErrorLex
    globalErrorLex['error'] = True


literals = '(+-)[]*/:,;'


def t_GE(t):
    r'>='
    return t


def t_LE(t):
    r'<='
    return t


def t_EQ(t):
    r'=='
    return t


def t_DI(t):
    r'!='
    return t


def t_ASIGSIM(t):
    r':='
    return t


def t_GT(t):
    r'>'
    return t


def t_LT(t):
    r'<'
    return t


def t_FLOATInvalido(t):
    r'( 0+[0-9]+ (\.[0-9]+)+ ([eE][+-]?[0-9]+)? )|[0-9]+ \.[0-9]+ (\.[0-9]+)+| [0-9]+ (\. [0-9]+)? [eE][+-][+-]+ [0-9] + ((\.[0-9]+)+)? '
    global globalErrorLex
    globalErrorLex['error'] = True
    print (bcolors.FAIL+"Error lexico: \n\t "+"Numero flotante no valido '" + t.value+"'"+" en la linea "+str(t.lineno)+bcolors.ENDC)


def t_NFLOAT(t):
    r" ((0 | [1-9][0-9]*)([.][0-9]+)? [eE]([+-])?[0-9]+) |((0 | [1-9][0-9]*) \.[0-9]+)"
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value.upper() in PALABRAS_RESERVADAS:
        t.type = t.value.upper()
    return t


def t_INTInvalido(t):
    r'0+[0-9]+'
    print (bcolors.FAIL+"Error lexico:\n\t"+"Numero entero no valido '" + t.value+"'"+" en la linea "+str(t.lineno)+bcolors.ENDC)
    global globalErrorLex
    globalErrorLex['error'] = True


# A regular expression rule with some action code
def t_NINT(t):
    r'[1-9][0-9]*| 0'
    return t


def t_STRING(t):
    r'"([^\\\n]|(\\[^\n]))*?"'
    pos = 0
    bolean = False
    i = 0
    while (i < len(t.value)):
        if (t.value[i] == '\\'):
            if (t.value[i + 1] == 'n' or t.value[i + 1] == '"' or t.value[i + 1] == '\\' ):
                print
                if (t.value[i] == '\\'):
                    i += 1
            else:
                bolean = True
                if (i + 1) != (len(t.value) - 1):
                    a = t.value[i] + t.value[i + 1]
                    global globalErrorLex
                    globalErrorLex['error'] = True
                    print (bcolors.FAIL+"Error lexico:\n\tse ha detectado un caracter de escape (" + a + ") desconocido en la linea " + str(t.lineno)+bcolors.ENDC)
                else:
                    a = i
                    global globalErrorLex
                    globalErrorLex['error'] = True
                    print (bcolors.FAIL+"Error lexico:\n\tse ha detectado un caracter de escape incompleto en la linea"+ str(t.lineno)+bcolors.ENDC)
        i += 1

    for i in t.value:
        pos += 1

    if (not bolean):
        return t


def t_STRINGInvalida(t):
    r'"(.|\n)*|"'
    print (bcolors.FAIL+ "se ha detectado un string mal formado en la linea " + str(t.lineno) + " "+bcolors.ENDC)
    global globalErrorLex
    globalErrorLex['error'] = True


# Define a rule so we can track line numbers
def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'

# Manejo de errores
def t_error(t):
    print (bcolors.FAIL+"Error lexico:\n\t se a detectado el caracter illegal '%s' en la linea %d" % (t.value[0],t.lexer.lineno)+bcolors.ENDC)
    t.lexer.skip(1)


lexer = lex.lex()

if __name__ == '__main__':
    lex.runmain()
