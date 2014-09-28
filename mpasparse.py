# coding=utf-8

__author__ = 'noescobar,rass,anagui'

import ply.yacc as yacc

from mpaslex import tokens
from mpaslex import lexer


class Node():

    def __init__(self,name ,children = None, leaf = None):
        self.name = name
        if not children:
            self.children = []
        else:
            self.children = children
        self.leaf = leaf

    def append(self, child):
        self.children.append(child)
    def __str__(self):
        return self.name


# olarte or may be Pao
def dump_tree(n, indent = ''):
    #print n
    if not hasattr(n, 'datatype'):
        datatype = ''
    else:
        datatype = n.datatype

    if not n.leaf:
        print ('%s%s  %s' % (indent, n.name, datatype))
    else:
        print ('%s%s (%s)  %s' % (indent, n.name, n.leaf, datatype))

    indent = indent.replace('-', ' ')
    indent = indent.replace('+', ' ')

    for i in range(len(n.children)):
        c = n.children[i]
        if i == len(n.children)-1:
            dump_tree(c, indent + '  +--')
        else:
            dump_tree(c, indent + '  |--')

precedence = (
    ('right','IFRule'),
    ('left','semicolonSR'),
    ('left','SEMICOLON'),
)

def p_program(p) :
    '''
    program : program fun
    '''
    p[1].append(p[2])
    p[0] = p[1]
    #p[0]=p[1:]

def p_program(p) :
    '''
    program : fun
    '''
    p[0] = Node(name = 'funcion',children = [p[1]])
    #p[0]=p[1]

def p_funcion_args(p):
    '''
    fun : FUN funname '(' parameters ')' locals BEGIN statements END
    '''
    p[0] = Node(name = 'funcion',children = [p[4], p[6], p[8]],leaf=p[2])
    #p[0]=p[1:]

def p_funname(p):
    '''
    funname :  ID
    '''
    p[0] = p[1]
    #p[0]=p[1]

def p_funcion(p):
    '''
     fun : FUN funname  '(' ')' locals  BEGIN  statements END
    '''
    p[0] = Node(name = 'funcion',children = [p[5], p[7]],leaf=p[2])
    #p[0]=p[1:]


def p_statements_statement_semicolon(p):
    '''
    statements : statements ';'  statement
    '''
    p[1].append(p[3])
    p[0] = p[1]
    #p[0] = p[1:]

def p_statements_statement(p):
    '''
    statements : statement
    '''
    p[0] = Node(name = 'statements',children = [p[1]])
    #p[0] = p[1]


def p_statement_WHILE(p):
    '''
    statement : WHILE logica  DO statements %prec SEMICOLON
    '''
    p[0] = Node(name = 'While',children = [p[2], p[4]])
    #p[0] = p[1:]

def p_statement_IF(p):
    '''
    statement : IF logica THEN statements %prec IFRule
    '''
    p[0] = Node(name = 'IF',children = [p[2], p[4]])
    #p[0] = p[1:]

def p_statement_IF_ELSE(p):
    '''
    statement : IF logica THEN statements ELSE statements %prec semicolonSR
    '''
    p[0] = Node(name = 'IFELSE',children = [p[2], p[4]])
    #p[0] = p[1:]

def p_statement_SKIP(p):
    '''
    statement : SKIP
    '''
    p[0] = Node(name = 'Statement',leaf= p[1])
    #p[0] = p[1]


def p_statement_BREAK(p):
    '''
    statement : BREAK
    '''
    p[0] = Node(name = 'Statement',leaf= p[1])
    #p[0] = p[1]

def p_statement_RETURN(p):
    '''
    statement : RETURN expression
    '''
    p[0] = Node(name = 'RETURN',children=[p[2]])
    #p[0] = p[2]

def p_statement_PRINT(p):
    '''
    statement : PRINT '(' '\"' STRING '\"' ')'
    '''
    p[0] = Node(name = 'statement',leaf= p[4])
    #p[0] = p[1:]


def p_statement_WRITE(p):
    '''
    statement : WRITE '(' expression ')'
    '''
    p[0] = Node(name = 'statementWRITE',children= p[2])
    #p[0] = p[1:]


