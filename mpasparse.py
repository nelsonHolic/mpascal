# coding=utf-8
__author__ = 'noescobar,rass,anagui'

import ply.yacc as yacc

from mpaslex import tokens
from mpaslex import lexer



# -------------------------------------------------------------
# Nodos del Arbol de Sintaxis Abstracto (AST)

class AST(object):
    '''
    Clase base. No se usa directamente
    '''
    pass

class Identifier(AST):
    '''
    Un identificador
    '''

    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return "Identifier(%r)" % self.id

class Number(AST):
    '''
    Un Numero
    '''

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "Number(%r)" % self.value

class Binop(AST):
    '''
    Un operador binario (por ejemplo: izq + der)
    '''

    def __init__(self, op, left, right):
        self.left  = left
        self.op    = op
        self.right = right

    def __repr__(self):
        return "Binop(%r,%r,%r)" % (self.op, self.left, self.right)

class Assignment(AST):
    '''
    Asignacion de Variable
    '''

    def __init__(self, location, expr):
        self.location = location
        self.expr = expr

    def __repr__(self):
        return "Assignment(%r,%r)" % (self.location, self.expr)

# -------------------------------------------------------------
# Analizador Sintactico Descentente Recursivo
#
# Debe modificar los metodos para construir el AST

class RecursiveDescentParser(object):
    '''
    Implementacion de un analizador descendente recursivo.
    Cada metodo implementa solo una regla de la gramatica.
    Use el metodo ._accept() para probar y aceptar el token
    actual. Use el metodo ._expect() para coincidir y
    descartar el siguiente token de la entrada (o levantar
    una exception SyntaxError si no coincide).

    El atributo .tok contiene el utimo token aceptado. El
    atributo .nexttok contiene el siguiente token.
    '''

    def assignment(self):
        '''
        assignment : ID = expression ;
        '''
        if self._accept("ID"):
            name = self.tok.value
            self._expect("ASSIGN")
            expr = self.expression()
            self._expect("SEMI")
            return Assignment(name, expr)
        else:
            raise SyntaxError("Se esperaba un identificador")

    def expression(self):
        '''
        expression : term { ('+'|'-') term }       # EBNF
        '''
        # Se necesita complementarlo
        expr = self.term()
        while self._accept("PLUS") or self._accept("MINUS"):
            operator = self.tok.value
            right = self.term()
            expr = Binop(operator, expr, right)
        return expr

    def term(self):
        '''
        term : factor { ('*'|'/') factor}          # EBNF
        '''
        term = self.factor()
        while self._accept("TIMES") or self._accept("DIVIDE"):
            operator = self.tok.value
            right = self.factor()
            term = Binop(operator, term, right)
        return term

    def factor(self):
        '''
        factor : ID
               | NUMBER
               | ( expression )
        '''
        if self._accept("ID"):
            return Identifier(self.tok.value)
        elif self._accept("NUMBER"):
            return Number(self.tok.value)
        elif self._accept("LPAREN"):
            expr = self.expression()
            self._expect("RPAREN")
            return expr
        else:
            raise SyntaxError("Se esperaba ID, NUMBER o LPAREN")

    # ---------------------------------------------------------
    # Funciones utilitarias. Por favor, no las cambie
    def _advance(self):
        'Avanza el lexer en un simbol'
        self.tok, self.nexttok = self.nexttok, lexer.token()

    def _accept(self, toktype):
        'Consume el siguiente token si coincide con el tipo esperado'
        if self.nexttok and self.nexttok.type == toktype:
            self._advance()
            return True
        else:
            return False

    def _expect(self, toktype):
        'Consume o descarta el siguiente token o levanta SytaxError'
        if not self._accept(toktype):
            raise SyntaxError("Se esperaba %s" % toktype)

    def start(self):
        'Punto de entrada al parser'
        self._advance()         # Carga el primer simbolo
        return self.assignment()

    def parse(self, text):
        'Punto de entrada al parser'
        self.tok = None         # Se consume ultimo simbol
        self.nexttok = None   # Siguiente simbol
        lexer.input(text)
        return self.start()


precedence = (
    ('right','IFRule'),
    ('left','semicolonSR'),
)


def p_funcion_args(p):
    '''
    fun : FUN funname '(' parameters ')' locals BEGIN statements END
    '''
    p[0]=p[1:]

def p_funname(p):
    '''
    funname :  ID
    '''
    p[0]=p[1]

def p_funcion(p):
    '''
     fun : FUN funname  '(' ')' locals  BEGIN  statements END
    '''
    p[0]=p[1:]


def p_statements_statement_semicolon(p):
    '''
    statements : statements ';'  statement
    '''
    p[0] = p[1:]

def p_statements_statement(p):
    '''
    statements : statement
    '''
    p[0] = p[1]


def p_statement_WHILE(p):
    '''
    statement : WHILE logica  DO BEGIN statements END
    '''
    p[0] = p[1:]

