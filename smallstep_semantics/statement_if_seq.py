# -*- coding: utf-8 -*-  

class Number:
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return str(self.value)
        
    def reducible(self):
        return False

class Boolean:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        if self.value:
            return "true"
        else:
            return "false"

    def reducible(self):
        return False

    def __eq__(self, other):
        return self.value == other.value
    
class Add:
    def __init__(self, left, right):
        self.left = left
        self.right = right
        
    def __str__(self):
        return str(self.left)+'+'+str(self.right)
  
    def reducible(self):
        return True  
        
    def reduce(self, env):
        if self.left.reducible():
            return Add(self.left.reduce(env), self.right)
        elif self.right.reducible():
            return Add(self.left, self.right.reduce(env))
        else:
            return Number(self.left.value + self.right.value)
           
        
class Mulitiply:
    def __init__(self, left, right):
        self.left = left
        self.right = right
        
    def __str__(self):
        return str(self.left)+'*'+str(self.right)   

    def reducible(self):
        return True

    def reduce(self, env):
        if self.left.reducible():
            return Mulitiply(self.left.reduce(env), self.right)
        elif self.right.reducible():
            return Mulitiply(self.left, self.right.reduce(env))
        else:
            return Number(self.left.value * self.right.value)

            
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
        
    def get(self, name):
        return self.dict[name]
            
class Machine:
    def __init__(self, statement, env):
        self.statement = statement
        self.env = env
        
    def step(self):
        self.statement, self.env = self.statement.reduce(self.env)
        
    def run(self):
        while self.statement.reducible():
            print("#{}, #{}".format(str(self.statement), str(self.env)))
            self.step()
        print("#{}, #{}".format(str(self.statement), str(self.env)))
        

class Variable:
    def __init__(self, name):
        self.name = name
        
    def __str__(self):
        return str(self.name)
        
    def reducible(self):
        return True
        
    def reduce(self, env):
        return env.get(self.name)
        
class DoNothing:
    def __init__(self):
        pass
        
    def __str__(self):
        return 'do-nothing'
        
    def __eq__(self, other):
        return isinstance(other, DoNothing)
        
    def reducible(self):
        return False
        
class Assign:
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression
        
    def __str__(self):
        return str(self.name)+'='+str(self.expression)
        
    def reducible(self):
        return True
        
    def reduce(self, env):
        if self.expression.reducible():
            return Assign(self.name, self.expression.reduce(env)), env
        else:

            newEnv = env.newUpdate(self.name, self.expression)
            return DoNothing(), newEnv


class If:
    def __init__(self, condition, consequence, alternative):
        self.condition = condition
        self.consequence = consequence
        self.alternative = alternative

    def __str__(self):
        return "If [{}] [{}] else [{}]".format(str(self.condition),
                                                   str(self.consequence), str(self.alternative))

    def reducible(self):
        return True

    def reduce(self, env):
        if self.condition.reducible():
            return (If(self.condition.reduce(env), self.consequence, self.alternative), env)
        else:
            if self.condition == Boolean(True):
                return self.consequence, env
            else:
                return self.alternative, env

class Sequence:
    def __init__(self, first, second):
        self.first = first
        self.second = second
        
    def __str__(self):
        return "Sequence: [{}], [{}]".format(str(self.first), str(self.second))
        
    def reducible(self):
        return True
        
    def reduce(self, env):
        if self.first == DoNothing():
            return self.second, env
        else:
            first_reduced, env_reduced = self.first.reduce(env)
            return Sequence(first_reduced, self.second), env_reduced

                

print("Verify statement if - if x True: y = 1 else y = 2 ")
Machine(
    If(Variable('x'), 
        Assign('y', Number(1)),
        Assign('y', Number(2))),
    Env({'x':Boolean(True)})).run()
    
print("-----------------------------------")

print("Verify statement squence - x = 1 + 1， y = x + 3")
Machine(
    Sequence(Assign('x', Add(Number(1), Number(1))),  
        Assign('y', Add(Variable('x'), Number(3)))),
    Env({})).run()
    
print("-----------------------------------")



           