def p_statement_READ(p):
    '''
    statement : READ '(' ID ')'
    '''
    p[0] = Node(name = 'statementREAD',leaf= p[3])
    #p[0] = p[1:]


def p_statement_BEGIN(p):
    '''
    statement : BEGIN  statements   END
    '''
    p[0] = Node(name = 'Bloque instrucciones',children= [p[2]])
    #p[0] = p[1:]

def p_statement_expression(p):
    '''
    statement : expression
    '''
    p[0] = p[1]


def p_statement_assign(p):
    '''
    statement : assign
    '''
    p[0] = p[1]



def p_locals_defvarrecur(p):
    '''
    locals : locals  defvar ';'
    '''
    p[0]=Node("varlist",[p[1],p[2]])


def p_locals_funrecur(p):
    '''
    locals : locals fun ';'
    '''
    p[1].append(p[2])
    p[0]=p[1]
    #p[0]=Node("funlist",[p[1],p[2]])
    #p[0] = p[1:]

def p_locals_fun(p):
    '''
    locals : fun ';'
    '''
    p[0] = p[1]
    #p[0] = p[1:]

def p_locals_defvar(p):
    '''
    locals : defvar ';'
    '''
    p[0] = p[1]
    #p[0] = p[1:]

def p_logica_simple(p):
    '''
    logica : logica explog relacion
    '''
    p[0] = Node(name = 'logica',children= [p[1],p[3]],leaf=p[2])
    #p[0] = p[1:]

def p_logica_complex(p):
    '''
    logica : '(' logica ')' explog  relacion
    '''
    p[0] = Node(name = 'logica',children= [p[1],p[5]],leaf=p[2])
    #p[0] = p[1:]


def p_logica_relacion(p):
    '''
    logica : relacion
    '''
    p[0] = p[1]
    #p[0] = p[1:]

def p_logica_relacion_GREATER(p):
    '''
    relacion : expression GT expression
    '''
    p[0] = Node(name = 'comparacion',children= [p[1],p[3]],leaf=p[2])
    #p[0] = p[1:]


def p_logica_relacion_EQUAL(p):
    '''
    relacion : expression EQ expression
    '''
    p[0] = Node(name = 'comparacion',children= [p[1],p[3]],leaf=p[2])
    #p[0] = p[1:]


def p_logica_relacion_LESS(p):
    '''
    relacion : expression LT expression
    '''
    p[0] = Node(name = 'comparacion',children= [p[1],p[3]],leaf=p[2])
    #p[0] = p[1:]


def p_logica_relacion_DIFERENT(p):
    '''
    relacion : expression DI expression
    '''
    p[0] = Node(name = 'comparacion',children= [p[1],p[3]],leaf=p[2])
    #p[0] = p[1:]


def p_logica_relacion_GEQUAL(p):
    '''
    relacion : expression GE expression
    '''
    p[0] = Node(name = 'comparacion',children= [p[1],p[3]],leaf=p[2])
    #p[0] = p[1:]


def p_logica_relacion_LEQUAL(p):
    '''
    relacion : expression LE expression
    '''
    p[0] = Node(name = 'comparacion',children= [p[1],p[3]],leaf=p[2])
    #p[0] = p[1:]

def p_valor_ID(p):
    '''
    valor : ID
    '''
    p[0] = Node(name = 'Variable',leaf= p[1])
    #p[0]=p[1]

def p_valor_NINT(p):
    '''
    valor : NINT
    '''
    p[0] = Node(name = 'Entero',leaf= p[1])
    #p[0]=p[1]

def p_valor_NFLOAT(p) :
    '''
    valor : NFLOAT
    '''
    p[0] = Node(name = 'Flotante',leaf= p[1])
    #p[0]=p[1]

def p_defvar_id(p):
    '''
    defvar :  ID ':'  tipo
    '''
    p[0]= Node(name = 'defvar',children = [ p[3]],leaf=p[1])
    #p[0]= l
    #p[0]=p[1:]

def p_defvar_vect(p):
    '''
    defvar : ID ':' tipo '[' valor ']'
    '''
    p[0] = Node(name = 'defvar',children = [ p[3], p[5]],leaf=p[1])
    #p[0] = p[1:]

def p_tipo_INT(p):
    '''
    tipo : INT
    '''
    p[0] = Node(name = 'tipo',leaf = p[1])
    #p[0] = p[1]

