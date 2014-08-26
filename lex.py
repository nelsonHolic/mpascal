__author__ = 'noescobar'


# ------------------------------------------------------------
# calclex.py
#
# algo nuevo 
#  tokenizer for a simple expression evaluator for
# numbers and +,-,*,/
# ------------------------------------------------------------

import ply.lex as lex

import sys

sys.path.append("../..")

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
    'IDInvalido',
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
    r'/ \* (.|\n)* \* /'
    pass

def t_COMMENTInvalidoL(t):
    r'/ \* (.|\n)* '
    print ("SE HA DETECTADO UN COMENTARIO SIN TERMINAR EN LA LINEA "+str(t.lineno))

def t_COMMENTInvalidoR(t):
    r'\*/'
    print ("SE HA DETECTADO UN COMENTARIO MAL FORMADO EN LA LINEA "+str(t.lineno))

literals='+-()[]*/:,;'

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
    r"((0 | [1-9][0-9]* | 0+[0-9]*) \.\.+ [0-9]+)|((0 | [1-9][0-9]*) \.+ [0-9]+ \.+[0-9]+)+ | ((0 | [1-9][0-9]* | 0+[0-9]*) (\.[0-9]+)? [eE][eE]+[+-]+[0-9\w]+) |((0 | [1-9][0-9]* | 0+[0-9]*) (\.[0-9]+)?[eE]+[+-][+-]+[0-9\w]+) | (0+[0-9]* \.[0-9]+ ([eE][+-][0-9]+)?) "
    print ("NUMERO FLOTANTE NO VALIDO '"+t.value +"' EN LA LINEA  "+str(t.lineno))

def t_NFLOAT(t):
    r"((0 | [1-9][0-9]*) \.[0-9]+) | ((0 | [1-9][0-9]*) (\.[0-9]+)? [eE]([+-])?[0-9]+)"
    return t

def t_IDInvalido(t):
    r'([\d]+[a-zA-Z_][a-zA-Z_0-9]*) | ([a-zA-Z_0-9]+(&|%|\$|!|\?|\#)+ | (&|%|\$|!|\?|\#)+[a-zA-Z_0-9]+ )+ [a-zA-Z_0-9]*'
    print ("ID NO VALIDO '"+t.value +"' EN LA LINEA  "+str(t.lineno))


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value.upper() in PALABRAS_RESERVADAS:
        t.type=t.value.upper()
    return t

def t_INTInvalido(t):
    r'0+[1-9]+'
    print ("NUMERO ENTERO NO VALIDO '"+t.value +"' EN LA LINEA  "+str(t.lineno))

# A regular expression rule with some action code
def t_NINT(t):
    r'[1-9][0-9]*| 0'
    return t

def t_STRING(t):
    r'\" .* \"'
    pos = 0
    bolean = False
    for i in t.value :
        pos +=1
        if (i == '\\'):
            if(t.value[pos] == 'n' or t.value[pos] == '"' or t.value[pos] == '\\' ):
                pass
            else:
                bolean = True
                a= i+t.value[pos]
                d=a.encode('string_escape').replace('\\\\','\\')
                print ("SE HA DETECTADO UN CARACTER DE ESCAPE ("+d+") DESCONOCIDO EN LA LINEA "+str(t.lineno))
    if(not bolean):
        return t

def t_STRINGInvalida(t):
   r' \" .* | .* \" '
   print ("SE HA DETECTADO UN STRING MAL FORMADO EN LA LINEA "+str(t.lineno)+ " "+t.value)

# A regular expression rule with some action code


# Define a rule so we can track line numbers
def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Manejo de errores
def t_error(t):
	print ("linea '%d': caracter ilegal '%s'" % (t.lexer.lineno, t.value[0]))
	t.lexer.skip(1)


lexer=lex.lex()
if __name__ == '__main__':
     lex.runmain()
