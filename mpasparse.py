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
def p_expression_plus(p):
    '''expression : valor "+" expression

    '''
         p[0] = p[1] + p[3]

def p_expression_minus(p):
    '''
    expression : valor '-' expression
    '''
     p[0] = p[1] - p[3]

def p_expression_times(p):
    '''
    expression : valor '*' expression
    '''
     p[0] = p[1] * p[3]

def p_expression_divide(p):
    '''
    expression : valor '/' expression
    '''
     p[0] = p[1] / p[3]

def p_expression_int(p):
    '''
    expression : INT '(' valor ')'
    '''
     p[0] = int(p[3])

def p_expression_float(p):
    '''
    expression : FLOAT '(' valor ')'
    '''
     p[0] = float(p[3])

    #| expression : funname '(' args ')'
    #| expression : funname '('')'
    #| expression : valor


def p_term_times(p):
    'term : term "*" factor'
    p[0] = p[1] * p[3]

def p_term_div(p):
    'term : term "/" factor'
    p[0] = p[1] / p[3]

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]