def p_tipo_FLOAT(p):
    '''
    tipo : FLOAT
    '''
    p[0] = Node(name = 'tipo',leaf = p[1])
    #p[0] = p[1]

def p_explog_or(p) :
    '''
    explog : OR
    '''
    p[0] = Node(name = 'explog',leaf = p[1])
    #p[0]=p[1]

def p_explog_NOT(p) :
    '''
    explog : NOT
    '''
    p[0] = Node(name = 'explog',leaf = p[1])
    p[0]=p[1]

def p_explog_AND(p) :
    '''
    explog : AND
    '''
    p[0] = Node(name = 'explog',leaf = p[1])
    p[0]=p[1]


def p_parameters_multi(p):
    '''
    parameters : parameters ',' defvar
    '''
    p[0]=Node("parameterslist",[p[1],p[3]])
    #p[0] = p[1:]

def p_parameters_unique(p) :
    '''
    parameters : defvar
    '''
    p[0] = p[1]
    #p[0] = p[1]

def p_assign_val(p):
    '''
    assign :  ID ASIGSIM  expression
    '''
    p[0] = Node(name = 'assign',children  = [p[3]],leaf=p[1])
    #p[0]=p[1:]


def p_assign_vec(p):
    '''
    assign : ID '[' valor ']' ASIGSIM valor
    '''
    p[0] = Node(name = 'assign',children = [p[3],p[6]],leaf=p[1])
    #p[0]=p[1:]

def p_assign_vtv(p):
    '''
    assign : ID '[' valor ']' ASIGSIM ID '[' valor ']'
    '''
    p[0] = Node(name = 'assign',children = [p[3],p[6],p[8]],leaf=p[1])
    #p[0]=p[1:]

def p_expression_plus(p):
    '''
    expression : expression "+" valor
    '''
    p[0] = Node(name = 'expression',children = [p[1],p[3]],leaf=p[2])
    #p[0] = p[1] + p[3]


def p_expression_minus(p):
    '''
    expression : expression '-' valor
    '''
    p[0] = Node(name = 'expression',children = [p[1],p[3]],leaf=p[2])
    #p[0] = p[1] - p[3]



def p_expression_times(p):
    '''
    expression : expression '*' valor
    '''
    p[0] = Node(name = 'expression',children = [p[1],p[3]],leaf=p[2])
    #p[0] = p[1] * p[3]


def p_expression_divide(p):
    '''
    expression : expression '/' valor
    '''
    p[0] = Node(name = 'expression',children = [p[1],p[3]],leaf=p[2])
    #p[0] = p[1] / p[3]


def p_expression_int(p):
    '''
    expression : INT '(' valor ')'
    '''
    p[0] = Node(name = 'expression',children = [p[3]],leaf= p[1])
    #p[0] = int(p[3])


def p_expression_float(p):
    '''
    expression : FLOAT '(' valor ')'
    '''
    p[0] = Node(name = 'expression',children = [p[3]], leaf = p[1])
    #p[0] = float(p[3])

def p_expression_funargs(p):
    '''
    expression : funname '(' args ')'
    '''
    p[0] = Node(name = 'Funcion',children = [p[3]], leaf=p[1])
    #p[0]=p[1:]

def p_args_MULTI(p):
    '''
    args : args ',' valor
    '''
    p[1].append(p[3])
    p[0] = p[1]
    #p[0]=p[1:]

def p_args(p):
    '''
    args : valor
    '''
    p[0]=p[1]
    #p[0]=p[1]

def p_expression_fun(p):
    '''
    expression : funname '(' ')'
    '''
    p[0] = Node(name = 'expression',leaf= p[1])
    #p[0]=p[1:]

def p_expresion_valor(p):
    '''
     expression : valor
    '''
    p[0]=p[1]
    #p[0]=p[1]

def p_error(p):
    print ("Usted tiene un error de sintaxis en la linea %s." % p.lineno)
    print(" '%s' " %p.value)
    raise SyntaxError

parse = yacc.yacc()

dump_tree(parse.parse("fun lol (d:int,f:float)  x:int; y:int; begin  holamundo(5,3); 35 > 2; y:=5 end ",debug=1))




