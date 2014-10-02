# coding=utf-8

__authors__ = 'noescobar,rass,anagui'

import ply.yacc as yacc

from mpaslex import *
import sys
from mpasast import *

print '''
      La representacion de el arbol de sintaxis abstracto de el programa analizado
      se muestra en un archivo nuevo creado llamado RepresentacionAST.txt
      ubicado en la carpeta donde se encuentre mpasparse.py
      '''


precedence = (
    ('right','ELSE'),
    ('left', 'OR','NOT', 'AND'),
    ('left','*','/'),
    ('left','+','-'),
    ('right','IFRule'),
    ('left','SEMICOLON'),
)

def p_program_funciones(p) :
    '''
    program : program fun
    '''
    p[1].append(p[2])
    p[0]=p[1]

def p_program(p) :
    '''
    program : fun
    '''
    p[0]= Program(funlist=[p[1]])

def p_funcion_args(p):
    '''
    fun : FUN funname '(' parameters ')' locals BEGIN statements END
    '''
    p[0]=Funcion(ID=p[2],parameters=p[4], locals=p[6],statements=p[8])

def p_funcion_arg_sinLocals(p):
    '''
    fun : FUN funname '(' parameters ')' BEGIN statements END
    '''
    p[0]=Funcion(ID=p[2],parameters=p[4], locals= None,statements=p[7])

def p_funcion_sin_locals(p):
    '''
    fun : FUN funname '(' ')' BEGIN statements END
    '''
    p[0]=Funcion(ID=p[2],parameters=None, locals= None,statements=p[6])

def p_funname(p):
    '''
    funname :  ID
    '''
    p[0] = p[1]

def p_funcion(p):
    '''
     fun : FUN funname  '(' ')' locals  BEGIN  statements END
    '''
    p[0]=Funcion(ID=p[2],parameters=None, locals=p[5],statements=p[7])

def p_statements_statement_semicolon(p):
    '''
    statements : statements ';'  statement
    '''
    p[1].append(p[3])
    p[0] = p[1]

def p_statements_statement_semicolon_error(p):
    '''
    statements : statements error  statement
    '''
    if not globalErrorLex['error']:
        print(bcolors.FAIL+"\tNo se a encontrado ningun ';', antes del "+p[2].type+"  "+p[2].value+bcolors.ENDC)

def p_statements_statement(p):
    '''
    statements : statement
    '''
    p[0]=Statements(statements=[p[1]])

def p_statement_WHILE(p):
    '''
    statement : WHILE logica  DO statements %prec SEMICOLON
    '''
    p[0]=WhileStatement(logica=p[2],statements=p[4])

def p_statement_IF_ELSE(p):
    '''
    statement : IF logica THEN statements ELSE statements
    '''
    p[0]=IfelseStatement(condition = p[2],then_b=p[4],else_b=p[6])

def p_statement_IF(p):
    '''
    statement : IF logica THEN statements %prec IFRule
    '''
    p[0] = IfStatement(condition = p[2],then_b=p[4])

def p_statement_SKIP(p):
    '''
    statement : SKIP
    '''
    p[0] = SkipStatement(skippy=p[1])

def p_statement_BREAK(p):
    '''
    statement : BREAK
    '''
    p[0]=BreakStatement(breaky=p[1])

def p_statement_RETURN(p):
    '''
    statement : RETURN expression
    '''
    p[0]= ReturnStatement(expression=p[2])

def p_statement_PRINT(p):
    '''
    statement : PRINT '(' STRING ')'
    '''
    p[0] = printStatement(STRING=p[3])

def p_statement_WRITE(p):
    '''
    statement : WRITE '(' expression ')'
    '''
    p[0]= WriteStatement(expression=p[3])

def p_statement_READ(p):
    '''
    statement : READ '(' ID ')'
    '''
    p[0] = ReadStatement(ID = p[3])

def p_statement_READ_vect(p):
    '''
    statement : READ '(' ID '[' expression ']' ')'
    '''
    p[0] = ReadStatementVect(ID = p[3], posexpre = p[5])

def p_statement_BEGIN(p):
    '''
    statement : BEGIN  statements   END
    '''
    p[0] = BeginEndStatement(statements = p[2])

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
    p[1].append(p[2])
    p[0]= p[1]

def p_locals_funrecur(p):
    '''
    locals : locals fun ';'
    '''
    p[1].append(p[2])
    p[0]=p[1]

def p_locals_fun(p):
    '''
    locals : fun ';'
    '''
    p[0]=Locals(localsList=[p[1]])

def p_locals_defvar(p):
    '''
    locals : defvar ';'
    '''
    p[0] = Locals(localsList=[p[1]])

def p_logica_simple(p):
    '''
    logica : logica OR logica
    logica : logica AND logica
    '''
    p[0]=logicaOp(op=p[2],left=p[1],right=p[3])


def p_logica_simple_not(p):
    '''
    logica : NOT logica
    '''
    p[0]=logicaOp(op=p[1],left=None,right=p[2])

def p_logica_complex(p):
    '''
    logica : '(' logica ')'
    '''
    p[0] = p[2]

def p_logica_relacion(p):
    '''
    logica : relacion
    '''
    p[0] = p[1]

def p_logica_relacion_GREATER(p):
    '''
    relacion : expression GT expression
    '''
    p[0] = RelationalOp(left = p[1], op = p[2], right = p[3])