def p_statement_IF(p):
    '''
    statement : IF logica THEN statements %prec IFRule
    '''
    p[0] = p[1:]

def p_statement_IF_ELSE(p):
    '''
    statement : IF logica THEN statements ELSE statements %prec semicolonSR
    '''
    p[0] = p[1:]

def p_statement_SKIP(p):
    '''
    statement : SKIP
    '''
    p[0] = p[1]


def p_statement_BREAK(p):
    '''
    statement : BREAK
    '''
    p[0] = p[1]

def p_statement_RETURN(p):
    '''
    statement : RETURN expression
    '''
    p[0] = p[2]


def p_statement_PRINT(p):
    '''
    statement : PRINT '(' '\"' STRING '\"' ')'
    '''
    p[0] = p[1:]


def p_statement_WRITE(p):
    '''
    statement : WRITE '(' expression ')'
    '''
    p[0] = p[1:]


def p_statement_READ(p):
    '''
    statement : READ '(' ID ')'
    '''
    p[0] = p[1:]


def p_statement_BEGIN(p):
    '''
    statement : BEGIN  statements   END
    '''
    p[0] = p[1:]

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


# def p_statement_defvar(p):
#     '''
#     statement : defvar
#     '''
#     p[0] = p[1]

def p_locals_defvarrecur(p):
    '''
    locals : locals  defvar ';'
    '''
    p[0] = p[1:]

def p_locals_funrecur(p):
    '''
    locals : locals fun ';'
    '''
    p[0] = p[1:]

def p_locals_fun(p):
    '''
    locals : fun ';'
    '''
    p[0] = p[1:]

def p_locals_defvar(p):
    '''
    locals : defvar ';'
    '''
    p[0] = p[1:]

def p_logica_simple(p):
    '''
    logica : logica explog relacion
    '''
    p[0] = p[1:]

def p_logica_complex(p):
    '''
    logica : '(' logica explog ')' relacion
    '''
    p[0] = p[1:]


def p_logica_relacion(p):
    '''
    logica : relacion
    '''
    p[0] = p[1:]

def p_logica_relacion_GREATER(p):
    '''
    relacion : expression GT expression
    '''
    p[0] = p[1] > p[2]


def p_logica_relacion_EQUAL(p):
    '''
    relacion : expression EQ expression
    '''
    p[0] = p[1:]


def p_logica_relacion_LESS(p):
    '''
    relacion : expression LT expression
    '''
    p[0] = p[1:]


def p_logica_relacion_DIFERENT(p):
    '''
    relacion : expression DI expression
    '''
    p[0] = p[1:]


def p_logica_relacion_GEQUAL(p):
    '''
    relacion : expression GE expression
    '''
    p[0] = p[1:]


def p_logica_relacion_LEQUAL(p):
    '''
    relacion : expression LE expression
    '''
    p[0] = p[1:]

def p_valor_ID(p):
    '''
    valor : ID
    '''
    p[0]=p[1]

def p_valor_NINT(p):
    '''
    valor : NINT
    '''
    p[0]=p[1]

def p_valor_NFLOAT(p) :
    '''
    valor : NFLOAT
    '''
    p[0]=p[1]

def p_defvar_id(p):
    '''
    defvar :  ID ':'  tipo
    '''
    p[0]=p[1:]

def p_defvar_vect(p):
    '''
    defvar : ID ':' tipo '[' valor ']'
    '''
    p[0] = p[1:]

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

def p_explog_or(p) :
    '''
    explog : OR
    '''
    p[0]=p[1]

def p_explog_NOT(p) :
    '''
    explog : NOT
    '''
    p[0]=p[1]

def p_explog_AND(p) :
    '''
    explog : AND
    '''
    p[0]=p[1]


def p_parameters_multi(p):
    '''
    parameters : parameters ',' defvar
    '''
    p[0] = p[1:]

def p_parameters_unique(p) :
    '''
    parameters : defvar
    '''
    p[0]=p[1]

def p_assign_val(p):
    '''
    assign :  ID ASIGSIM  valor
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
    expression : expression "+" valor
    '''
    p[0] = p[1] + p[3]


def p_expression_minus(p):
    '''
    expression : expression '-' valor
    '''
    p[0] = p[1] - p[3]



def p_expression_times(p):
    '''
    expression : expression '*' valor
    '''
    p[0] = p[1] * p[3]


def p_expression_divide(p):
    '''
    expression : expression '/' valor
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

def p_args_MULTI(p):
    '''
    args : args ',' valor
    '''
    p[0]=p[1:]

def p_args(p):
    '''
    args : valor
    '''
    p[0]=p[1]

def p_expression_fun(p):
    '''
    expression : funname '(' ')'
    '''
    p[0]=p[1:]

def p_expresion_valor(p):
    '''
     expression : valor
    '''
    p[0]=p[1]

def p_error(p):
    print "Error sintactico en el archivo de entrada!"


parse = yacc.yacc(debug=1)

