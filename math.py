import sympy as sp
from sympy.parsing.sympy_parser import parse_expr
import re

class MathAgent:
    def __init__(self):
        # Initialize symbols that might be used frequently
        self.symbols = {}
        # Predefine some common symbols or allow dynamic creation
        # self.symbols.update({'x': sp.symbols('x'), 'y': sp.symbols('y')})
    
    def parse_symbols(self, expression):
        # Extract symbols (variables) from the expression string.
        # This is a simplistic approach: find alphabetic characters that are not known functions.
        tokens = set(re.findall(r'[a-zA-Z_]\w*', expression))
        # Filter out known sympy functions (a more comprehensive list can be maintained)
        sympy_funcs = {fname for fname in dir(sp) if callable(getattr(sp, fname))}
        symbols = tokens - sympy_funcs
        for sym in symbols:
            if sym not in self.symbols:
                self.symbols[sym] = sp.symbols(sym)
    
    def evaluate(self, question):
        """
        Evaluate a math question and return an answer.
        """
        # Remove any question-related words to isolate the expression
        # This is a basic approach; more sophisticated NLP could be used for advanced parsing.
        question = question.lower().strip("?")
        
        # Identify common operations based on keywords
        if "solve" in question:
            # Example: "Solve x^2 - 4 = 0"
            equation_part = question.split("solve",1)[1].strip()
            if "=" in equation_part:
                left, right = equation_part.split("=")
                expr = parse_expr(left) - parse_expr(right)
            else:
                expr = parse_expr(equation_part)
            self.parse_symbols(str(expr))
            # Attempt to solve for all symbols found
            solutions = {}
            for sym in self.symbols.values():
                sol = sp.solve(expr, sym)
                if sol:
                    solutions[str(sym)] = sol
            return f"Solutions: {solutions}" if solutions else "No solutions found."
        
        elif "integrate" in question:
            # Example: "Integrate sin(x) dx"
            # Extract the integrand
            integrand_part = question.split("integrate",1)[1].strip()
            # Basic handling for 'dx' at end:
            if integrand_part.endswith("dx"):
                integrand_part = integrand_part[:-2].strip()
            self.parse_symbols(integrand_part)
            # We'll integrate with respect to the first symbol found
            if self.symbols:
                var = list(self.symbols.values())[0]
            else:
                var = sp.symbols('x')
            integrand = parse_expr(integrand_part, local_dict=self.symbols)
            result = sp.integrals.integrals.Integral(integrand, var).doit()
            return str(result)
        
        elif "differentiate" in question or "derive" in question:
            # Example: "Differentiate x**2 + sin(x) with respect to x"
            # Extract the function part
            func_part = question.split("differentiate",1)[-1] if "differentiate" in question else question.split("derive",1)[-1]
            # Try to find "with respect to"
            wrt_match = re.search(r'with respect to (\w+)', func_part)
            if wrt_match:
                var_name = wrt_match.group(1)
                var = sp.symbols(var_name)
                func_part = func_part.split("with respect to",1)[0]
            else:
                # default variable
                var = sp.symbols('x')
            self.parse_symbols(func_part)
            self.symbols[str(var)] = var  # ensure var is in symbols
            func_expr = parse_expr(func_part, local_dict=self.symbols)
            result = sp.diff(func_expr, var)
            return str(result)
        
        elif "simplify" in question:
            # Example: "Simplify (x^2 - 1)/(x - 1)"
            expr_part = question.split("simplify",1)[1].strip()
            self.parse_symbols(expr_part)
            expr = parse_expr(expr_part, local_dict=self.symbols)
            result = sp.simplify(expr)
            return str(result)
        
        else:
            # Try to evaluate as a plain expression
            try:
                self.parse_symbols(question)
                expr = parse_expr(question, local_dict=self.symbols)
                result = expr.evalf()  # numerical evaluation if possible
                return str(result)
            except Exception as e:
                return f"Sorry, I couldn't understand the question. {e}"

# Interactive loop with the MathAgent
agent = MathAgent()

print("Math Agent: Ask me a math question (or type 'exit' to quit).")
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Math Agent: Goodbye!")
        break
    answer = agent.evaluate(user_input)
    print(f"Math Agent: {answer}")
