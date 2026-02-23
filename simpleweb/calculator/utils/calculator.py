class Calcu:
    def __init__(self, num1:float, num2:float, opp:str):
        try:
            self.num1 = num1
            self.num2 = num2
            self.opp = opp
        except(ValueError, TypeError):
            self.num1 = 0
            self.num2 = 0
    
    def calculate(self)->float:
        switch_opp = {
            'add': self.num1 + self.num2,
            'sub': self.num1 - self.num2,
            'mul': self.num1 * self.num2,
            'div': self.num1 / self.num2 if self.num2 != 0 else 0
        }
        result = switch_opp.get(self.opp, 0)
        return result
            