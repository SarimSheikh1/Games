import sympy as sp
from sympy.parsing.sympy_parser import parse_expr
import re

class MathAgent:
    def __init__(self):
        self.symbols = {}

    def parse_symbols(self, expression):
        tokens = set(re.findall(r'[a-zA-Z_]\w*', expression))
        sympy_funcs = {fname for fname in dir(sp) if callable(getattr(sp, fname))}
        symbols_found = tokens - sympy_funcs
        for sym in symbols_found:
            if sym not in self.symbols:
                self.symbols[sym] = sp.symbols(sym)

    def evaluate(self, question):
        question = question.lower().strip().rstrip("?")
        
        try:
            # Parse symbols first
            self.parse_symbols(question)
            # Convert to Sympy expression
            expr = parse_expr(question, local_dict=self.symbols)
            # Evaluate expression numerically if possible
            result = expr.evalf()
            return str(result)
        except SyntaxError as se:
            return "Error: The expression contains a syntax error. Please check your input."
        except Exception as e:
            return f"Error evaluating expression: {e}"

agent = MathAgent()

print("Math Agent: Ask me a math question with operations +, -, *, /, and parentheses (or type 'exit' to quit).")
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Math Agent: Goodbye!")
        break
    answer = agent.evaluate(user_input)
    print(f"Math Agent: {answer}")
