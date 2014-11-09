# coding=utf-8

__authors__ = 'noescobar,rass,anagui'

import ply.yacc as yacc
from mpaslex import *
from mpasast import *
from symtab import *

globalErrorSintactico = {'error' : False}


precedence = (
    ('right','ELSE'),
    ('left','error'),
    ('left', 'OR','NOT', 'AND'),
    ('left','+','-'),
    ('left','*','/'),
    ('right','IFRule'),
    ('left','SEMICOLON'),
)

def p_program_funciones(p) :
    '''
    program : program fun
    '''
    global globalErrorSintactico
    if not globalErrorSintactico['error']:
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
    p[0] = p.slice[1]

def p_funcion(p):
    '''
     fun : FUN funname  '(' ')' locals  BEGIN  statements END
    '''
    p[0]=Funcion(ID=p[2], parameters=None , locals=p[5],statements=p[7])


def p_funcion_end_Error(p):
    '''
     fun : FUN funname  '(' ')' locals  BEGIN  statements error
    '''
    global globalErrorSintactico
    if not globalErrorLex['error'] and not globalErrorSintactico['error']:
        if(p[8]).type == 'END':
            print(bcolors.FAIL+"\t ';' redundante, antes de "+p[8].value+bcolors.ENDC)
            globalErrorSintactico['error']=True
        else:
            print(bcolors.FAIL+"\tNo se ha encontrado ningun END, antes de "+p[8].value+bcolors.ENDC)
            globalErrorSintactico['error']=True

def p_funcion_end_wlocals_Error(p):
    '''
     fun : FUN funname  '(' ')' BEGIN  statements error
    '''
    global globalErrorSintactico
    if not globalErrorLex['error'] and not globalErrorSintactico['error']:
        if(p[7]).type == 'END':
            print(bcolors.FAIL+"\t ';' redundante, antes de "+p[7].value+bcolors.ENDC)
            globalErrorSintactico['error']=True
        else:
            print(bcolors.FAIL+"\tNo se ha encontrado ningun END, antes de "+p[7].value+bcolors.ENDC)
            globalErrorSintactico['error']=True


def p_funcion_end_args_Error(p):
    '''
     fun : FUN funname  '(' parameters ')' locals  BEGIN  statements error
    '''
    global globalErrorSintactico
    if not globalErrorLex['error'] and not globalErrorSintactico['error']:
        if(p[9]).type == 'END':
            print(bcolors.FAIL+"\t ';' redundante, antes de "+p[9].value+bcolors.ENDC)
            globalErrorSintactico['error']=True
        else:
            print(bcolors.FAIL+"\tNo se ha encontrado ningun END, antes de "+p[9].value+bcolors.ENDC)
            globalErrorSintactico['error']=True
    


def p_funcion_end_args_wlocals_Error(p):
    '''
     fun : FUN funname  '(' parameters ')' BEGIN  statements error
    '''
    global globalErrorSintactico
    if not globalErrorLex['error'] and not globalErrorSintactico['error']:
        if(p[8]).type == 'END':
            print(bcolors.FAIL+"\t ';' redundante, antes de "+p[8].value+bcolors.ENDC)
            globalErrorSintactico['error']=True
        else:
            print(bcolors.FAIL+"\tNo se ha encontrado ningun END, antes de "+p[8].value+bcolors.ENDC)
            globalErrorSintactico['error']=True
    

def p_funcion_args_BEGIN_Error(p):
    '''
    fun : FUN funname '(' parameters ')' locals error statements END
    '''
    global globalErrorSintactico
    if not globalErrorLex['error'] and not globalErrorSintactico['error']:
            print(bcolors.FAIL+"\t No se ha encontrado ningun begin antes de "+p[7].value+bcolors.ENDC)
            globalErrorSintactico['error']=True


def p_statements_statement_semicolon(p):
    '''
    statements : statements ';'  statement
    '''
    global globalErrorSintactico
    if not globalErrorSintactico['error']:
        p[1].append(p[3])
        p[0] = p[1]




def p_statements_statement_semicolon_error(p):
    '''
    statements : statements error  statement
    '''
    global globalErrorSintactico
    if not globalErrorLex['error'] and not globalErrorSintactico['error']:
        print(bcolors.FAIL+"\tNo se ha encontrado ningun ';', antes del "+p[2].value+bcolors.ENDC)
        globalErrorSintactico['error']=True
    

