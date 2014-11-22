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
falta agregar error despues del error de asignacion a un array
Falta corregir todo lo de void (fun , etc) <------ NPI
if a > 1 then return bogus_nested(a) * bogus_fact(a - 1); /* okay: float * float */ else if bar(n) > float(0) then <---- funciones que se llaman sin saber su return
Falta revisar lo de los indices negativos.
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

    def codeGenerator(self,file, indent = 0):
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
# ----------------------------------------------------------------------



class Entero(AST):

    type=int
    _fields = ['INT']

    def __repr__(self):
        return self.INT.value

    def evalExpression(self, file, indent=0, pila=[]):
        cadena = "\t"*indent
        print >> file, "\n%s! push %s" % (cadena, self.INT.value)
        pila.append(self.INT.value)




class Float(AST):

    type=float
    _fields = ['FLOAT']

    def __repr__(self):
        return self.FLOAT.value

    def evalExpression(self, file, indent=0, pila=[]):
        cadena = "\t"*indent
        print >> file, "\n%s! push %s" % (cadena, self.FLOAT.value)
        pila.append(self.FLOAT.value)


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
                if self.valor.type != int:
                    if n.indice:
                        print("Error en la linea %s : La variable %s es un vector y su indice debe ser entero." % (self.ID.lineno,self.ID.value))
                    else:
                        print("Error en la linea %s : El indice de los vectores debe de ser entero." % (self.ID.lineno))
            if(not bandera):
                if n.indice and self.valor :
                    self.type=n.type
                elif n.indice and not self.valor:
                    print ("Error en la linea %s : La variable %s es un vector y no se accede a ella como tal." % (self.ID.lineno,self.ID.value))
                elif not n.indice and self.valor:
                    print ("Error en la linea %s : La variable %s no es un vector y se intenta acceder a ella como tal."%(self.ID.lineno,self.ID.value))
            self.type=n.type
            self.indice=self.valor

    def evalExpression(self, file, indent=0, pila=[]):
        cadena = "\t"*indent
        if self.valor:
            self.valor.evalExpression(file, indent, pila)
            print >> file, "\n%s! index := pop" % cadena
            print >> file, "\n%s! push %s[index]" % (cadena, self.ID.value)
        else:
            print >> file, "\n%s! push %s" % (cadena, self.ID.value)


    def __repr__(self):
        if self.valor:
            return self.ID.value+"["+self.valor+"]"
        else:
            return self.ID.value


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
            print("ERROR : funcion main no definida.")

    def codeGenerator(self,file,indent = 0):
        cadena = "\t"*indent
        print >>file, "\n%s!program (start) ---------------" % cadena
        for func in self.funlist:
            func.codeGenerator(file, indent + 1)
        print >>file, "%s!program (end) ----------------" %cadena



@validate_fields(statements=list)
class Statements(AST):
    _fields = ['statements']

    def append(self,statement):
        self.statements.append(statement)

    def Analisissemantico(self):
        for statement in self.statements:
            statement.Analisissemantico()

    def codeGenerator(self,file,indent = 0):
        for statement in self.statements:
            statement.codeGenerator(file, indent)

    def __iter__(self):
        return self.statements.__iter__()

class Funcion(AST): # <---------------------- falta saber el tipo antes de tenerla toda

    type = None
    _fields = ['ID', 'parameters', 'locals','statements']

    def Analisissemantico(self):
        global current
        global _scope
        attach_symbol(self.ID,int)
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

    def codeGenerator(self,file,indent = 0):
        cadena = "\t"*indent
        print >>file, "\n%s! function : %s (start) Hola soy una funcion" % (cadena, self.ID.value)
        for statement in self.statements:
            statement.codeGenerator(file, indent + 1)
        print >>file, "%s! function : %s (end) Chao soy una funcion\n" % (cadena, self.ID.value)


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
                    self.expression.Analisissemantico()
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

    def codeGenerator(self,file,indent = 0):
        cadena = "\t"*indent
        print >>file, "\n%s! Assign(start)" % cadena
        self.expression.evalExpression(file, indent+1, [])
        print >> file, "\n\t%s! %s := pop" % (cadena, self.ID.value)
        print >>file, "%s! Assing (end)\n" % cadena



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

    def codeGenerator(self,file,indent = 0):
            cadena = "\t"*indent
            print >>file, "\n%s! AssignVec (start)" % cadena
            self.posexpreori.evalExpression(file, indent+1, [])
            print >> file, "\n\t%s! index := pop" % cadena
            self.expression.evalExpression(file, indent+1, [])
            print >> file, "\n\t%s! %s[index] := pop" % (cadena, self.ID.value)
            print >> file, "%s! AssingVec (end)\n" % cadena

