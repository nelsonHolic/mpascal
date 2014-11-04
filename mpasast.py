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

'''
En el codigo estan los comentarios de donde va que cosa.
To do :
Falta corregir los mensajes de error , practicamente TODOS sobre todo el lineno.
Falta chequear que no se redefina una variable/parametro en una funcion de locals # pregunta a eingel.
Falta chequeo de que es un vector por lo que se debe acceder a el en manera de vector o visceversa.
Falta propagar el resultado de las expresiones aritmeticas para que sea mas sencillo hacer algunas cosas en esta entrega y en posteriores.
'''

import sys
from ply.lex import LexToken

class bcolorsAST:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'




_scope=[]
current=None

class Errorsemantico(Exception):

    def __init__(self, valor,lineno): # real signature unknown
        self.valor=valor
        self.lineno = lineno

    def __str__(self):
        lineno = ""
        if(self.lineno):
            lineno = self.lineno
        return repr(self.valor)+repr(lineno)



class Symbol(): #att : name scope level
    paramnum=None
    def __init__(self,name,scope,type,lineno):
        self.name=name
        self.scope=scope
        self.type=type
        self.lineno=lineno

    def changetype(self,type):
        self.type=type


def new_scope():# crea una nueva tabla de simbolos || usar cada vez que entra a una funcion
    global current
    global _scope
    current={}
    #print _scope
    _scope.append(current)
    return current

def pop_scope(): # cada que se sale de una funcion
    global current
    global _scope
    r=_scope.pop()
    current=_scope[-1]
    return r

def get_symbol(name,level=0,attr=None):
    global _scope
    for i in range(len(_scope)-(level+1),-1,-1):
        s=_scope[i]
        try:
            sym=s[name]
            # if attr:
            #     if hasattr(sym,attr):
            #         return sym
            #     else :
            return sym
        except KeyError :
            pass
    return None

def add_symbol(name,type,lineno):
    global current
    s=Symbol(name=name,scope=current,type=type,lineno=lineno)
    current[name]=s
    #print current
    return s

def set_symbol(s):
    global current
    current[s.name]=s # ingresamos a current[print]=print

def attach_symbol(t,type):
    global current
    s=current.get(t.value)
    if not s:
        s=add_symbol(t.value,type,t.lexer.lineno)
    else:
        print("Redefinicion de %s" % t.value)
    t.symtab=s




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
            salida += "%s" % (self.representacion(stringBefore= ""))
            if type(archivo) == file:
                archivo.write(salida)
            else:
                print salida

    #este es elmetodo encargado de mostrar como esta contruido el arbol permitiendo crear un string segun como este conformado
    #el el hijo o nodoHijo del arbol
    def representacion(self, stringBefore = None):
            stringReturn = ""
            numeroDeHijos = 0
            if stringBefore or type(stringBefore) == str:
                if(stringBefore== ""):
                    stringReturn = stringBefore+self.__class__.__name__
                else:
                    stringReturn = "\n"+stringBefore+self.__class__.__name__
                pos = len(stringReturn.split("\n"))
                stringBefore = (" " *len(stringBefore))
                for atributo in self._fields:
                    nodoHijo = self.__getattribute__(atributo)
                    if nodoHijo:
                        if isinstance(nodoHijo,AST):
                            try:
                                numeroDeHijos += 1
                                stringReturn += nodoHijo.representacion(stringBefore+" "+"+"+("-"*4))
                            except Exception,e:
                                sys.exit(bcolorsAST.WARNING+'arbol muy profundo, no puede escribirse el archivo'+bcolorsAST.ENDC)
                        elif type(nodoHijo) == list:
                            for hijo in nodoHijo:
                                if hijo:
                                    if isinstance(hijo,AST):
                                        try:
                                            numeroDeHijos += 1
                                            stringReturn += hijo.representacion(stringBefore+" "+"+"+("-"*4))
                                        except Exception,e:
                                            sys.exit(bcolorsAST.WARNING+'arbol muy profundo, no puede escribirse el archivo'+bcolorsAST.ENDC)
                                    else:
                                        try:
                                            numeroDeHijos += 1
                                            if  isinstance(hijo,LexToken):
                                                stringReturn += "\n"+stringBefore+" "+"+"+("-"*4)+atributo+" : "+str(nodoHijo.value)
                                            else:
                                                stringReturn += "\n"+stringBefore+" "+"+"+("-"*4)+atributo+" : "+str(nodoHijo)
                                        except Exception,e:
                                            sys.exit(bcolorsAST.WARNING+'arbol muy profundo, no puede escribirse el archivo'+bcolorsAST.ENDC)
                        else:
                            try:
                                if isinstance(nodoHijo,LexToken):
                                    stringReturn += "\n"+stringBefore+" "+"+"+("-"*4)+atributo+" : "+str(nodoHijo.value)
                                else:
                                    stringReturn += "\n"+stringBefore+" "+"+"+("-"*4)+atributo+" : "+str(nodoHijo)
                            except Exception,e:
                                print(e)
                vecStringReturn = stringReturn.split("\n")
                if len(vecStringReturn)/6 >= 1000:
                    pass #print("Profundidad del la rama muy profundo, simplificando el arbol")
                else:
                    try:
                        while pos < len(vecStringReturn) and numeroDeHijos > 0:
                            location = vecStringReturn[pos].find("+")
                            auxcadena = vecStringReturn[pos]
                            if location != len(stringBefore)+1:
                                auxcadena = auxcadena[:(len(stringBefore)+1)]+"|"+auxcadena[(len(stringBefore)):]
                            else:
                                numeroDeHijos -= 1
                            vecStringReturn[pos] = auxcadena
                            pos += 1
                    except Exception,e:
                        sys.exit(bcolorsAST.WARNING+'arbol muy profundo, no puede escribirse el archivo'+bcolorsAST.ENDC)
                stringReturn = "\n".join(vecStringReturn)
            else:
                stringReturn = self.__class__.__name__
            return  stringReturn




    def __repr__(self, stringBefore = None):
        return self.__class__.__name__

    def Analisissemantico(self):
        pass

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
    type=int
    _fields = ['INT']