def p_statements_statement(p):
    '''
    statements : statement
    '''
    p[0]=Statements(statements=[p[1]])




def p_statements_statement_empty_error(p):
    '''
    statements : error
    '''
    global globalErrorSintactico
    if not globalErrorLex['error'] and not globalErrorSintactico['error']:
        print(bcolors.FAIL+"\t bloque de instrucciones vacio"+bcolors.ENDC)
        globalErrorSintactico['error']=True
    



def p_statement_WHILE(p):
    '''
    statement : WHILE logica DO statements %prec SEMICOLON
    '''
    p[0]=WhileStatement(logica=p[2],statements=p[4])

def p_statement_WHILE_nologerror(p):
    '''
    statement : WHILE error DO statements %prec SEMICOLON
    '''
    global globalErrorSintactico
    if not globalErrorLex['error'] and not globalErrorSintactico['error']:
        print(bcolors.FAIL+"\tNo se ha encontrado ninguna relacion logica para la sentencia WHILE antes de "+p[2].value+bcolors.ENDC)
        globalErrorSintactico['error']=True


def p_statement_WHILE_DO_Error(p):
    '''
    statement : WHILE logica  error statements %prec SEMICOLON
    '''
    global globalErrorSintactico
    if not globalErrorLex['error'] and not globalErrorSintactico['error']:
        print(bcolors.FAIL+"\tNo se ha encontrado ninguna DO para la sentencia WHILE antes de "+p[3].value+bcolors.ENDC)
        globalErrorSintactico['error']=True


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

def p_statement_IF_nologerror(p):
    '''
    statement : IF error THEN statements %prec IFRule
    '''
    global globalErrorSintactico
    if not globalErrorLex['error'] and not globalErrorSintactico['error']:
        print(bcolors.FAIL+"\tNo se ha encontrado ninguna relacion logica para la sentencia if antes de "+p[2].value+bcolors.ENDC)
        globalErrorSintactico['error']=True

def p_statement_IF_THEN_Error(p):
    '''
    statement : IF logica error statements %prec IFRule
    '''
    global globalErrorSintactico
    if not globalErrorLex['error'] and not globalErrorSintactico['error']:
        print(bcolors.FAIL+"\tNo se ha encontrado ningun THEN para la sentencia IF antes de "+p[3].value+bcolors.ENDC)
        globalErrorSintactico['error']=True

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
    p[0]= ReturnStatement(expression=p[2], token = p.slice[1])

def p_statement_PRINT(p):
    '''
    statement : PRINT '(' STRING ')'
    '''
    p[0] = printStatement(STRING=p[3])

def p_statement_PRINT_RPARENT_Error(p):
    '''
    statement : PRINT '(' STRING error
    '''
    global globalErrorSintactico
    if not globalErrorLex['error'] :
        print(bcolors.FAIL+"\t Parentesis desvalanceado, antes del "+p[4].value+bcolors.ENDC)
        globalErrorSintactico['error']=True
    


def p_statement_PRINT_STRING_ERROR(p):
    '''
    statement : PRINT '(' error ')'
    '''
    global globalErrorSintactico
    if not globalErrorLex['error'] :
        print(bcolors.FAIL+"\t No se ha encontrado ningun string para el print, en su lugar se encontro "+p[3].value+bcolors.ENDC)
        globalErrorSintactico['error']=True
    


def p_statement_WRITE(p):
    '''
    statement : WRITE '(' expression ')'
    '''
    p[0]= WriteStatement(expression=p[3])

def p_statement_WRITE_RPAREN_error(p):
    '''
    statement : WRITE '(' expression error
    '''
    global globalErrorSintactico
    if not globalErrorLex['error'] :
        print(bcolors.FAIL+"\t Parentesis desvalanceado para la instruccion write, antes del "+p[4].value+bcolors.ENDC)
        globalErrorSintactico['error']=True
    


def p_statement_WRITE_expresion_error(p):
    '''
    statement : WRITE '(' error ')'
    '''
    global globalErrorSintactico
    if not globalErrorLex['error'] :
        if p[3].value == ')':
            print(bcolors.FAIL+"\t Write vacio, se necesita una expresion"+bcolors.ENDC)
        else:
            print(bcolors.FAIL+"\t No se encontro ninguna expresion valida para la instruccion write, en su lugar se encontro "+p[3].value+bcolors.ENDC)
        globalErrorSintactico['error']=True
    



