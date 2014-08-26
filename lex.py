__author__ = 'noescobar'


# ------------------------------------------------------------
# calclex.py
#
# algo nuevo 
#  tokenizer for a simple expression evaluator for
# numbers and +,-,*,/
# ------------------------------------------------------------


import sys
sys.path.append("../..")

import ply.lex as lex


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
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'LCORCH',
    'RCORCH',
    'ID',
    'IDInvalido',
    'GT',
    'GE',
    'LT',
    'LE',
    'EQ',
    'DI',
    'ASIGSIM',
    'DEFSIM',
    'FLOATInvalido',
    'NFLOAT',
    'INTinvalido',
    'NINT',
    'COMMENT',
    'COMMENTInvalidoL',
    'COMMENTInvalidoR',
) + PALABRAS_RESERVADAS


def t_COMMENT(t):
    r'/ \* (.|\n)* \* /'
    pass

def t_COMMENTInvalidoL(t):
    r'/ \* (.|\n)* '
    print ("SE HA DETECTADO UN COMENTARIO SIN TERMINAR EN LA LINEA "+str(t.lineno))

def t_COMMENTInvalidoR(t):
    r'\*/'
    print ("SE HA DETECTADO UN COMENTARIO MAL FORMADO EN LA LINEA "+str(t.lineno))





# Regular expression rules for simple tokens
def t_PLUS(t) :
    r'\+'
    return t

def t_MINUS(t):
    r'-'
    return t

def t_TIMES  (t):
    r'\*'
    return t

def t_DIVIDE(t):
    r'/'
    return t

def t_LPAREN (t):
    r'\('
    return t

def t_RPAREN (t):
    r'\)'
    return t

def t_LCORCH (t):
    r'\['
    return t

def t_RCORCH (t):
    r'\]'
    return t

def t_GE      (t):
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

def t_ASIGSIM  (t):
    r':='
    return t

def t_GT     (t):
    r'>'
    return t


def t_LT(t):
    r'<'
    return t





def t_DEFSIM (t):
    r':'
    return t


def t_FLOATInvalido(t):
    r"((0 | [1-9][0-9]* | 0+[0-9]*) \.\.+ [0-9]+)|((0 | [1-9][0-9]*) \.+ [0-9]+ \.+[0-9]+)+ | ((0 | [1-9][0-9]* | 0+[0-9]*) (\.[0-9]+)? [eE][eE]+[+-]+[0-9\w]+) |((0 | [1-9][0-9]* | 0+[0-9]*) (\.[0-9]+)?[eE]+[+-][+-]+[0-9\w]+) | (0+[0-9]* \.[0-9]+ ([eE][+-][0-9]+)?) "
    print ("NUMERO FLOTANTE NO VALIDO '"+t.value +"' EN LA LINEA  "+str(t.lineno))

def t_NFLOAT(t):
    r"((0 | [1-9][0-9]*) \.[0-9]+) | ((0 | [1-9][0-9]*) (\.[0-9]+)? [eE][+-][0-9]+)"
    t.value = float(t.value)
    return t

def t_IDInvalido(t):
    r'([\d]+[a-zA-Z_][a-zA-Z_0-9]*) | [a-zA-Z_0-9]+(&|%|\$|!|\?|\#)+ [a-zA-Z_0-9]* '
    print ("ID NO VALIDO '"+t.value +"' EN LA LINEA  "+str(t.lineno))


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value in PALABRAS_RESERVADAS:
        t.type=t.value
    return t

def t_INTInvalido(t):
    r'0+[1-9]+'
    print ("NUMERO ENTERO NO VALIDO '"+t.value +"' EN LA LINEA  "+str(t.lineno))

# A regular expression rule with some action code
def t_NINT(t):
    r'[1-9][0-9]*| 0'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'\" (.|\n)* \"'
    pos = 0
    bolean = False
    for i in t.value :
        pos +=1
        if (i == "\\"):
            if(t.value[pos] == 'n' or t.value[pos] == '"' or t.value[pos] == '\\' ):
                pass
            else:
                bolean = True
                print ("SE HA DETECTADO UN CARACTER DE ESCAPE DESCONOCIDO EN LA LINEA "+str(t.lineno))
                break
    if(not bolean):
        return t

def t_STRINGInvalida(t):
   r' \" .* | .* \" ' # falta agregar lo de solo \n \" \\
   print ("SE HA DETECTADO UN STRING MAL FORMADO EN LA LINEA "+str(t.lineno)+ " "+t.value)

# A regular expression rule with some action code


# Define a rule so we can track line numbers
def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)




# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print "NO ES VALIDO '%s'" % t.value[0]
    t.lexer.skip(1)

# Build the lexer
lex.lex()

if __name__ == '__main__':
	lex.runmain()