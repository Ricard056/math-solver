import sympy as sp
from typing import List, Tuple, Optional, Dict, Any
import re

class IntegralSolver:
    """Solves integrals with automatic coordinate system detection"""
    
    COORDINATE_PATTERNS = {
        'cartesian': {'x', 'y', 'z'},
        'polar': {'r', 'theta'},
        'cylindrical': {'r', 'theta', 'z'},
        'spherical': {'rho', 'theta', 'phi'}
    }
    
    def __init__(self):
        # Define common symbols
        self.symbols = {
            'x': sp.Symbol('x'),
            'y': sp.Symbol('y'),
            'z': sp.Symbol('z'),
            'r': sp.Symbol('r', positive=True),
            'theta': sp.Symbol('theta'),
            'phi': sp.Symbol('phi'),
            'rho': sp.Symbol('rho', positive=True),
            'pi': sp.pi,
            'e': sp.E
        }
    
    def detect_coordinate_system(self, variables: List[str]) -> str:
        """Auto-detect coordinate system from variables"""
        var_set = set(variables)
        
        # Check exact matches first
        if var_set == {'r', 'theta'}:
            return 'polar'
        elif var_set == {'r', 'theta', 'z'}:
            return 'cylindrical'
        elif var_set == {'rho', 'theta', 'phi'}:
            return 'spherical'
        elif var_set.issubset({'x', 'y', 'z'}):
            return 'cartesian'
        
        # Default to cartesian if uncertain
        return 'cartesian'
    
    def parse_expression(self, expr_str: str) -> sp.Expr:
        """Parse mathematical expression string to SymPy expression"""
        # Replace common notation
        expr_str = expr_str.replace('^', '**')
        
        # Parse with predefined symbols
        try:
            return sp.sympify(expr_str, locals=self.symbols)
        except Exception as e:
            raise ValueError(f"Cannot parse expression '{expr_str}': {e}")
    
def solve_integral(self, exercise) -> Tuple[Optional[str], Optional[float]]:
        """Solve the integral and return exact and decimal solutions"""
        try:
            # Parse the function
            integrand = self.parse_expression(exercise.function)
            
            # Sort integrals by order (inner to outer)
            sorted_integrals = sorted(exercise.integrals, key=lambda x: x.order)
            
            # Perform integration
            result = integrand
            for integral in sorted_integrals:
                var = self.symbols.get(integral.var, sp.Symbol(integral.var))
                lower = self.parse_expression(integral.limits.lower)
                upper = self.parse_expression(integral.limits.upper)
                
                # Integrate
                antiderivative = sp.integrate(result, var)
                # Apply limits
                result = antiderivative.subs(var, upper) - antiderivative.subs(var, lower)
                
                # Simplify after each integration
                result = sp.simplify(result)
            
            # Get exact solution
            exact_solution = str(result)
            
            # Get decimal solution
            try:
                decimal_solution = float(result.evalf())
            except:
                decimal_solution = None
            
            return exact_solution, decimal_solution
            
        except Exception as e:
            print(f"Error solving integral: {e}")
            return None, None
    
def generate_latex_integral(self, exercise) -> str:
        """Generate LaTeX code for the integral setup"""
        # Sort integrals by order (outer to inner for display)
        sorted_integrals = sorted(exercise.integrals, key=lambda x: -x.order)
        
        latex = ""
        for integral in sorted_integrals:
            latex += f"\\int_{{{integral.limits.lower}}}^{{{integral.limits.upper}}} "
        
        # Add function and differentials
        function_latex = exercise.function.replace('**', '^').replace('*', ' ')
        latex += f"{function_latex} \\, "
        
        # Add differentials in reverse order
        for integral in sorted(exercise.integrals, key=lambda x: x.order):
            latex += f"d{integral.var} "
        
        return latex.strip()
    
def determine_quantity_type(self, exercise) -> Optional[str]:
        """Determine if integral represents Area, Volume, or Mass"""
        num_integrals = len(exercise.integrals)
        coord_system = exercise.coordinate_system
        
        if num_integrals == 2:
            return "Area"
        elif num_integrals == 3:
            # Check if function suggests density (contains rho or density keywords)
            if 'rho' in exercise.function.lower() or 'density' in exercise.function.lower():
                return "Mass"
            return "Volume"
        
        return None