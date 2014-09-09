__author__='noescobar,rass,anagui'


import ply.yacc as yacc

def p_funcion(p) :
    '''fun : FUN funname '(' parameters ')' locals BEGIN statements END
    | fun : FUN funname  '('')' locals  BEGIN  statements END'''

def funname(p) :
    'funname :  ID'

def valor(p) :
    '''valor : ID
    |valor :int
    |float
    |number
    |expression
    |number
     '''

def defvar(p) :
    '''defvar :  ID ':'  tipo
    | ID ':' tipo '[' valor ']'
    '''

def assign(p) : 
    '''assign :  ID ASIGSIM  valor
    | assign : ID  ASIGSIM  ID
    | assign : ID '[' valor ']' ASIGSIM valor
    | ID '[' valor ']' ASIGSIM ID '[' valor ']'
    '''
def p_expression(p):
    '''expression : valor "+" expression
    | expression : valor '-' expression
    | expression : valor '*' epression
    | expression : valor '/'
    | expression : INT '(' valor ')'
    | expression : FLOAT '(' valor ')'
    | expression : funname '(' args ')'
    | expression : funname '('')'
    | expression : valor
    '''
    if p[2] == '+' :
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[1] == "INT" :
        p[0] = int(p[3])
    elif p[1] == "FLOAT" :
        p[0] = float(p[3])
    elif 1: p[0] = p[1]


def p_term_times(p):
    'term : term "*" factor'
    p[0] = p[1] * p[3]

def p_term_div(p):
    'term : term "/" factor'
    p[0] = p[1] / p[3]

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]




