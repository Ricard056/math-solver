#!/usr/bin/env python3
import sympy as sp
from typing import List, Tuple, Optional, Dict, Any
import re

from models.exercise import Exercise

class IntegralSolver:
    """Solves integrals with automatic coordinate system detection and improved quantity type detection"""
    
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
    
    def normalize_function(self, func_str: str) -> str:
        """Remove constant multiplicative factors to identify base function"""
        if not func_str or func_str.strip() == "":
            return "1"
        
        # Parse the expression
        try:
            expr = sp.sympify(func_str, locals=self.symbols)
            
            # Extract non-constant factors
            if expr.is_number:
                return "1"
            
            # Handle products - separate constants from variables
            if expr.is_Mul:
                constant_part = 1
                variable_part = 1
                
                for factor in expr.args:
                    if factor.is_number:
                        constant_part *= factor
                    else:
                        variable_part *= factor
                
                if variable_part == 1:
                    return "1"
                else:
                    return str(variable_part)
            
            # If not a product, return as is (already normalized)
            return str(expr)
            
        except Exception:
            # Fallback: manual normalization for simple cases
            func_str = func_str.strip()
            
            # Remove leading constants like "2*", "3*", etc.
            pattern = r'^(\d+(?:\.\d+)?)\s*\*\s*(.+)$'
            match = re.match(pattern, func_str)
            if match:
                return match.group(2)
            
            # Handle pure constants
            if re.match(r'^\d+(?:\.\d+)?$', func_str):
                return "1"
            
            return func_str
    
    def is_spherical_jacobian(self, normalized_func: str) -> bool:
        """Detect if function is only the spherical Jacobian"""
        spherical_jacobian_patterns = [
            r'^r\*\*2\*sin\(phi\)$',
            r'^rho\*\*2\*sin\(theta\)$',
            r'^r\^2\*sin\(phi\)$',
            r'^rho\^2\*sin\(theta\)$',
            r'^r\*\*2\*sin\(theta\)$',  # Alternative naming
            r'^rho\*\*2\*sin\(phi\)$'   # Alternative naming
        ]
        
        for pattern in spherical_jacobian_patterns:
            if re.match(pattern, normalized_func.replace(' ', '')):
                return True
        
        return False
    
    def is_cylindrical_jacobian(self, normalized_func: str) -> bool:
        """Detect if function is only the cylindrical Jacobian"""
        return normalized_func.strip() == "r"
    
    def determine_quantity_type_and_units(self, exercise: 'Exercise', base_unit: str = "u") -> Tuple[Optional[str], Optional[str]]:
        """Determine quantity type and units based on function and coordinate system"""
        function = exercise.function
        coordinate_system = exercise.coordinate_system
        num_integrals = len(exercise.integrals)
        
        # Normalize function (remove constant factors)
        normalized_function = self.normalize_function(function)
        
        if coordinate_system == "cartesian":
            if normalized_function == "1":
                # Pure geometric integrals
                if num_integrals == 1:
                    return "Length", f"{base_unit}"
                elif num_integrals == 2:
                    return "Area", f"{base_unit}^2"
                elif num_integrals == 3:
                    return "Volume", f"{base_unit}^3"
            else:
                if num_integrals == 1:
                    return "Area", f"{base_unit}^2"
                elif num_integrals == 2:
                    return "Volume", f"{base_unit}^3"  # Surface with height/thickness
                elif num_integrals == 3:
                    return "Mass", f"{base_unit}"      # Density × volume
                    
        elif coordinate_system == "polar":
            if normalized_function == "r":  # Only Jacobian
                return "Area", f"{base_unit}^2"
            else:  # Additional function beyond Jacobian
                return "Volume", f"{base_unit}^3"
                
        elif coordinate_system == "cylindrical":
            if self.is_cylindrical_jacobian(normalized_function):
                if num_integrals == 2:
                    return "Area", f"{base_unit}^2"
                elif num_integrals == 3:
                    return "Volume", f"{base_unit}^3"
            else:
                if num_integrals == 2:
                    return "Volume", f"{base_unit}^3"
                elif num_integrals == 3:
                    return "Mass", f"{base_unit}"
                    
        elif coordinate_system == "spherical":
            if self.is_spherical_jacobian(normalized_function):
                return "Volume", f"{base_unit}^3"
            else:
                return "Mass", f"{base_unit}"
        
        # Default fallback
        return None, None
    
    def parse_expression(self, expr_str: str) -> sp.Expr:
        """Parse mathematical expression string to SymPy expression"""
        # Replace common notation
        expr_str = expr_str.replace('^', '**')
        
        # Parse with predefined symbols
        try:
            return sp.sympify(expr_str, locals=self.symbols)
        except Exception as e:
            raise ValueError(f"Cannot parse expression '{expr_str}': {e}")
    
    def solve_integral(self, exercise: 'Exercise') -> Tuple[Optional[str], Optional[float]]:
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
    
    def generate_latex_integral(self, exercise: 'Exercise') -> str:
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
    
    def determine_quantity_type(self, exercise: 'Exercise', base_unit: str = "u") -> Optional[str]:
        """Determine quantity type using the improved logic"""
        quantity_type, _ = self.determine_quantity_type_and_units(exercise, base_unit)
        return quantity_type
    
    def determine_units(self, exercise: 'Exercise', base_unit: str = "u") -> Optional[str]:
        """Determine units using the improved logic"""
        _, units = self.determine_quantity_type_and_units(exercise, base_unit)
        return units