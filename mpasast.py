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
To do :
Falta corregir los mensajes de error # varios
Falta chequear que en ambas partes del if no haya un break
Falta corregir los parametros que son vectores // errores raros
Falta corregir todo lo de void (write, fun , etc)
Falta ver eso de fun() :int|float que esta muy raro
Falta ver algunos errores extraños como que diga que una variable es y no es un vector a la vez.
'''

import sys
from symtab import *#current,_scope
from ply.lex import LexToken

class bcolorsAST:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'






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



class Entero(AST):

    type=int
    _fields = ['INT']



class Float(AST):

    type=float
    _fields = ['FLOAT']

class Variable(AST):

    type=None
    _fields = ['ID','valor']
    indice=None

    def Analisissemantico(self,bandera=0):
        n=get_symbol(self.ID.value)
        if not n:
            print("Error en la linea %s : No existe la variable %s "% (str(self.ID.lineno),self.ID.value))
        else:
            if self.valor and not bandera :
                self.valor.Analisissemantico()
                if self.valor.type != type (7):
                    print("Error en la linea %s : La variable %s es un vector y su indice debe ser entero." % (self.ID.lineno,self.ID.value))
            if(not bandera):
                if n.indice and self.valor :
                    self.type=n.type
                elif n.indice and not self.valor:
                    print ("Error en la linea %s : La variable %s es un vector y no se accede a ella como tal." % (self.ID.lineno,self.ID.value))
                elif not n.indice and self.valor:
                    print ("Error en la linea %s : La variable %s no es un vector y se intenta acceder a ella como tal."%(self.ID.lineno,self.ID.value))
            self.type=n.type
            self.indice=self.valor


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
        if self.parameters :
            self.parameters.Analisissemantico()
            m.params= self.parameters.param_decls # para saber el tipo de los parametros
            set_symbol(m)
        elif self.parameters == None :
            m.params=0 # Si no tiene parametros
            set_symbol(m)

        if self.locals:
            self.locals.Analisissemantico() # Analisis a cada local

        self.statements.Analisissemantico() # Analisis a los statements
        m = get_symbol("%return") # Buscamos si tiene return
        if m:
            a = get_symbol(self.ID.value)
            self.type  = m.type
            a.type = self.type
        else : # Si no tiene es void
            a = get_symbol(self.ID.value)
            self.type  = "void"
            a.type = "void"
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



class AssignStatement(AST):
    _fields = ['ID', 'expression']

    def Analisissemantico(self):
        m=get_symbol(self.ID.value)
        if not m:
                    print("Error en la linea %s : No existe la variable %s "% (self.ID.lineno,self.ID.value))
        else:
            if not m.indice :
                self.expression.Analisissemantico()
                if (m.type==self.expression.type):
                    pass
                else:
                    if not(self.expression.type == None):
                        print("Error en la asignacion de %s en la linea %s , %s es de tipo %s y se le esta asignando un valor del tipo %s" % (m.name,str(self.ID.lineno),m.name,m.type,self.expression.type))
            else :
                print("Error en la linea %s : La variable %s es un vector y no se accede a ella como tal" % (self.ID.lineno,self.ID.value)) # tiene indice y no



class AssignVecStatement(AST):# Indices negativos es un error
    _fields = ['ID','posexpreori', 'expression']

    def Analisissemantico(self):
        m=get_symbol(self.ID.value)
        if not m:
                    print("Error en la linea %s : No existe la variable %s en la linea %s"% (self.ID.lineno,self.ID.value))
        else:
            if m.indice :
                self.expression.Analisissemantico()
                self.posexpreori.Analisissemantico()
                if (m.type==self.expression.type ):
                    if (self.posexpreori.type != type(7)) :
                        print("Error en la linea %s : El indice de la variable %s al ser un vector debe ser entero"% (self.ID.lineno,m.name))
                else:
                        print("Error en la asignacion de %s en la linea %s , %s es de tipo %s y se le esta asignando un valor del tipo %s" % (m.name,str(self.ID.lineno),m.name,m.type,self.expression.type))
            else :
                print("Error en la linea %s : La variable %s no es un vector y se accede a ella como tal. " % (self.ID.lineno,self.ID.value)) # no tiene indice y si


class printStatement(AST):
    _fields = ['STRING']

class ReadStatement(AST):
    _fields = ['ID']

    def Analisissemantico(self):
        m=get_symbol(self.ID.value)

        if not m:
            print("Error en la linea %s : No existe la variable %s ."% (self.ID.lineno,self.ID.value))


class ReadStatementVect(AST):
    _fields = ['ID','posexpre']

    def Analisissemantico(self):
        m=get_symbol(self.ID.value)

        if not m:
            print("Error en la linea %s : No existe la variable %s ."% (self.ID.lineno,self.ID.value))
        elif self.posexpre :
            if m.indice :
                if type(self.posexpre)!= int:
                    print("Error en la linea %s : El indice de la variable %s no es de tipo entero."% (self.ID.lineno,m.name))
            else :
                print("Error en la linea %s : La variable %s no es un vector y se intenta acceder a ella como tal."% (self.ID.lineno,self.ID.value))
        elif not self.posexpre and m.indice :
            print("Error en la linea %s : La funcion read solo puede leer un dato, no un vector completo."% (self.ID.lineno))



class WriteStatement(AST):
    _fields = ['expression']

    def Analisissemantico(self):
        self.expression.Analisissemantico()


class BeginEndStatement(AST):
    _fields = ['statements']

    def Analisissemantico(self):
        self.statements.Analisissemantico()



class Defvar(AST):
    type = None
    _fields = ['ID', 'tipo', 'valor']

    def Analisissemantico(self):
        attach_symbol(self.ID, eval(self.tipo),self.valor)
        if self.valor:
            if type(eval(self.valor.value)) != type(7):
                print("Error en la linea %s : La asignacion de tamano en un vector debe ser un numero entero." % (self.ID.lineno))
        self.type = eval(self.tipo)



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

class ReturnStatement(AST):
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
            print("Error en la linea %s : Conflicto de tipos con el tipo de dato que retorna la funcion." % (repr(self.token.lineno)))

class Expression(AST):
    _fields = ['op', 'left', 'right']
    type=None

    def Analisissemantico(self):
        self.left.Analisissemantico()
        self.right.Analisissemantico()
        if self.left.type==self.right.type:
            self.type=self.left.type
        else:
            print("Error en la linea %s : La expresion  %s %s %s involucra diferentes tipos de datos."% (self.op.lineno,self.left,self.op.value,self.right))
            

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
        self.right.Analisissemantico()
        self.right.type=eval(self.tipo)
        self.type=self.right.type



class RelationalOp(AST):
    _fields = ['op', 'left', 'right']
    type = None

    def Analisissemantico(self):
        self.left.Analisissemantico()
        self.right.Analisissemantico()
        if(self.left.type!=self.right.type):
            print("Error en la linea %s de tipos en la expresion logica %s %s %s" % (self.op.lineno,self.left,self.op.value,self.right))
        else :
            self.type=type(True)


class logicaOp(AST):
    _fields = ['op', 'left', 'right']
    type=None

    def Analisissemantico(self):
        self.left.Analisissemantico()
        self.right.Analisissemantico()
        self.type=type(True)


class FunCall(AST): # Falta chequear que si es un array el argumento, se mire si tienen el mismo indice, god save us
    type = None
    _fields =['ID', 'args']

    def Analisissemantico(self):
        m=get_symbol(self.ID.value)
        if not m:
            print("Error en la linea %s : La funcion %s no existe"% (self.ID.lineno,self.ID.value))
        elif m.name!="main":
            if m.params or m.params==0 : #what the fuck
                if m.params==0 :
                    if self.args :
                        print("Error en la linea %s : La funcion %s no requiere argumentos." % (self.ID.lineno,self.ID.value))
                    else:
                        self.type = m.type
                else :
                    if self.args :
                        if len(m.params) > len(self.args.argsList):
                                print("Error en la linea %s : Faltan parametros en el llamado a la funcion %s, se esperaban %s parametros."% (self.ID.lineno,self.ID.value,len(m.params)))
                        elif len(m.params) < len(self.args.argsList):
                                print("Error en la linea %s : Sobran parametros en el llamado a la funcion %s, se esperaban %s parametros."% (self.ID.lineno,self.ID.value,len(m.params)))
                        else : # Desde aca muto
                            i = 0
                            for arg in self.args.argsList:

                                if not m.params[i].valor : # Si no es un vector el parametro
                                    arg.Analisissemantico()
                                    if arg.type != m.params[i].type: # si los tipos son diferentes error
                                            print("3Error en la linea %s : Los tipos en el llamado de la funcion  %s no son correctos.En el argumento %s se esperaba un %s y se ingreso un %s. " % (self.ID.lineno,self.ID.value,str(i+1),m.params[i].type,arg.type ))
                                else : # Si es un vector el parametro
                                    if self.args.argsList[i].valor : # si se le engresa una posicion
                                        arg.Analisissemantico()
                                        if arg.type != m.params[i].type:
                                            print("1.Error en la linea %s : Los tipos en el llamado de la funcion  %s no son correctos.En el argumento %s se esperaba un %s y se ingreso un %s. " % (self.ID.lineno,self.ID.value,str(i+1),m.params[i].type,arg.type ))
                                    else:   # si no se le ingresa posicion
                                        arg.Analisissemantico(1)
                                        l=get_symbol(arg.ID.value) # Buscamos el argumento como variable
                                        if l.indice.value != m.params[i].valor.value : # si los indices del parametro y del vector ingresado son diferentes
                                            print ("2.Error en la linea %s : En la funcion %s el argumento %s ( %s ) es un vector de %s y se esperaba un vector de %s " % (self.ID.lineno,self.ID.value,str(i+1),arg.ID.value,l.indice.value,m.params[i].valor.value ))
                                        elif arg.type != m.params[i].type : # si los indices son iguales pero los tipos son diferentes
                                            print("3.Error en la linea %s : Los tipos en el llamado de la funcion  %s no son correctos. En el argumento %s (%s) se esperaba un %s y se ingreso un %s. " % (self.ID.lineno,self.ID.value,str(i+1),arg.ID.value,m.params[i].type,arg.type ))
                            i +=1
                    else :
                        print("Error en la linea %s : Faltan parametros en el llamado a la funcion %s, se esperaban %s parametros."% (self.ID.lineno,self.ID.value,len(m.params)))

                    self.type = m.type
            else :
                print("Error en la linea %s : La variable %s no es una funcion." % (self.ID.lineno, self.ID.value))
        else:
            print("Error en la linea %s : La funcion principal main no se puede llamar dentro de una funcion."% self.ID.lineno)



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

