import streamlit as st
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr
import re

class MathAgent:
    def __init__(self):
        pass  # No persistent symbols stored across evaluations

    def evaluate(self, expression):
        """
        Evaluate a general arithmetic expression, providing helpful feedback for errors.
        """
        # Basic cleanup: strip unnecessary parts
        expression = expression.strip().rstrip("?")
        
        # Prepare a fresh symbol dictionary for each evaluation
        symbols = {}
        
        # Identify symbols in the expression for Sympy parsing (for cases with variables)
        tokens = set(re.findall(r'[a-zA-Z_]\w*', expression))
        sympy_funcs = {fname for fname in dir(sp) if callable(getattr(sp, fname))}
        symbols_found = tokens - sympy_funcs
        for sym in symbols_found:
            symbols[sym] = sp.symbols(sym)

        try:
            # Convert the input into a Sympy expression using the fresh symbols
            expr = parse_expr(expression, local_dict=symbols)
            # Evaluate the expression numerically if possible
            result = expr.evalf()
            return str(result)
        except SyntaxError:
            return ("It seems there's a syntax error in your expression. "
                    "Please check your operators and operands.")
        except Exception as e:
            return f"Error evaluating expression: {e}"

# Streamlit app layout
st.title("Math Agent")
st.write("Ask me a math question with operations +, -, *, /, and parentheses.")

# Create an instance of MathAgent
agent = MathAgent()

# Input text box for the user to enter their math expression
user_input = st.text_input("Your math expression:", value="", key="unique_math_input")

# If the user has provided input
if user_input:
    answer = agent.evaluate(user_input)
    st.write(f"**Answer:** {answer}")

#( 12 - 30 ) * 12 ( 10 + 300)