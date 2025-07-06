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
            'exp': r'e^',
            'sqrt': r'\\sqrt',
            'log': r'\\log',
            'ln': r'\\ln'
        }
        
        # Constants mappings
        self.constants = {
            'pi': r'\\pi',
            'e': r'e',
            'E': r'e'  # SymPy uses E for Euler's number
        }
    
    def clean_integral_setup(self, integral_setup_str: str) -> str:
        """Clean and format the integral_setup LaTeX string"""
        if not integral_setup_str:
            return ""
        
        result = integral_setup_str
        
        # Fix exponentials: ** → ^
        result = self._fix_exponentials(result)
        
        # Fix mathematical functions
        result = self._fix_math_functions(result)
        
        # Fix constants
        result = self._fix_constants(result)
        
        # Fix multiplication spacing
        result = self._fix_multiplication_spacing(result)
        
        # Clean extra spaces
        result = self._clean_spacing(result)
        
        return result
    
    def _fix_exponentials(self, text: str) -> str:
        """Convert ** to ^ for LaTeX exponents"""
        # Handle cases like x**2 → x^{2}
        result = re.sub(r'(\w+)\*\*(\w+|\d+)', r'\1^{\2}', text)
        # Handle parentheses: (expr)**n → (expr)^{n}
        result = re.sub(r'\)\*\*(\w+|\d+)', r')^{\1}', result)
        return result
    
    def _fix_math_functions(self, text: str) -> str:
        """Fix mathematical functions for proper LaTeX rendering"""
        result = text
        
        for func, latex_func in self.math_functions.items():
            if func == 'exp':
                # Special handling for exp(x) → e^{x}
                result = re.sub(rf'{func}\(([^)]+)\)', rf'{latex_func}{{\1}}', result)
            else:
                # For trig functions: sin(x) → \sin(x)
                result = re.sub(rf'\b{func}\b', latex_func, result)
        
        return result
    
    def _fix_constants(self, text: str) -> str:
        """Fix mathematical constants"""
        result = text
        
        for const, latex_const in self.constants.items():
            # Only replace if it's a standalone constant (word boundary)
            result = re.sub(rf'\b{const}\b', latex_const, result)
        
        return result
    
    def _fix_multiplication_spacing(self, text: str) -> str:
        """Fix multiplication to have proper spacing"""
        # Fix cases like 2*r → 2 r, but preserve things like cos(theta)
        result = re.sub(r'(\d+)\*([a-zA-Z])', r'\1 \2', text)
        result = re.sub(r'([a-zA-Z])\*([a-zA-Z])', r'\1 \2', result)
        
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
        
        # Handle fractions: 50/3 → \frac{50}{3}
        result = re.sub(r'(\d+)/(\d+)', r'\\frac{\1}{\2}', exact)
        
        # Handle mathematical constants
        result = self._fix_constants(result)
        
        # Handle square roots: sqrt(x) → \sqrt{x}
        result = re.sub(r'sqrt\(([^)]+)\)', r'\\sqrt{\1}', result)
        
        # Handle exponentials in exact solutions
        result = self._fix_exponentials(result)
        
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
            'Mass': 'M'
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