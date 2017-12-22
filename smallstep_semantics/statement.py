
class Number:
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return str(self.value)
        
    def reducible(self):
        return False
        
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
            stri = stri +', '+str(item[0])+':'+str(item[1])
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
            print("#{}, #{}".format(self.statement, str(self.env)))
            self.step()
        print("#{}, #{}".format(self.statement, self.env))
        

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
        return isinstance(other, Dothing)
        
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
        
machine = Machine(Assign('x', Add(Variable('x'), Number(1))),
                  Env({'x':Number(2)}))
machine.run()

           