def p_statement_READ(p):
    '''
    statement : READ '(' ID ')'
    '''
    p[0] = ReadStatement(ID = p.slice[3])

def p_statement_READ_RPAREN_Error(p):
    '''
    statement : READ '(' ID error
    '''
    global globalErrorSintactico
    if not globalErrorLex['error'] :
        print(bcolors.FAIL+"\t Parentesis desvalanceado para la instruccion read, antes del "+p[4].value+bcolors.ENDC)
        globalErrorSintactico['error']=True
    


def p_statement_READ_LPAREN_Error(p):
    '''
    statement : READ error ID ')'
    '''
    global globalErrorSintactico
    if not globalErrorLex['error'] :
        print(bcolors.FAIL+"\t Parentesis inicial desvalanceado para la instruccion read"+bcolors.ENDC)
        globalErrorSintactico['error']=True
    



def p_statement_READ_Empty_Error(p):
    '''
    statement : READ '(' error ')'
    '''
    global globalErrorSintactico
    if not globalErrorLex['error'] :
        if p[3].value == ')':
            print(bcolors.FAIL+"\t Read vacio, se necesita una direccion"+bcolors.ENDC)
        else:
            print(bcolors.FAIL+"\t No se encontro ninguna direccion para la instruccion read, en su lugar se encontro "+p[3].value+bcolors.ENDC)
        globalErrorSintactico['error']=True
    


def p_statement_READ_vect(p):
    '''
    statement : READ '(' ID '[' expression ']' ')'
    '''
    p[0] = ReadStatementVect(ID = p.slice[3], posexpre = p[5])



def p_statement_READ_VEC_RBRAKECT_Error(p):
    '''
    statement : READ '(' ID error expression ']' ')'
    '''
    global globalErrorSintactico
    if not globalErrorLex['error'] :
        print(bcolors.FAIL+"\t No se encontro ningun '[' para la direccion "+p[3].value+", en la instruccion read, en su lugar se encontro "+p[4].value+bcolors.ENDC)
        globalErrorSintactico['error']=True
    


def p_statement_READ_VEC_ID_Error(p):
    '''
    statement : READ '(' error '[' expression ']' ')'
    '''
    global globalErrorSintactico
    if not globalErrorLex['error'] :
        print(bcolors.FAIL+"\t No se encontro ninguna direccion para la instruccion read, en su lugar se encontro "+p[3].value+bcolors.ENDC)
        globalErrorSintactico['error']=True
    



def p_statement_READ_VEC_EXPR_Error(p):
    '''
    statement : READ '(' ID '[' error ']' ')'
    '''
    global globalErrorSintactico
    if not globalErrorLex['error'] :
        print(bcolors.FAIL+"\t Expresion invalida para la direccion "+p[3]+", en la instruccion read, en su lugar se encontro "+p[5].value+bcolors.ENDC)
        globalErrorSintactico['error']=True
    




def p_statement_READ_VEC_RBRACKET_Error(p):
    '''
    statement : READ '(' ID '[' expression error ')'
    '''
    global globalErrorSintactico
    if not globalErrorLex['error'] :
        print(bcolors.FAIL+"\t No se encontro ningun ']', en la instruccion read, antes de "+p[6].value+bcolors.ENDC)
        globalErrorSintactico['error']=True
    


def p_statement_READ_VEC_PARENT_Error(p):
    '''
    statement : READ '(' ID '[' expression ']' error
    '''
    global globalErrorSintactico
    if not globalErrorLex['error'] :
        print(bcolors.FAIL+"\t parentesis desvalanceado , en la instruccion read, antes de "+p[7].value+bcolors.ENDC)
        globalErrorSintactico['error']=True
    



def p_statement_BEGIN(p):
    '''
    statement : BEGIN  statements   END
    '''
    p[0] = BeginEndStatement(statements = p[2])

def p_statement_end_ERROR(p):
    '''
    statement : BEGIN  statements  error
    '''
    global globalErrorSintactico
    if not globalErrorLex['error'] :
        print(bcolors.FAIL+"\t no se ha encontrado ningun END, antes de "+p[3].value+bcolors.ENDC)
        globalErrorSintactico['error']=True
    

