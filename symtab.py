

_scope=[]
current=None

class Errorsemantico(Exception):

    def __init__(self, *args, **kwargs): # real signature unknown
        pass


    @staticmethod # known case of __new__
    def __new__(S, *more):
        pass


class Symbol(): #att : name scope level

    def __init__(self,name,scope,level,type,lineno):
        self.name=name
        self.scope=scope
        self.level=level
        self.type=type
        self.lineno=lineno

    def changetype(self,type):
        self.type=type


def new_scope():# crea una nueva tabla de simbolos || usar cada vez que entra a una funcion
    global current
    current={}

    _scope.append(current)
    return current

def pop_scope(): # cada que se sale de una funcion
    global current
    r=_scope.pop()
    current=_scope[-1]
    return r

def get_symbol(name,level=0,attr=None):
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
    s=Symbol(name=name,scope=current,type=type,lineno=lineno)
    current[name]=s
    return s

def set_symbol(s):
    current[s.name]=s # ingresamos a current[print]=print

def attach_symbol(t,type):
    s=current.get(t.value)
    if not s:
        s=add_symbol(t.value,type,t.lexer.lineno)
    else:
        print("Redefinicion de %s" % t.value)
        raise Errorsemantico
    t.symtab=s


