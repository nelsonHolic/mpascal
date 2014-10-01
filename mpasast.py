# mpasast.py
# -*- coding: utf-8 -*-
'''
Objetos Arbol de Sintaxis Abstracto (AST - Abstract Syntax Tree).

Este archivo define las clases para los diferentes tipos de nodos del
árbol de sintaxis abstracto.  Durante el análisis sintático, se debe 
crear estos nodos y conectarlos.  En general, usted tendrá diferentes
nodos AST para cada tipo de regla gramatical.  Algunos ejemplos de
nodos AST pueden ser encontrados al comienzo del archivo.  Usted deberá
añadir más.
'''

# NO MODIFICAR
class AST(object):
    '''
    Clase base para todos los nodos del AST.  Cada nodo se espera 
    definir el atributo _fields el cual enumera los nombres de los
    atributos almacenados.  El método a continuación __init__() toma
    argumentos posicionales y los asigna a los campos apropiados.
    Cualquier argumento adicional especificado como keywords son 
    también asignados.
    '''
    _fields = []
    def __init__(self,*args,**kwargs):
        boolargs = len(args) == len(self._fields)
        boolkwargs = len(kwargs) == len(self._fields)
        assert boolargs or boolkwargs
        if len(args) == len(self._fields):
            for name,value in zip(self._fields,args):
                setattr(self,name,value)
            # Asigna argumentos adicionales (keywords) si se suministran
        elif len(kwargs) == len(self._fields):
            for name,value in kwargs.items():
                setattr(self,name,value)


    def pprint(self,archivo= None):
        salida = ''
        for depth, node in flatten(self):
            if type(archivo) == file:
                salida += "\n%s%s" % (" "*(4*depth),node)
            else:
                print("%s%s" % (" "*(4*depth),node))
        if type(archivo) == file:
            archivo.write(salida)

    def pprint2(self,archivo= None):
            salida = ''
            salida += "\n%s" % (self.representacion(stringBefore= " "))
            if type(archivo) == file:
                archivo.write(salida)
            else:
                print salida

    #este es elmetodo encargado de mostrar como esta contruido el arbol permitiendo crear un string segun como este conformado
    #el el hijo o nodoHijo del arbol
    def representacion(self, stringBefore = None):
        stringReturn = ""
        if stringBefore :
            stringReturn = "\n"+stringBefore+self.__class__.__name__
            for atributo in self._fields:
                nodoHijo = self.__getattribute__(atributo)
                if nodoHijo:
                    if isinstance(nodoHijo,AST):
                        stringReturn += nodoHijo.representacion(stringBefore+(" "*4))
                    elif type(nodoHijo) == list:
                        for hijo in nodoHijo:
                            if hijo:
                                if isinstance(hijo,AST):
                                    stringReturn += hijo.representacion(stringBefore+(" "*4))
                                else:
                                    stringReturn += "\n"+stringBefore+(" "*4)+atributo+" : "+str(nodoHijo)
                    else:
                        stringReturn += "\n"+stringBefore+(" "*4)+atributo+" : "+str(nodoHijo)
        else:
            stringReturn = self.__class__.__name__
        return  stringReturn



    def __repr__(self, stringBefore = None):
        # stringReturn = ""
        # if stringBefore:
        #     stringReturn = stringBefore+self.__class__.__name__+" :"
        #     for atributos in self._fields:
        #         nodoHijo = self.__getattribute__(atributos)
        #         if isinstance(nodoHijo,AST):
        #
        # else:
        return self.__class__.__name__

def validate_fields(**fields):
    def validator(cls):
        old_init = cls.__init__
        def __init__(self, *args, **kwargs):
            old_init(self, *args, **kwargs)
            for field,expected_type in fields.items():
                assert isinstance(getattr(self, field), expected_type)
        cls.__init__ = __init__
        return cls
    return validator