def p_statement_expression_fun(p):
    '''
    statement : funname '(' args ')'
    '''
    p[0] = FunCall(ID = p[1], args = p[3])

def p_statement_expression_funnoargs(p):
    '''
    statement : funname '(' ')'
    '''
    p[0] = FunCall(ID = p[1], args = None)

def p_statement_assign(p):
    '''
    statement : assign
    '''
    p[0] = p[1]

def p_locals_defvarrecur(p):
    '''
    locals : locals  defvar ';'
    '''
    global globalErrorSintactico
    if not globalErrorSintactico['error']:
        p[1].append(p[2])
        p[0]= p[1]


def p_locals_defvarrecur_error(p):
    '''
    locals : locals  defvar error
    '''
    global globalErrorSintactico
    if not globalErrorLex['error'] :
        print(bcolors.FAIL+"\t No se ha encontrado ningun ';', antes del "+p[3].value+bcolors.ENDC)
        globalErrorSintactico['error']=True
    


def p_locals_funrecur(p):
    '''
    locals : locals fun ';'
    '''
    global globalErrorSintactico
    if not globalErrorSintactico['error']:
        p[1].append(p[2])
        p[0]=p[1]


def p_locals_funrecur_error(p):
    '''
    locals : locals fun error
    '''
    global globalErrorSintactico
    if not globalErrorLex['error'] :
        print(bcolors.FAIL+"\t No se a encontrado ningun ';', antes del "+p[3].value+bcolors.ENDC)
        globalErrorSintactico['error']=True
    

def p_locals_fun(p):
    '''
    locals : fun ';'
    '''
    p[0]=Locals(localsList=[p[1]])

def p_locals_fun_eror(p):
    '''
    locals : fun error
    '''
    global globalErrorSintactico
    if not globalErrorLex['error'] :
        print(bcolors.FAIL+"\t No se a encontrado ningun ';', antes del "+p[2].value+bcolors.ENDC)
        globalErrorSintactico['error']=True
    

def p_locals_defvar(p):
    '''
    locals : defvar ';'
    '''
    p[0] = Locals(localsList=[p[1]])

def p_locals_defvar_error(p):
    '''
    locals : defvar error
    '''
    global globalErrorSintactico
    if not globalErrorLex['error'] :
        print(bcolors.FAIL+"\t No se a encontrado ningun ';', antes del "+p[2].value+bcolors.ENDC)
        globalErrorSintactico['error']=True
    

def p_logica_simple(p):
    '''
    logica : logica OR logica
    logica : logica AND logica
    '''
    p[0]=logicaOp(op=p[2],left=p[1],right=p[3])


def p_logica_op_error(p):
    '''
    logica : logica error logica
    '''
    global globalErrorSintactico
    if not globalErrorLex['error'] :
        print(bcolors.FAIL+"\t No se a encontrado ningun conector logico, antes del "+p[2].value+bcolors.ENDC)
        globalErrorSintactico['error']=True
    


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

# def p_logica_complex_error(p):
#     '''
#     logica : error logica ')'
#     '''
#     if not globalErrorLex['error']:
#         print(bcolors.FAIL+"\tParentesis desbalanceado."+p[2]+bcolors.ENDC)
#         b=1

def p_logica_complex_error2(p):
    '''
    logica : '(' logica error
    '''
    if not globalErrorLex['error']:
        print(bcolors.FAIL+"\tParentesis desbalanceado."+bcolors.ENDC)
        globalErrorSintactico['error']=True
    

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
    p[0]=Variable(ID= p.slice[1],valor=None)

def p_valor_ID_vect(p):
    '''
    valor : ID '[' expression ']'
    '''
    p[0]=Variable(ID=p.slice[1],valor=p[3])

def p_valor_ID_vect_Error(p):
    '''
    valor : ID '[' logica ']'
    '''
    if not globalErrorLex['error']:
        print(bcolors.FAIL+"\t valor invalido : operacion logica"+bcolors.ENDC)
        globalErrorSintactico['error']=True

def p_valor_NINT(p):
    '''
    valor : NINT
    '''

    p[0]=Entero(INT=p.slice[1])

def p_valor_NFLOAT(p) :
    '''
    valor : NFLOAT
    '''
    p[0]=Float(FLOAT=p.slice[1])

