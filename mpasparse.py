# coding=utf-8
__author__ = 'noescobar,rass,anagui'

import ply.yacc as yacc


def p_funcion_args(p):
    '''
    fun : FUN funname '(' parameters ')' locals BEGIN statements END
    '''
    p[0]=p[1:]

def p_funcion(p):
    '''
     fun : FUN funname  '('')' locals  BEGIN  statements END
    '''
    p[0]=p[1:]

def funname(p):
    '''
    funname :  ID
    '''
    p[0]=p[1]

def p_valor_ID(p):
    '''
    valor : ID
    '''
    p[0]=p[1]

def p_valor_int(p):
    '''
    valor : int
    '''
    p[0]=p[1]

def p_valor_float(p) :
    '''
    valor : float
    '''
    p[0]=p[1]

def p_valor_number(p):
    '''
    valor : number
    '''
    p[0]=p[1]

def p_valor_expr(p):
    '''
    valor :expression
    '''
    p[0]=p[1]


def p_defvar_id(p):
    '''defvar :  ID ':'  tipo

    '''
    p[0]=p[1:]

def p_defvar_vect(p):
    '''
    defvar : ID ':' tipo '[' valor ']'
    '''
    p[0] = p[1:]

def p_parameters_multi(p):
    '''
    parameters : defvar ‘,’ parameters
    '''
    p[0] = p[1:]

def p_parameters_unique(p) :
    '''
    parameters: defvar
    '''
    p[0]=p[1]

def p_assign_val(p):
    '''
    assign :  ID ASIGSIM  valor
    '''
    p[0]=p[1:]

def p_assign_var(p):
    '''
    assign : ID  ASIGSIM  ID
    '''
    p[0]=p[1:]

def p_assign_vec(p):
    '''
    assign : ID '[' valor ']' ASIGSIM valor
    '''
    p[0]=p[1:]

def p_assign_vtv(p):
    '''
    assign : ID '[' valor ']' ASIGSIM ID '[' valor ']'
    '''
    p[0]=p[1:]

def p_expression_plus(p):
    '''
    expression : valor "+" expression
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

def p_expression_funargs(p):
    '''
    expression : funname '(' args ')'
    '''
    p[0]=p[1:]

def p_expression_fun(p):
    '''
    expression : funname '('')'
    '''
    p[0]=p[1:]

def  p_expresion_valor(p):
    '''
     expression : valor
    '''
    p[0]=p[1]


parse = yacc.yacc()