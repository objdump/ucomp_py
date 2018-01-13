# -*- coding: utf-8 -*-  

class Number:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)        

    def __eq__(self, other):
        return self.value == other.value        
        
    def eval(self, env):
        return self

        
class Boolean:
    def __init__(self, value):
        self.value = value
               
    def __str__(self):
        if self.value:
            return "true"
        else:
            return "false"

    def __eq__(self, other):
        return self.value == other.value   
            
    def eval(self, env):
        return self  

        
class Variable:
    def __init__(self, name):
        self.name = name
        
    def __str__(self):
        return str(self.name)
        
    def eval(self, env):
        return env.get(self.name)
        
class LessThan:
    def __init__(self, left, right):
        self.left = left
        self.right = right
        
    def __str__(self):
        return "({} < {})".format(self.left, self.right)
        
    def eval(self, env):
        return Boolean(self.left.eval(env).value < self.right.eval(env).value)

        
class Add:
    def __init__(self, left, right):
        self.left = left
        self.right = right
        
    def __str__(self):
        return '('+ str(self.left)+' + '+str(self.right) +')'
  
    def eval(self, env):
        return Number(self.left.eval(env).value + self.right.eval(env).value)

        
class Multiply:
    def __init__(self, left, right):
        self.left = left
        self.right = right
        
    def __str__(self):
        return '('+ str(self.left)+' * '+str(self.right) +')'   

    def eval(self, env):
        return Number(self.left.eval(env).value * self.right.eval(env).value)

        
class Env:
    def __init__(self, dict):
        self.dict = dict
        
    def __str__(self):
        stri = ("Env:")
        for item in self.dict.items():
            stri = stri +' '+str(item[0])+':'+str(item[1])
        return stri
            
    def update(self, name, value):
        self.dict[name] = value
        return self
        
    def newUpdate(self, name, expression):
        newDict = dict(self.dict)
        newDict[name] = expression
        return Env(newDict)
        
    def merge(self, assoc):
        self.dict.update(assoc)
        return self
        
    def get(self, name):
        return self.dict[name]
 

print("----- Test Number -----")
print(Number(23).eval(Env({})))
print("----- Test Variable -----")
print(Variable('x').eval(Env({ 'x': Number(23) })))
print("----- Test LessThan -----")
print(LessThan(Add(Variable('x'), Number(2)),
    Variable('y')).eval(Env({ 'x': Number(2), 'y': Number(5)})))
    
    
class DoNothing:
    def __init__(self):
        pass
        
    def __str__(self):
        return '<< do-nothing >>'
        
    def __eq__(self, other):
        return isinstance(other, DoNothing)
        
    def eval(self, env):
        return env

        
class Assign:
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression
        
    def __str__(self):
        return '<< '+str(self.name)+' = '+str(self.expression) + '>>'
        
    def eval(self, env):
        return env.merge({self.name: self.expression.eval(env)})


print("\n----- Test Assign -----")
print(Assign('x', Add(Variable('x'), Number(1))).eval(
        Env({'x':Number(2)})))       

                  
class If:
    def __init__(self, condition, consequence, alternative):
        self.condition = condition
        self.consequence = consequence
        self.alternative = alternative

    def __str__(self):
        return "<<If {} then {} else {}>>".format(str(self.condition),
                                                   str(self.consequence), str(self.alternative))
                                               
    def eval(self, env):
        if self.condition.eval() == Boolean(True):
            return self.consequence.eval(env)
        else:
            return self.alternative.eval(env)
            
 
class Sequence:
    def __init__(self, first, second):
        self.first = first
        self.second = second
        
    def __str__(self):
        return "<<Sequence: {}, {}>>".format(str(self.first), str(self.second))
        
    def eval(self, env):
        return (self.second.eval(self.first.eval(env)))
        

print("\n----- Test Sequence -----")
print(Sequence(Assign('x', Add(Number(1), Number(1))),
    Assign('y', Add(Variable('x'), Number(3)))).eval(Env({})))
    
    
class While:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
        
    def __str__(self):
        return "<<While ({}) {}>>".format(str(self.condition), 
            str(self.body))
       
    def eval(self, env):
        if self.condition.eval(env) == Boolean(True):
            new_env = self.body.eval(env)
            return self.eval(new_env)
        else:
            return env

print("\n----- Test While -----")           
print(While(LessThan(Variable('x'), Number(5)),
    Assign('x', Multiply(Variable('x'), Number(3)))).eval(Env({'x': Number(1)})))

