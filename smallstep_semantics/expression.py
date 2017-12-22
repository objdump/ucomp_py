
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
        
    def reduce(self):
        if self.left.reducible():
            return Add(self.left.reduce(), self.right)
        elif self.right.reducible():
            return Add(self.left, self.right.reduce())
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

    def reduce(self):
        if self.left.reducible():
            return Mulitiply(self.left.reduce(), self.right)
        elif self.right.reducible():
            return Mulitiply(self.left, self.right.reduce())
        else:
            return Number(self.left.value * self.right.value)

class Machine:
    def __init__(self, expression):
        self.expression = expression
        
    def step(self):
        self.expression = self.expression.reduce()
        
    def run(self):
        while self.expression.reducible():
            print(self.expression)
            self.step()
        print(self.expression)
        

class Variable:
    def __init__(self, name):
        self.name = name
        
    def __str__(self):
        return str(name)
        
    def reducible(self):
        return True
        
    def reduce(self, env):
        return env[name]
        

        
Machine(Add(Mulitiply(Number(1), Number(2)),
    Mulitiply(Number(3), Number(4)))).run()
    

    

        