# ----------------------------------------------------------------------
# Nodos AST especificos
#
# Para cada nodo es necesario definir una clase y añadir la especificación
# del apropiado _fields = [] que indique que campos deben ser almacenados.
# A modo de ejemplo, para un operador binario es posible almacenar el
# operador, la expresión izquierda y derecha, como esto:
# 
#    class Binop(AST):
#        _fields = ['op','left','right']
# ----------------------------------------------------------------------

# Unos pocos nodos ejemplos

class Entero(AST):
    '''
    Un valor constante como 2, 2.5, o "dos"
    '''
    _fields = ['INT']

    def __repr__(self, stringBefore = None):
            stringReturn = ''
            if stringBefore:
                stringReturn = stringBefore+self.__class__.__name__
                if self.INT:
                    stringReturn += "\n"+stringBefore+(" "*4)+"Valor   : "+self.INT
            else:
                stringReturn = self.__class__.__name__
            return stringReturn


class Float(AST):
    '''
    Un valor constante como 2, 2.5, o "dos"
    '''
    _fields = ['FLOAT']

class Variable(AST):
    '''
    Un valor constante como 2, 2.5, o "dos"
    '''
    _fields = ['ID','valor']

    def __repr__(self, stringBefore = None):
        stringReturn = ''
        if stringBefore:
            stringReturn= stringBefore+self.__class__.__name__#+" : "+ (self.ID if self.ID else self.valor)
            if self.ID:
                stringReturn += "\n"+stringBefore+(" "*4)+"ID : "+self.ID
            if self.valor:
                if type(self.valor) == str:
                    stringReturn += "\n"+stringBefore+(" "*4)+"valor : "+self.valor
                else:
                    stringReturn += "\n"+stringBefore+(" "*4)+"valor : \n"+self.valor.__repr__(stringBefore = stringBefore+(" "*8))

        else:
            stringReturn =  self.__class__.__name__
        return stringReturn

@validate_fields(funlist=list)
class Program(AST):
    _fields = ['funlist']

    def append(self,fun):
        self.funlist.append(fun)


@validate_fields(statements=list)
class Statements(AST):
    _fields = ['statements']

    def append(self,statement):
        self.statements.append(statement)

class FuncPrototype(AST):
    _fields = ['ID', 'parameters', 'locals','statements']


@validate_fields(param_decls=list)
class Parameters(AST):
    _fields = ['param_decls']

    def append(self,param):
        self.param_decls.append(param)


@validate_fields(localsList=list)
class Locals(AST):
    _fields = ['localsList']

    def append(self,vardec):
        self.localsList.append(vardec)


@validate_fields(argsList=list)
class Args(AST):
    _fields = ['argsList']

    def append(self, arg):
        self.argsList.append(arg)

class ParamDecl(AST):
    _fields = ['ID', 'tipo']

class AssignStatement(AST):
    _fields = ['ID', 'expression']



class AssignVecStatement(AST):
    _fields = ['ID','posexpreori', 'expression']

class exprStatement(AST):
    _fields = ['expression']

class printStatement(AST):
    _fields = ['STRING']

class ReadStatement(AST):
    _fields = ['ID']

class ReadStatementVect(AST):
    _fields = ['ID','posexpre']

class WriteStatement(AST):
    _fields = ['expression']

class BeginEndStatement(AST):
    _fields = ['statements']

class Defvar(AST):
    _fields = ['ID', 'value', 'tipo', 'valor']


class IfStatement(AST):
    _fields = ['condition', 'then_b']

class BreakStatement(AST):
    _fields = ['breaky']

class SkipStatement(AST):
    _fields = ['skippy']

class IfelseStatement(AST):
    _fields = ['condition', 'then_b','else_b']

class WhileStatement(AST):
    _fields = ['logica','statements']

class ReturnStatement(AST):
    _fields = ['expression']

class signexpression(AST):
    _fields = ['op', 'expression']

class Expression(AST):
    _fields = ['op', 'left', 'right']

class RelationalOp(AST):
    _fields = ['op', 'left', 'right']


class logicaOp(AST):
    _fields = ['op', 'left', 'right']


class FunCall(AST):
    _fields = ['ID', 'args']

# class ExprList(AST):
#     _fields = ['expressions']
#
#     def append(self, e):
#         self.expressions.append(e)