def p_logica_relacion_EQUAL(p):
    '''
    relacion : expression EQ expression
    '''
    p[0] = RelationalOp(left = p[1], op = p[2], right = p[3])

def p_logica_relacion_LESS(p):
    '''
    relacion : expression LT expression
    '''
    p[0] = RelationalOp(left = p[1], op = p[2], right = p[3])

def p_logica_relacion_DIFERENT(p):
    '''
    relacion : expression DI expression
    '''
    p[0] = RelationalOp(left = p[1], op = p[2], right = p[3])

def p_logica_relacion_GEQUAL(p):
    '''
    relacion : expression GE expression
    '''
    p[0] = RelationalOp(left = p[1], op = p[2], right = p[3])

def p_logica_relacion_LEQUAL(p):
    '''
    relacion : expression LE expression
    '''
    p[0] = RelationalOp(left = p[1], op = p[2], right = p[3])

def p_valor_ID(p):
    '''
    valor : ID
    '''
    p[0]=Variable(ID=p[1],valor=None)

def p_valor_ID_vect(p):
    '''
    valor : ID '[' expression ']'
    '''
    p[0]=Variable(ID=p[1],valor=p[3])

def p_valor_NINT(p):
    '''
    valor : NINT
    '''
    p[0]=Entero(INT=p[1])

def p_valor_NFLOAT(p) :
    '''
    valor : NFLOAT
    '''
    p[0]=Float(FLOAT=p[1])

def p_defvar_id(p):
    '''
    defvar :  ID ':'  tipo
    '''
    p[0]= Defvar(ID = p[1], tipo = p[3], value = None, valor=None)

def p_defvar_vect(p):
    '''
    defvar : ID ':' tipo '[' valor ']'
    '''
    p[0] = Defvar(ID = p[1], tipo= p[3], valor = p[5], value = None)

def p_tipo_INT(p):
    '''
    tipo : INT
    '''
    p[0] = p[1]

def p_tipo_FLOAT(p):
    '''
    tipo : FLOAT
    '''
    p[0] = p[1]


def p_parameters_multi(p):
    '''
    parameters : parameters ',' defvar
    '''
    p[1].append(p[3])
    p[0]= p[1]

def p_parameters_unique(p) :
    '''
    parameters : defvar
    '''
    p[0] = Parameters(param_decls=[p[0]])


def p_assign_val(p):
    '''
    assign :  ID ASIGSIM  expression
    '''
    p[0]=AssignStatement(ID=p[1],expression=p[3])

def p_assign_vec(p):
    '''
    assign : ID '[' expression ']' ASIGSIM expression
    '''
    p[0] = AssignVecStatement(ID = p[0], posexpreori = p[3], expression = p[6])

def p_expression_plus(p):
    '''
    expression : expression "+" expression
    '''
    p[0]=Expression(op=p[2],left=p[1],right=p[3])


def p_expression_minus(p):
    '''
    expression : expression '-' expression
    '''
    p[0]=Expression(op=p[2],left=p[1],right=p[3])

def p_expression_times(p):
    '''
    expression : expression '*' expression
    '''
    p[0]=Expression(op=p[2],left=p[1],right=p[3])


def p_expression_divide(p):
    '''
    expression : expression '/' expression
    '''
    p[0]= Expression(op=p[2],left=p[1],right=p[3])


def p_expression_parent(p):
    '''
    expression : '(' expression ')'
    '''
    p[0] = p[2]

def p_expression_negative(p):
    '''
    expression : '-' expression
    '''
    p[0] = Expression(op=p[1],left=None,right=p[2])

def p_expression_positive(p):
    '''
    expression : '+' expression
    '''
    p[0] = Expression(op=p[1],left=None,right=p[2])

def p_expression_int(p):
    '''
    expression : INT '(' expression ')'
    '''
    p[0]=p[3]

def p_expression_float(p):
    '''
    expression : FLOAT '(' expression ')'
    '''
    p[0]=p[3]

def p_expression_funargs(p):
    '''
    expression : funname '(' args ')'
    '''
    p[0] = FunCall(ID = p[1], args = p[3])

def p_expression_fun(p):
    '''
    expression : funname '(' ')'
    '''
    p[0] = FunCall(ID = p[1], args = None)

def p_args_MULTI(p):
    '''
    args : args ',' expression
    '''
    p[1].append(p[3])
    p[0] = p[1]

def p_args(p):
    '''
    args : expression
    '''
    p[0]= Args(argsList = [p[1]])

def p_expresion_valor(p):
    '''
     expression : valor
    '''
    p[0]= p[1]

boolError = False

def p_error(p):
    global globalErrorLex
    if p and not globalErrorLex['error']:
        print (bcolors.FAIL+"Error de sintaxis en la linea %s :" % (p.lineno-1)+bcolors.ENDC)
        #print(bcolors.FAIL+"\tAntes del simbolo '%s' " %p.value+bcolors.ENDC)

parse = yacc.yacc()



if __name__ == '__main__':
    try:
        filename = sys.argv[1]
        f = open(filename)
        data = f.read()
        f.close()
    except IndexError:
        sys.stdout.write("ha habido un error en la lectura del archivo. Leyendo en entrada estandar:\n")
        data = sys.stdin.read()
    ast = parse.parse(data,debug = 0)
    if ast:
        outFile = open('RepresentacionAST.txt','w')
        #dibujito.pprint(outFile)
        ast.pprint2(outFile) # crea el archivo de impresion RepresentacionAST.txt
        outFile.close()