class Float(AST):
    '''
    Un valor constante como 2, 2.5, o "dos"
    '''
    type=float
    _fields = ['FLOAT']

class Variable(AST):
    '''
    Un valor constante como 2, 2.5, o "dos"
    '''
    type=None
    _fields = ['ID','valor']

    def Analisissemantico(self):
        n=get_symbol(self.ID.value)
        #print self.ID.value
        if not n:
            print("Error no existe la variable %s en la linea %s"% (self.ID.value,str(self.ID.lineno)))
        else:
            self.type=n.type


@validate_fields(funlist=list)
class Program(AST):
    _fields = ['funlist']

    def append(self,fun):
        self.funlist.append(fun)

    def Analisissemantico(self):
        global _scope
        global current
        current=new_scope()
        for func in self.funlist:
            func.Analisissemantico()

        m=get_symbol("main")
        if not m:
            print(" Error : funcion main no definida.")





@validate_fields(statements=list)
class Statements(AST):
    _fields = ['statements']

    def append(self,statement):
        self.statements.append(statement)

    def Analisissemantico(self):
        for statement in self.statements:
            statement.Analisissemantico()

class Funcion(AST): # <----------------------

    type = None
    _fields = ['ID', 'parameters', 'locals','statements']

    def Analisissemantico(self):
        global current
        global _scope
        attach_symbol(self.ID,None)
        m = get_symbol(self.ID.value)
        new_scope()
        if self.parameters:
            self.parameters.Analisissemantico()
            m.params= self.parameters.param_decls
            set_symbol(m)
        if self.locals:
            self.locals.Analisissemantico()
        self.statements.Analisissemantico()
        m = get_symbol("%return")
        if m:
            a = get_symbol(self.ID.value)
            self.type  = m.type
            a.type = self.type
        pop_scope()



@validate_fields(param_decls=list)
class Parameters(AST):
    _fields = ['param_decls']

    def append(self,param):
        self.param_decls.append(param)

    def Analisissemantico(self):
        for parameter in self.param_decls:
            parameter.Analisissemantico()


@validate_fields(localsList=list)
class Locals(AST):
    _fields = ['localsList']

    def append(self,vardec):
        self.localsList.append(vardec)

    def Analisissemantico(self):
        for local in self.localsList :
            local.Analisissemantico()



@validate_fields(argsList=list)
class Args(AST):
    _fields = ['argsList']

    def append(self, arg):
        self.argsList.append(arg)

    #
    # def Analisissemantico(self):
    #
    #     for argumento in self.argsList:
    #         argumento.Analisissemantico



class AssignStatement(AST):
    _fields = ['ID', 'expression']

    def Analisissemantico(self):
        m=get_symbol(self.ID.value)
        if not m:
                    print("Error no existe la variable %s en la linea %s"% (self.ID.value,str(self.ID.lineno)))
        else:
            self.expression.Analisissemantico()
            if (m.type==self.expression.type):
                pass
            else:
                if not(self.expression.type == None):
                    print("Error en la asignacion de %s en la linea %s , %s es de tipo %s y se le esta asignando un valor del tipo %s" % (m.name,str(self.ID.lineno),m.name,m.type,self.expression.type))



class AssignVecStatement(AST):
    _fields = ['ID','posexpreori', 'expression']

    def Analisissemantico(self):
        m=get_symbol(self.ID.value)
        if not m:
                    print("Error no existe la variable %s en la linea %s"% (self.ID.value,str(self.ID.lineno)))
        else:
            self.expression.Analisissemantico()
            self.posexpreori.Analisissemantico()
            if (m.type==self.expression.type):
                if self.posexpreori.type != int:
                    print("Error en el indice de la variable %s en la linea %s los indices deben ser enteros"% (m.name,str(self.ID.lineno)))
            else:
                if not(self.expression.type == None):
                    print("Error en la asignacion de %s en la linea %s , %s es de tipo %s y se le esta asignando un valor del tipo %s" % (m.name,str(self.ID.lineno),m.name,m.type,self.expression.type))