# Usted deberá añadir mas nodos aquí.  Algunos nodos sugeridos son
# BinaryOperator, UnaryOperator, ConstDeclaration, VarDeclaration, 
# AssignmentStatement, etc...

# ----------------------------------------------------------------------
#                  NO MODIFIQUE NADA AQUI ABAJO
# ----------------------------------------------------------------------

# Las clase siguientes para visitar y reescribir el AST son tomadas
# desde el módulo ast de python .

# NO MODIFIQUE
class NodeVisitor(object):
    '''
    Clase para visitar nodos del árbol de sintaxis.  Se modeló a partir
    de una clase similar en la librería estándar ast.NodeVisitor.  Para
    cada nodo, el método visit(node) llama un método visit_NodeName(node)
    el cual debe ser implementado en la subclase.  El método genérico
    generic_visit() es llamado para todos los nodos donde no hay coincidencia
    con el método visit_NodeName().
    
    Es es un ejemplo de un visitante que examina operadores binarios:

        class VisitOps(NodeVisitor):
            visit_Binop(self,node):
                print("Operador binario", node.op)
                self.visit(node.left)
                self.visit(node.right)
            visit_Unaryop(self,node):
                print("Operador unario", node.op)
                self.visit(node.expr)

        tree = parse(txt)
        VisitOps().visit(tree)
    '''
    def visit(self,node):
        '''
        Ejecuta un método de la forma visit_NodeName(node) donde
        NodeName es el nombre de la clase de un nodo particular.
        '''
        if node:
            method = 'visit_' + node.__class__.__name__
            visitor = getattr(self, method, self.generic_visit)
            return visitor(node)
        else:
            return None
    
    def generic_visit(self,node):
        '''
        Método ejecutado si no se encuentra médodo aplicable visit_.
        Este examina el nodo para ver si tiene _fields, es una lista,
        o puede ser recorrido completamente.
        '''
        for field in getattr(node,"_fields"):
            value = getattr(node,field,None)
            if isinstance(value, list):
                for item in value:
                    if isinstance(item,AST):
                        self.visit(item)
            elif isinstance(value, AST):
                self.visit(value)

# NO MODIFICAR
class NodeTransformer(NodeVisitor):
    '''
    Clase que permite que los nodos del arbol de sintraxis sean 
    reemplazados/reescritos.  Esto es determinado por el valor retornado
    de varias funciones visit_().  Si el valor retornado es None, un
    nodo es borrado. Si se retorna otro valor, reemplaza el nodo
    original.
    
    El uso principal de esta clase es en el código que deseamos aplicar
    transformaciones al arbol de sintaxis.  Por ejemplo, ciertas optimizaciones
    del compilador o ciertas reescrituras de pasos anteriores a la generación
    de código.
    '''
    def generic_visit(self,node):
        for field in getattr(node,"_fields"):
            value = getattr(node,field,None)
            if isinstance(value,list):
                newvalues = []
                for item in value:
                    if isinstance(item,AST):
                        newnode = self.visit(item)
                        if newnode is not None:
                            newvalues.append(newnode)
                    else:
                        newvalues.append(node)
                value[:] = newvalues
            elif isinstance(value,AST):
                newnode = self.visit(value)
                if newnode is None:
                    delattr(node,field)
                else:
                    setattr(node,field,newnode)
        return node

# NO MODIFICAR
def flatten(top):
    '''
    Aplana el arbol de sintaxis dentro de una lista para efectos
    de depuración y pruebas.  Este retorna una lista de tuplas de
    la forma (depth, node) donde depth es un entero representando
    la profundidad del arból de sintaxis y node es un node AST
    asociado.
    '''
    class Flattener(NodeVisitor):
        def __init__(self):
            self.depth = 0
            self.nodes = []
        def generic_visit(self,node):
            self.nodes.append((self.depth,node))
            self.depth += 1
            NodeVisitor.generic_visit(self,node)
            self.depth -= 1

    d = Flattener()
    d.visit(top)
    return d.nodes