class printStatement(AST):
    _fields = ['STRING']

    def codeGenerator(self,file,indent = 0):
            cadena = "\t"*indent
            print >>file, "\n%s! Print (start)" % cadena
            print >>file, "%s! Print (end)\n" % cadena

class ReadStatement(AST):
    _fields = ['ID']

    def codeGenerator(self,file,indent = 0):
            cadena = "\t"*indent
            print >>file, "\n%s! Read(start)" % cadena
            print >>file, "%s! Read (end)\n" % cadena


    def Analisissemantico(self):
        m=get_symbol(self.ID.value)

        if not m:
            print("Error en la linea %s : No existe la variable %s ."% (self.ID.lineno,self.ID.value))
        elif m.indice:
            print("Error en la linea %s : La variable %s es un vector y la funcion read no puede recibir un vector como parametro, solamente una posicion."% (self.ID.lineno,self.ID.value))


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

    def codeGenerator(self,file,indent = 0):
            cadena = "\t"*indent
            print >>file, "\n%s! ReadVec(start)" % cadena
            print >>file, "%s! ReadVec(end)\n" % cadena

class WriteStatement(AST):
    _fields = ['expression','token']

    def Analisissemantico(self):
        self.expression.Analisissemantico()
        if self.expression.type != int and self.expression.type != float:
            print("Error en la linea %s : write solo acepta tipo INT o FLOAT"%(self.token.lineno))


    def codeGenerator(self,file,indent = 0):
            cadena = "\t"*indent
            print >>file, "\n%s! write (start)" % cadena
            self.expression.evalExpression(file,indent+1)
            print >>file, "\n\t%s! write := pop\n" % cadena
            print >>file, "\n%s! write (end)\n" % cadena



class BeginEndStatement(AST):
    _fields = ['statements']

    def Analisissemantico(self):
        self.statements.Analisissemantico()

    def codeGenerator(self,file,indent = 0):
        self.statements.codeGenerator(file, indent)



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

    def codeGenerator(self,file,indent = 0):
        cadena = "\t"*indent
        print >>file, "\n%s! if (start)" % cadena
        self.condition.evalExpression(file, indent+1, [])
        print >>file, "\n\t%s! if false: goto next\n" % cadena
        print >>file, "\n\t%s! then (start)" % cadena
        self.then_b.codeGenerator(file, indent+2)
        print >>file, "\t%s! then (end)\n" % cadena
        print >>file, "%s! if (end) \n" % cadena
        print >>file, "%s! next:\n" % cadena

class BreakStatement(AST):
    _fields = ['breaky']

    def codeGenerator(self,file, indent = 0):
        cadena = "\t"*indent
        print >>file, "\n%s! break (start)\n" % cadena
        print >>file, "%s! break (end) \n" % cadena

class SkipStatement(AST):
    _fields = ['skippy']

    def codeGenerator(self,file, indent = 0):
        cadena = "\t"*indent
        print >>file, "\n%s! skip (start)\n" % cadena
        print >>file, "%s! skip (end) \n" % cadena

class IfelseStatement(AST):
    _fields = ['condition', 'then_b','else_b']

    def Analisissemantico(self):
        self.condition.Analisissemantico()
        self.then_b.Analisissemantico()
        self.else_b.Analisissemantico()

    def codeGenerator(self,file, indent = 0):
        cadena = "\t"*indent
        print >>file, "\n%s! if (start)" % cadena
        self.condition.evalExpression(file, indent+1, [])
        print >>file, "\n\t%s! if false: goto else\n" % cadena
        print >>file, "\n\t%s! then (start)" % cadena
        self.then_b.codeGenerator(file,indent+2)
        print >>file, "\n\t%s! goto next \n" % cadena
        print >>file, "\n\t%s! then (end)\n" % cadena
        print >>file, "\n\t%s! else:" % cadena
        print >>file, "\n\t%s! else (start)" % cadena
        self.else_b.codeGenerator(file,indent+2)
        print >>file, "\n\t%s! else (end)\n" % cadena
        print >>file, "\n%s! if (end)" % cadena
        print >>file, "\n%s! next: \n" % cadena

