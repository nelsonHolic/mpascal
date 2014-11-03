

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
    print range(len(_scope)-(level+1),-1,-1)
    for i in range(len(_scope)-(level+1),-1,-1):
        s=_scope[i]
        try:
            sym=s[name]
            if attr:
                if hasattr(sym,attr):
                    return sym
                else :
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


