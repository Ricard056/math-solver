#!/usr/bin/env python3
import re
from typing import Optional

class LaTeXFormatter:
    """Formatter class for cleaning and formatting mathematical LaTeX content"""
    
    def __init__(self):
        # Mathematical function mappings for LaTeX
        self.math_functions = {
            'sin': r'\\sin',
            'cos': r'\\cos',
            'tan': r'\\tan',
            'sec': r'\\sec',
            'csc': r'\\csc',
            'cot': r'\\cot',
            'arcsin': r'\\arcsin',
            'arccos': r'\\arccos',
            'arctan': r'\\arctan',
            'sinh': r'\\sinh',
            'cosh': r'\\cosh',
            'tanh': r'\\tanh',
            'sqrt': r'\\sqrt',
            'log': r'\\log',
            'ln': r'\\ln',
            'lim': r'\\lim',
            'max': r'\\max',
            'min': r'\\min'
        }
        
        # Greek letters and special symbols
        self.greek_symbols = {
            'alpha': r'\\alpha',
            'beta': r'\\beta',
            'gamma': r'\\gamma',
            'Gamma': r'\\Gamma',
            'delta': r'\\delta',
            'Delta': r'\\Delta',
            'epsilon': r'\\epsilon',
            'varepsilon': r'\\varepsilon',
            'zeta': r'\\zeta',
            'eta': r'\\eta',
            'theta': r'\\theta',
            'Theta': r'\\Theta',
            'vartheta': r'\\vartheta',
            'iota': r'\\iota',
            'kappa': r'\\kappa',
            'lambda': r'\\lambda',
            'Lambda': r'\\Lambda',
            'mu': r'\\mu',
            'nu': r'\\nu',
            'xi': r'\\xi',
            'Xi': r'\\Xi',
            'pi': r'\\pi',
            'Pi': r'\\Pi',
            'rho': r'\\rho',
            'varrho': r'\\varrho',
            'sigma': r'\\sigma',
            'Sigma': r'\\Sigma',
            'tau': r'\\tau',
            'upsilon': r'\\upsilon',
            'Upsilon': r'\\Upsilon',
            'phi': r'\\phi',
            'Phi': r'\\Phi',
            'varphi': r'\\varphi',
            'chi': r'\\chi',
            'psi': r'\\psi',
            'Psi': r'\\Psi',
            'omega': r'\\omega',
            'Omega': r'\\Omega'
        }
        
        # Constants mappings
        self.constants = {
            'E': r'e',  # SymPy uses E for Euler's number
            'oo': r'\\infty',  # SymPy infinity
            'I': r'i'   # SymPy imaginary unit
        }
    
    def clean_integral_setup(self, integral_setup_str: str) -> str:
        """Clean and format the integral_setup LaTeX string"""
        if not integral_setup_str:
            return ""
        
        result = integral_setup_str
        
        # Fix Greek symbols FIRST (before other operations)
        result = self._fix_greek_symbols(result)
        
        # Fix exponentials: ** → ^
        result = self._fix_exponentials(result)
        
        # Fix exp() function specially
        result = self._fix_exp_function(result)
        
        # Fix mathematical functions
        result = self._fix_math_functions(result)
        
        # Fix constants
        result = self._fix_constants(result)
        
        # Remove unnecessary multiplication symbols
        result = self._remove_multiplication_symbols(result)
        
        # Fix differentials - SIMPLE VERSION
        result = self._fix_differentials(result)
        
        # Clean extra spaces
        result = self._clean_spacing(result)
        
        return result
    
    def _fix_greek_symbols(self, text: str) -> str:
        """Convert Greek letter names to LaTeX symbols"""
        result = text
        
        for symbol, latex_symbol in self.greek_symbols.items():
            # Use word boundaries to avoid partial matches
            result = re.sub(rf'\b{symbol}\b', latex_symbol, result)
        
        return result
    
    def _fix_exponentials(self, text: str) -> str:
        """Convert ** to ^ for LaTeX exponents with proper braces"""
        result = text
        
        # Handle complex exponents: x**(y + z) → x^{y + z}
        result = re.sub(r'(\w+|\))\*\*\(([^)]+)\)', r'\1^{\2}', result)
        
        # Handle simple exponents: x**2 → x^{2}
        result = re.sub(r'(\w+|\))\*\*(\w+|\d+)', r'\1^{\2}', result)
        
        return result
    
    def _fix_exp_function(self, text: str) -> str:
        """Convert exp() functions to e^{} format"""
        result = text
        
        # Handle nested parentheses in exp functions
        # exp(complex_expression) → e^{complex_expression}
        
        def replace_exp(match):
            content = match.group(1)
            return f'e^{{{content}}}'
        
        # Match exp with balanced parentheses
        # This handles exp(x + y), exp(2), exp(x*y), etc.
        result = re.sub(r'exp\(([^)]+(?:\([^)]*\)[^)]*)*)\)', replace_exp, result)
        
        return result
    
    def _fix_math_functions(self, text: str) -> str:
        """Fix mathematical functions for proper LaTeX rendering"""
        result = text
        
        for func, latex_func in self.math_functions.items():
            # For standard functions: sin(x) → \sin(x)
            result = re.sub(rf'\b{func}\b', latex_func, result)
        
        return result
    
    def _fix_constants(self, text: str) -> str:
        """Fix mathematical constants"""
        result = text
        
        for const, latex_const in self.constants.items():
            # Only replace if it's a standalone constant (word boundary)
            result = re.sub(rf'\b{const}\b', latex_const, result)
        
        return result
    
    def _remove_multiplication_symbols(self, text: str) -> str:
        """Remove unnecessary multiplication symbols"""
        result = text
        
        # Remove * between number and variable: 2*x → 2x
        result = re.sub(r'(\d+)\*([a-zA-Z\\])', r'\1\2', result)
        
        # Remove * between variables: x*y → xy (but be careful with functions)
        result = re.sub(r'([a-zA-Z])\*([a-zA-Z])', r'\1\2', result)
        
        # Remove * between variable and function: r*\sin → r\sin
        result = re.sub(r'([a-zA-Z])\*(\\[a-zA-Z]+)', r'\1\2', result)
        
        # Remove * between number and function: 2*\sin → 2\sin
        result = re.sub(r'(\d+)\*(\\[a-zA-Z]+)', r'\1\2', result)
        
        # Remove * between closing brace and variable: }*x → }x
        result = re.sub(r'\}\*([a-zA-Z])', r'}\1', result)
        
        # Remove * between variable and opening brace: x*{ → x{
        result = re.sub(r'([a-zA-Z])\*\{', r'\1{', result)
        
        return result
    
    def _fix_differentials(self, text: str) -> str:
        """Fix differentials: dtheta → d\theta, etc."""
        result = text
        
        # SIMPLE AND DIRECT - only the most common ones
        result = re.sub(r'\bdtheta\b', r'd\\theta', result)
        result = re.sub(r'\bdphi\b', r'd\\phi', result)
        result = re.sub(r'\bdrho\b', r'd\\rho', result)
        
        return result
    
    def _clean_spacing(self, text: str) -> str:
        """Clean up extra spaces while preserving LaTeX structure"""
        # Remove extra spaces but preserve single spaces
        result = re.sub(r' +', ' ', text)
        result = result.strip()
        
        return result
    
    def format_solution_display(self, exact: str, decimal: float, units: str, precision: int) -> str:
        """Format the solution part: exact = decimal units"""
        if not exact or decimal is None:
            return "N/A"
        
        # Clean the exact solution
        exact_clean = self._format_exact_solution(exact)
        
        # Format decimal with specified precision
        decimal_str = f"{decimal:.{precision}f}"
        
        # Format units
        units_formatted = self._format_units(units)
        
        return f"{exact_clean} = {decimal_str} \\ {units_formatted}"
    
    def _format_exact_solution(self, exact: str) -> str:
        """Format exact solution for LaTeX display"""
        if not exact:
            return ""
        
        result = exact
        
        # ESTRATEGIA: Procesar fracciones ANTES de transformar funciones
        # para evitar que \cos(1)/2 se convierta en \cos\dfrac{1}{2}
        
        # 1. Handle fractions FIRST (while functions are still in original form)
        result = self._fix_fractions_early(result)
        
        # 2. THEN fix Greek symbols
        result = self._fix_greek_symbols(result)
        
        # 3. Handle mathematical constants
        result = self._fix_constants(result)
        
        # 4. Handle square roots: sqrt(x) → \sqrt{x}
        result = re.sub(r'sqrt\(([^)]+)\)', r'\\sqrt{\1}', result)
        
        # 5. Handle exp functions
        result = self._fix_exp_function(result)
        
        # 6. Handle exponentials
        result = self._fix_exponentials(result)
        
        # 7. Fix math functions
        result = self._fix_math_functions(result)
        
        # 8. Remove unnecessary multiplications
        result = self._remove_multiplication_symbols(result)
        
        return result
    
    def _fix_fractions_early(self, text: str) -> str:
        """Fix fractions BEFORE other transformations to avoid conflicts"""
        result = text
        
        # Handle function calls with division: cos(1)/2 → dfrac{cos(1)}{2}
        # (BEFORE cos becomes \cos)
        result = re.sub(r'([a-zA-Z]+\([^)]+\))/(\d+)', r'\\dfrac{\1}{\2}', result)
        
        # Handle expressions in parentheses: (expression)/denominator
        result = re.sub(r'\(([^)]+)\)/(\d+)', r'\\dfrac{\1}{\2}', result)
        
        # Handle exp() specifically: exp(x)/2 → dfrac{exp(x)}{2}
        result = re.sub(r'(exp\([^)]+\))/(\d+)', r'\\dfrac{\1}{\2}', result)
        
        # Handle simple cases: variable/number, number/number
        result = re.sub(r'([a-zA-Z]+)/(\d+)', r'\\dfrac{\1}{\2}', result)
        result = re.sub(r'(\d+)/(\d+)', r'\\dfrac{\1}{\2}', result)
        
        return result
    
    def _format_units(self, units: str) -> str:
        """Format units for LaTeX display"""
        if not units:
            return "\\text{u}"
        
        # Handle exponential units: u^2 → \text{u}^2
        if '^' in units:
            base, exp = units.split('^', 1)
            return f"\\text{{{base}}}^{{{exp}}}"
        else:
            return f"\\text{{{units}}}"
    
    def get_quantity_label(self, quantity_type: Optional[str]) -> str:
        """Get the appropriate label for quantity type"""
        if not quantity_type:
            return ""
        
        labels = {
            'Area': 'A',
            'Volume': 'V',
            'Mass': 'M',
            'Length': 'L',
            'Measure': 'M'
        }
        
        return labels.get(quantity_type, "")
    
    def format_exercise_number(self, id_letter: Optional[str], id_part: Optional[int]) -> str:
        """Format the exercise number/letter for LaTeX items"""
        if id_letter:
            return f"[{id_letter})]"
        elif id_part:
            # Convert number to letter: 1→a, 2→b, etc.
            letter = chr(ord('a') + id_part - 1)
            return f"[{letter})]"
        else:
            return ""  # Regular numbered item