import re

class Infix:
    def __init__(self, function):
        self.function = function
    def __ror__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))
    def __or__(self, other):
        return self.function(other)
    def __rlshift__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))
    def __rshift__(self, other):
        return self.function(other)
    def __call__(self, value1, value2):
        return self.function(value1, value2)

iff = Infix(lambda x,y: x == y)
implies = Infix(lambda x,y: not x or y)
xor = Infix(lambda x,y: x == y)


def program_help():
    print("Function latex_print takes up to 2 optional arguments")
    print("Without argument, it defaults to 10 for true/false values")
    print("With one argument, it expects a string of two characters to represent true/false values")
    print("With 2 arguments, the first/second arguments represent the true/false values")


class TTable:
    def __init__(self, variables, formula):
        self.variables = variables
        self.tvalues = []
        self.formula = formula

        # creates a list with all possible truth valuations
        for i in range(2 ** len(variables)):
            self.tvalues.append('{0:b}'.format(i))
        self.tvalues = map(lambda x: ('{:0' + str(len(self.variables)) + '}').format(int(x)), self.tvalues)
        self.tvalues = map(lambda x: map(lambda y: int(y), x), self.tvalues)

    def print_latex(self, *optional):
        if len(optional) == 0:
            output = lambda x: int(x)
        elif len(optional) == 2:
            output = lambda x: optional[0] if x else optional[1]
        elif len(optional) == 1:
            output = lambda x: optional[0][0] if x else optional[0][1]
        else:
            program_help()

        # begin
        print("\\begin{center}")
        print("\\begin{tabular}{", end='')
        for variable in self.variables:
            print('c', end='')
        print('|', end='')
        for formula in self.formula:
            print('c', end='')
        print('}')
        # first row
        first_different = 0
        for variable in self.variables:
            if first_different == 0:
                print(variable, end=' ')
                first_different = 1
            else:
                print('&', variable, end=' ')
        for formula in self.formula:
            split = re.findall(r"[\w']+|[(, 2)]", formula)
            print(' &', end=' ')
            for expression in split:
                if expression == "not":
                    print("$\\neg$", end=' ')
                elif expression == "and":
                    print(" $\\land$", end=' ')
                elif expression == "or":
                    print(" $\\lor$", end=' ')
                elif expression == "implies":
                    print(" $\\rightarrow$", end=' ')
                elif expression == "iff":
                    print(" $\\leftrightarrow$", end=' ')
                elif expression == "xor":
                    print(" $\\oplus")
                else:
                    print(''.join(expression.split()), end='')
        print('\\\\\\hline')
        # table values
        for truth_valuation in self.tvalues:
            # doesn't print & in first iteration
            first_different = 0
            # assign truth values
            for n, value in enumerate(truth_valuation):
                locals()[self.variables[n]] = value
                if first_different == 0:
                    print(output(bool(value)), end=' ')
                    first_different = 1
                else:
                    print('&', output(bool(value)), end=' ')
            for formula in self.formula:
                    print('&', output(eval(formula.replace("iff", "|iff|").replace("implies", "|implies|").replace("xor", "|xor|"))), end=' ')
            print('\\\\')
        # end
        print("\\end{tabular}")
        print("\\end{center}")


test = TTable(['P', 'Q', 'R'],
              ["(P implies Q)", "(Q implies R)", "(P iff R)"])
test.print_latex("TF")