class WhileStatement(AST):
    _fields = ['logica','statements']

    def Analisissemantico(self):
        self.logica.Analisissemantico()
        self.statements.Analisissemantico()

    def codeGenerator(self,file, indent = 0):
        cadena = "\t"*indent
        print >>file, "\n%s! while (start)" % cadena
        print >>file, "\n\t%s! test:" % cadena
        self.logica.evalExpression(file, indent+1, [])
        print >>file, "\n\t%s! relop := pop" % cadena
        print >>file, "\n\t%s! if not relop: goto done" % cadena
        for statement in self.statements:
            statement.codeGenerator(file, indent +1)
        print >> file, "\n\t%s! goto test" % cadena
        print >> file, "\n\t%s! done:" % cadena
        print >>file, "%s! while (end)\n" % cadena

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


    def evalExpression(self, file, indent = 0, pila = []):
        cadena = "\t"*indent
        self.left.evalExpression(file, indent, pila)
        self.right.evalExpression(file, indent, pila)
        if self.op.value == "+":
            print >> file, "\n%s!    add" % cadena
        if self.op.value == "-":
            print >> file, "\n%s!    sub" % cadena
        if self.op.value == "/":
            print >> file, "\n%s!    div" % cadena
        if self.op.value == "*":
            print >> file, "\n%s!    multiply" % cadena


    def __repr__(self):
        return str(self.left)+str(self.op.value)+str(self.right)


class UnariExpression(AST):
    _fields = ['op','right']
    type=None

    def Analisissemantico(self):
        self.right.Analisissemantico()
        self.type=self.right.type

    def evalExpression(self, file, indent=0, pila=[]):
        cadena = "t"*indent
        self.right.evalExpression(file, indent, pila)
        valor = pila.pop()
        pila.append(self.op.value+valor)

    def __repr__(self):
            return str(self.op.value)+str(self.right)

class CastExpression(AST):
    _fields = ['tipo','right']
    type=None

    def Analisissemantico(self):
        self.right.Analisissemantico()
        if self.right.type != type(0) and self.right.type != float:
            print("Error en la linea  : No se puede castear a %s algo que no sea tipo int o float." %(self.tipo))
        else :
            self.type=eval(self.tipo)

    def evalExpression(self, file, indent=0, pila=[]):
        pass


    def __repr__(self):
            return str(self.tipo)+"("+str(self.right)+")"



class RelationalOp(AST):
    _fields = ['op', 'left', 'right']
    type = None

    def Analisissemantico(self):
        self.left.Analisissemantico()
        self.right.Analisissemantico()
        if(self.left.type!=self.right.type):
            print("Error en la linea %s : de tipos en la expresion logica %s %s %s involucra diferentes tipos de datos" % (self.op.lineno,self.left,self.op.value,self.right))
        else :
            self.type=type(True)

    def evalExpression(self, file, indent=0, pila=[]):
        cadena = "\t"*indent
        self.left.evalExpression(file, indent, pila)
        self.right.evalExpression(file, indent, pila)
        print >> file, "\n%s!    operator : %s" % (cadena, self.op.value)


    def __repr__(self):
            return str(self.left)+str(self.op.value)+str(self.right)


class logicaOp(AST):
    _fields = ['op', 'left', 'right']
    type=None

    def Analisissemantico(self):
        if self.left:
            self.left.Analisissemantico()
        self.right.Analisissemantico()
        self.type=type(True)


    def evalExpression(self, file, indent=0, pila=[]):
        cadena = "\t"*indent
        if self.left:
            self.left.evalExpression(file, indent, pila)
        self.right.evalExpression(file, indent, pila)
        print >> file, "\n%s!    operator : %s" % (cadena, self.op.value)

    def __repr__(self):
            return str(self.left)+str(self.op.value)+str(self.right)