class printStatement(AST):
    _fields = ['STRING']

class ReadStatement(AST):
    _fields = ['ID']

    def Analisissemantico(self):
        m=get_symbol(self.ID.value)
        if not m:
            print("Error no existe la variable %s en la linea %s"% (self.ID.value,str(self.ID.lineno)))


class ReadStatementVect(AST):
    _fields = ['ID','posexpre']

    def Analisissemantico(self):
        m=get_symbol(self.ID.value)

        if not m:
            print("Error no existe la variable %s en la linea %s"% (self.ID.value,str(self.ID.lineno)))
        elif type(self.posexpre)!= int:
            print("Error en el indice de la variable %s en la linea %s"% (m.name,str(m.lineno)))




class WriteStatement(AST):
    _fields = ['expression']


class BeginEndStatement(AST):
    _fields = ['statements']

    def Analisissemantico(self):
        self.statements.Analisissemantico()



class Defvar(AST):
    type = None
    _fields = ['ID', 'tipo', 'valor']

    def Analisissemantico(self): # Tenemos que coger valor y evaluarlo para guardarlo en la tabla de simbolos, asi podemos chequear que una variable es un vector y en otra etapa ver si se sale del rango con una asignacion
        attach_symbol(self.ID, eval(self.tipo))
        if self.valor:
            self.valor.Analisissemantico()
            if self.valor.type != int:
                print("Error de tipo para la asignacion de tamaño en la linea %s" % (self.ID.lineno))
        self.type = eval((self.tipo))



class IfStatement(AST):
    _fields = ['condition', 'then_b']

    def Analisissemantico(self):
        self.condition.Analisissemantico()
        self.then_b.Analisissemantico()

class BreakStatement(AST):
    _fields = ['breaky']

class SkipStatement(AST):
    _fields = ['skippy']

class IfelseStatement(AST):
    _fields = ['condition', 'then_b','else_b']

    def Analisissemantico(self):
        self.condition.Analisissemantico()
        self.then_b.Analisissemantico()
        self.else_b.Analisissemantico()

class WhileStatement(AST):
    _fields = ['logica','statements']

    def Analisissemantico(self):
        self.logica.Analisissemantico()
        self.statements.Analisissemantico()

class ReturnStatement(AST): # Creamos simbolo falso %return para chequeo de tipos de return . Dado que es un ID invalido no tiene problema con sobreescritura
    _fields = ['expression','token']
    type=None

    def Analisissemantico(self):
        nombre  = "%return"
        self.expression.Analisissemantico()
        self.type=self.expression.type
        m= get_symbol(nombre)
        self.token.value = nombre
        if not m:
            attach_symbol(self.token,self.type)
        elif m.type != self.type:
            print("Conflicto de tipos con del return en la linea %s"%(repr(self.token.lineno)))

class Expression(AST):  # seria mejor propagar el resultado de una vez , ADEMAS serviria para dar los valores en el error y no solo que diga entero + float
    _fields = ['op', 'left', 'right']
    type=None

    def Analisissemantico(self):
        self.left.Analisissemantico()
        self.right.Analisissemantico()
        if self.left.type==self.right.type:
            self.type=self.left.type
        else:
            print("Error en la expresion : %s %s %s involucra diferentes tipos de variable."% (self.left,self.op,self.right)) # falta imprimir la linea
            

class UnariExpression(AST):
    _fields = ['op','right']
    type=None

    def Analisissemantico(self):
        self.right.Analisissemantico()
        self.type=self.right.type

class CastExpression(AST):
    _fields = ['tipo','right']
    type=None

    def Analisissemantico(self):
        #m=get_symbol(self.right)
        self.right.Analisissemantico()
        self.right.type=eval(self.tipo)
        self.type=self.right.type


class RelationalOp(AST):
    _fields = ['op', 'left', 'right']

    def Analisissemantico(self):
        self.left.Analisissemantico()
        self.right.Analisissemantico()
        if(self.left.type!=self.right.type):
            print("Error de tipos en la expresion logica %s %s %s en la linea %s" % (self.left,self.op,self.right,str(0))  # falta agregar la linea


class logicaOp(AST):
    _fields = ['op', 'left', 'right']


    def Analisissemantico(self):
        self.left.Analisissemantico()
        self.right.Analisissemantico()


class FunCall(AST): # asd
    type = None
    _fields = ['ID', 'args']

    def Analisissemantico(self):
        m=get_symbol(self.ID.value)
        if not m:
            print("Error no existe la funcion %s en la linea %s"% (self.ID.value,str(self.ID.lineno)))
        elif len(m.params) != len(self.args.argsList):
            print("Faltan parametros en la funcion %s de la linea %s" % (m.name,m.lineno))
        else :
            i = 0
            for arg in self.args.argsList:
                arg.Analisissemantico()
                if arg.type != m.params[i].type:
                    print("Error de tipos en laen el llamado de la funcion  %s %s en la linea %s" % (self.ID.value, arg , self.ID.lineno))
                i +=1
            self.type = m.type



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