def p_defvar_id(p):
    '''
    defvar :  ID ':'  tipo
    '''
    p[0]= Defvar(ID = p.slice[1], tipo = p[3], valor=None)

def p_defvar_id_tipo_error(p):
    '''
    defvar :  ID ':'  error
    '''
    if not globalErrorLex['error']:
        print(bcolors.FAIL+"\t tipo invalido : "+p[3].value+bcolors.ENDC)
        globalErrorSintactico['error']=True
    

def p_defvar_vect(p):
    '''
    defvar : ID ':' tipo '[' NINT ']'
    '''
    p[0] = Defvar(ID = p.slice[1], tipo= p[3], valor = p.slice[5])

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
    global globalErrorSintactico
    if not globalErrorSintactico['error']:
        p[1].append(p[3])
        p[0]= p[1]


def p_parameters_multi_error(p):
    '''
    parameters : parameters error defvar
    '''
    global globalErrorSintactico
    if not globalErrorLex['error'] :
        print(bcolors.FAIL+"\t No se a encontrado ninguna ',', antes del "+p[2].value+bcolors.ENDC)
        globalErrorSintactico['error']=True
    

def p_parameters_unique(p) :
    '''
    parameters : defvar
    '''
    p[0] = Parameters(param_decls= [p[1]])


def p_assign_val(p):
    '''
    assign :  ID ASIGSIM expression
    '''
    p[0]=AssignStatement(ID=p.slice[1],expression=p[3])


def p_assign_val_error(p):
    '''
    assign :  ID error expression
    '''
    global globalErrorSintactico
    if not globalErrorLex['error'] :
        print(bcolors.FAIL+"\t No se a encontrado ningun ':=', en su lugar se encontro "+p[2].value+bcolors.ENDC)
        globalErrorSintactico['error']=True
    


def p_assign_vec(p):
    '''
    assign : ID '[' expression ']' ASIGSIM expression
    '''
    p[0] = AssignVecStatement(ID = p.slice[1], posexpreori = p[3], expression = p[6])

def p_assign_vec_RBRAKECT_error(p):
    '''
    assign : ID '[' expression error ASIGSIM expression
    '''
    global globalErrorSintactico
    if not globalErrorLex['error'] :
        print(bcolors.FAIL+"\t No se a encontrado ningun ']', en su lugar se encontro "+p[4].value+bcolors.ENDC)
        globalErrorSintactico['error']=True


def p_assign_vec_expresion_error(p):
    '''
    assign : ID '[' error ']' ASIGSIM expression
    '''
    global globalErrorSintactico
    if not globalErrorLex['error'] :
        print(bcolors.FAIL+"\t Expresion invalidad, en su lugar se encontro "+p[3].value+bcolors.ENDC)
        globalErrorSintactico['error']=True
    


def p_assign_vec_error(p):
    '''
    assign : ID '[' expression ']' error expression
    '''
    global globalErrorSintactico
    if not globalErrorLex['error'] :
        print(bcolors.FAIL+"\t No se a encontrado ningun ':=', en su lugar se encontro "+p[2].value+bcolors.ENDC)
        globalErrorSintactico['error']=True
    


def p_expression_plus(p):
    '''
    expression : expression "+" expression
    '''
    p[0]=Expression(op=p.slice[2],left=p[1],right=p[3])


def p_expression_minus(p):
    '''
    expression : expression '-' expression
    '''
    p[0]=Expression(op=p.slice[2],left=p[1],right=p[3])

def p_expression_times(p):
    '''
    expression : expression '*' expression
    '''
    p[0]=Expression(op=p.slice[2],left=p[1],right=p[3])

def p_expression_times_error(p):
    '''
    expression : expression '*' error expression
    '''
    global globalErrorSintactico
    if not globalErrorLex['error'] :
        print(bcolors.FAIL+"\t valor incorrecto despues de *, en su lugar se encontro "+p[3].value+bcolors.ENDC)
        globalErrorSintactico['error']=True
    


def p_expression_divide(p):
    '''
    expression : expression '/' expression
    '''
    p[0]= Expression(op=p.slice[2],left=p[1],right=p[3])