class FunCall(AST): # Falta chequear que si es un array el argumento, se mire si tienen el mismo indice, god save us
    type = None
    _fields =['ID', 'args']

    def Analisissemantico(self):
        m=get_symbol(self.ID.value)
        if not m:
            print("Error en la linea %s : La funcion %s no existe"% (self.ID.lineno,self.ID.value))
        elif m.name!="main":
            if m.params or m.params==0:
                if m.params==0 :
                    if self.args:
                        print("Error en la linea %s : La funcion %s no requiere argumentos." % (self.ID.lineno,self.ID.value))
                    else:
                        self.type = m.type
                else :
                    if self.args:
                        if len(m.params) > len(self.args.argsList):
                                print("Error en la linea %s : Faltan parametros en el llamado a la funcion %s, se esperaban %s parametros."% (self.ID.lineno,self.ID.value,len(m.params)))
                        elif len(m.params) < len(self.args.argsList):
                                print("Error en la linea %s : Sobran parametros en el llamado a la funcion %s, se esperaban %s parametros."% (self.ID.lineno,self.ID.value,len(m.params)))
                        else : # Desde aca muto el numero de parametros es igual
                            i = 0
                            for arg in self.args.argsList:

                                if not m.params[i].valor: # Si no es un vector el parametro
                                    arg.Analisissemantico()
                                    if arg.type != m.params[i].type: # si los tipos son diferentes error
                                            print("Error en la linea %s : Los tipos en el llamado de la funcion  %s no son correctos.En el argumento %s se esperaba un %s y se ingreso un %s. " % (self.ID.lineno,self.ID.value,str(i+1),m.params[i].type,arg.type ))

                                elif m.params[i].valor and arg.valor:
                                    arg.Analisissemantico()
                                    print("Error en la linea %s : En la funcion %s en el argumento %s se espera un vector y se le ingreso un valor" % (self.ID.lineno,str(i+1),arg.ID.value))
                                else : # Si es un vector el parametro
                                    if arg.valor: # si se le engresa una posicion
                                        arg.Analisissemantico()
                                        if arg.type != m.params[i].type:
                                            print("Error en la linea %s : Los tipos en el llamado de la funcion  %s no son correctos.En el argumento %s se esperaba un %s y se ingreso un %s. " % (self.ID.lineno,self.ID.value,str(i+1),m.params[i].type,arg.type ))
                                    else:   # si no se le ingresa posicion
                                        arg.Analisissemantico(1)
                                        l=get_symbol(arg.ID.value) # Buscamos el argumento como variable
                                        if l:
                                            if l.indice:
                                                if l.indice.value != m.params[i].valor.value : # si los indices del parametro y del vector ingresado son diferentes
                                                    print ("Error en la linea %s : En la funcion %s el argumento %s ( %s ) es un vector de %s y se esperaba un vector de %s " % (self.ID.lineno,self.ID.value,str(i+1),arg.ID.value,l.indice.value,m.params[i].valor.value ))
                                                elif arg.type != m.params[i].type : # si los indices son iguales pero los tipos son diferentes
                                                    print("Error en la linea %s : Los tipos en el llamado de la funcion  %s no son correctos. En el argumento %s (%s) se esperaba un %s y se ingreso un %s. " % (self.ID.lineno,self.ID.value,str(i+1),arg.ID.value,m.params[i].type,arg.type ))
                                            else:
                                                    print("error en la linea %s: la variable %s no es un")
                                i +=1
                    else :
                        print("Error en la linea %s : Faltan parametros en el llamado a la funcion %s, se esperaban %s parametros."% (self.ID.lineno,self.ID.value,len(m.params)))

                    self.type = m.type
            else :
                print("Error en la linea %s : La variable %s no es una funcion." % (self.ID.lineno, self.ID.value))
        else:
            print("Error en la linea %s : La funcion principal main no se puede llamar dentro de una funcion."% self.ID.lineno)


    def evalExpression(self, file, indent=0, pila=[]): # todo: tener en cuenta la revision de los parametros
        cadena = "\t"*indent
        i=1

        if self.args :
            for arg in self.args.argsList:
                arg.evalExpression(file,indent+1,pila)
                print >>file,"\n%s arg %s := pop" % (cadena,i)
                i+=1
        print >> file, "\n%s! push %s(" % (cadena,self.ID.value),
        for z in range(len(self.args.argsList)):
            print >> file, "arg %s ," % (z+1),
        print >> file, ")"

    def codeGenerator(self, file, indent=0, pila=[]): # todo: tener en cuenta la revision de los parametros
        cadena = "\t"*indent
        i=1

        if self.args :
            for arg in self.args.argsList:
                arg.evalExpression(file,indent+1,pila)
                print >>file,"\n%s arg %s := pop" % (cadena,i)
                i+=1
        print >> file, "\n%s! push %s(" % (cadena,self.ID.value),
        for z in range(len(self.args.argsList)):
            print >> file, "arg %s ," % (z+1),
        print >> file, ")"


    def __repr__(self):
            return str(self.ID.value)+"("+str(self.args.argsList)+")"