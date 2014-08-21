__author__ = 'noescobar'

# ------------------------------------------------------------
# calclex.py
#
# algo nuevo 
#  tokenizer for a simple expression evaluator for
# numbers and +,-,*,/
# ------------------------------------------------------------


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
    'CARPINCHO',
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
    'GT',
    'GE',
    'LT',
    'LE',
    'EQ',
    'DI',
    'ASIGSIM',
    'DEFSIM',
    'NFLOAT',
    'NINT',
    'COMMENT',

) + PALABRAS_RESERVADAS

# Regular expression rules for simple tokens
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LCORCH  = r'\['
t_RCORCH  = r'\]'
t_GT      = r'\>'
t_GE      = r'\>='
t_LT      = r'\<'
t_LE      = r'\<='
t_EQ      = r'\=='
t_DI      = r'\!='
t_ASIGSIM  = r'\:='
t_DEFSIM  = r'\:'
t_CARPINCHO = r'LOL'


def t_ID(t):
    r' [a-zA-Z_][a-zA-Z_0-9]*'
    if t.value in PALABRAS_RESERVADAS:
        t.type=t.value
    return t


def t_NFLOAT(t):
    r"((0 | [1-9][0-9]*) \.[0-9]+) | ((0 | [1-9][0-9]*) (\.[0-9]+)? [eE][+-][0-9]+)"
    t.value = float(t.value)
    return t


# A regular expression rule with some action code
def t_NINT(t):
    r'^ [1-9][0-9]* [\w]$| ^0[.+]$'
    t.value = int(t.value)
    return t



# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_COMMENT(t):
    r'/ \* .* \* /'
    pass


# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print "NO ES VALIDO '%s'" % t.value[0]
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()