def p_expression_divide_error(p):
    '''
    expression : expression '/' error expression
    '''
    global globalErrorSintactico
    if not globalErrorLex['error'] :
        print(bcolors.FAIL+"\t valor incorrecto despues de /, en su lugar se encontro "+p[3].value+bcolors.ENDC)
        globalErrorSintactico['error']=True
    




def p_expression_parent(p):
    '''
    expression : '(' expression ')'
    '''
    p[0] = p[2]



def p_expression_negative(p):
    '''
    expression : '-' expression
    '''
    p[0] = UnariExpression(op=p.slice[1],right=p[2])

def p_expression_positive(p):
    '''
    expression : '+' expression
    '''
    p[0] = UnariExpression(op=p.slice[1],right=p[2])

def p_expression_int(p):
    '''
    expression : INT '(' expression ')'
    '''
    p[0]= CastExpression(tipo = p[1], right = p[3])


def p_expression_int_RPAREN_error(p):
    '''
    expression : INT '(' expression  error
    '''
    global globalErrorSintactico
    if not globalErrorLex['error'] :
        print(bcolors.FAIL+"\t Parentesis derecho desvalanceado, antes del "+p[4].value+bcolors.ENDC)
        globalErrorSintactico['error']=True
    



def p_expression_float(p):
    '''
    expression : FLOAT '(' expression ')'
    '''
    p[0]= CastExpression(tipo = p[1], right = p[3])


def p_expression_float_RPAREN_error(p):
    '''
    expression : FLOAT '(' expression error
    '''
    global globalErrorSintactico
    if not globalErrorLex['error'] :
        print(bcolors.FAIL+"\t Parentesis derecho desvalanceado, antes del "+p[4].value+bcolors.ENDC)
        globalErrorSintactico['error']=True
    


def p_expression_funargs(p):
    '''
    expression : funname '(' args ')'
    '''
    p[0] = FunCall(ID = p[1], args = p[3])

def p_expression_funargs_RPAREN(p):
    '''
    expression : funname '(' args error
    '''
    global globalErrorSintactico
    if not globalErrorLex['error'] :
        print(bcolors.FAIL+"\t Parentesis derecho desvalanceado de la funcion "+p[1]+", antes del "+p[4].value+bcolors.ENDC)
        globalErrorSintactico['error']=True
    

def p_expression_fun(p):
    '''
    expression : funname '(' ')'
    '''
    p[0] = FunCall(ID = p[1], args = None)

def p_args_MULTI(p):
    '''
    args : args ',' expression
    '''
    global globalErrorSintactico
    if not globalErrorSintactico['error']:
        p[1].append(p[3])
        p[0] = p[1]

def p_args_MULTI_error(p):
    '''
    args : args error expression
    '''
    global globalErrorSintactico
    if not globalErrorLex['error'] :
        print(bcolors.FAIL+"\t No se a encontrado ningun ',', antes de "+p[2].value+bcolors.ENDC)
        globalErrorSintactico['error']=True
    

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

boolError = {'error' :False}

def p_error(p):
    global globalErrorLex
    global globalErrorSintactico
    global boolError
    if p:
        if (not globalErrorSintactico['error'] and not globalErrorLex['error']):
            print (bcolors.FAIL+"Error de sintaxis en la linea %s  :" % p.lineno+bcolors.ENDC)
    else:
        if (not globalErrorLex['error'] and not globalErrorLex['error']):
            print (bcolors.FAIL+"Error de sintaxis en la linea final:")
            print ('\tNo se ha encontrado ningun end'+bcolors.ENDC)
    boolError['error'] = True

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
    if ast  and ((not globalErrorSintactico['error']) and (not globalErrorLex['error'] and (not boolError['error']))) :
        print('escribiendo la representacion del arbol(esto puede tardar segun la profundidad)...')
        outFile = open('RepresentacionAST.txt','w')
        try:
            ast.pprint2(outFile) # crea el archivo de impresion RepresentacionAST.txt
            print('Hecho!')
            print ('''
                  La representacion de el arbol de sintaxis abstracto de el programa analizado
                  se muestra en un archivo nuevo creado llamado RepresentacionAST.txt
                  ubicado en la carpeta donde se encuentre mpasparse.py
                  ''')
        except KeyboardInterrupt:
            print('escritura del arbol cancelada... saliendo')
        outFile.close()
        x=ast.Analisissemantico()

    else:
        ast = None

