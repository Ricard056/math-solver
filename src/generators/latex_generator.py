#!/usr/bin/env python3
import os
import subprocess
from typing import Dict, Any, List
from pathlib import Path

class LaTeXGenerator:
    """Generates LaTeX files and PDFs from intermediate JSON"""
    
    def __init__(self):
        self.template = self._load_template()
    
    def _load_template(self) -> str:
        """Load LaTeX document template with improved structure"""
        return r"""
\documentclass[12pt]{article}
\usepackage[utf8]{inputenc}
\usepackage{amsmath}
\usepackage{geometry}
\usepackage{fancyhdr}
\usepackage{titling}
\usepackage{lmodern}
\geometry{letterpaper, margin=1in}
\pagestyle{fancy}
\fancyhf{}
\rhead{<<ASSIGNMENT_TYPE>> <<NUMBER>>}
\lhead{Solucionario}
\cfoot{\thepage}
\setlength{\droptitle}{-4em}
\title{\textbf{<<ASSIGNMENT_TYPE>> <<NUMBER>> \\[0.5em] \large Solucionario}}
\author{}
\date{}
\begin{document}
\maketitle
\section*{Resultados}
\everymath{\displaystyle}
\setlength{\jot}{10pt}
\begin{enumerate}
<<EXERCISES>>
\end{enumerate}
\end{document}
"""
    
    def _decimal_to_fraction(self, decimal_val: float) -> str:
        """Convert decimal to fraction string for exact display"""
        from fractions import Fraction
        
        # Convert to fraction with reasonable denominator limit
        frac = Fraction(decimal_val).limit_denominator(1000)
        
        if frac.denominator == 1:
            return str(frac.numerator)
        else:
            return f"{frac.numerator}/{frac.denominator}"
    
    def _format_mathematical_expression(self, expr_str: str) -> str:
        """Convert mathematical expressions to proper LaTeX"""
        result = expr_str
        
        # Handle mathematical constants and functions first
        replacements = {
            'pi': '\\pi',
            'theta': '\\theta', 
            'phi': '\\phi',
            'rho': '\\rho',
            'sqrt(': '\\sqrt{',
            'exp(': 'e^{',
            'sin(': '\\sin(',
            'cos(': '\\cos(',
            'E': 'e'
        }
        
        for old, new in replacements.items():
            result = result.replace(old, new)
        
        # Handle operators (order matters!)
        result = result.replace('**', '^')
        result = result.replace('*', ' ')  # Remove multiplication symbols
        result = result.replace('\\cdot', '')  # Remove \cdot
        
        # Fix parentheses for functions that need closing braces
        if '\\sqrt{' in result:
            result = self._fix_function_braces(result, '\\sqrt{')
        if 'e^{' in result:
            result = self._fix_function_braces(result, 'e^{')
            
        return result
    
    def _fix_function_braces(self, expr: str, func_pattern: str) -> str:
        """Fix braces for functions like sqrt and exp"""
        # This is a simplified version - handles basic cases
        if func_pattern in expr:
            # For now, just ensure closing braces exist
            open_count = expr.count('{')
            close_count = expr.count('}')
            if open_count > close_count:
                expr += '}' * (open_count - close_count)
        return expr
    
    def generate_latex(self, data: Dict[str, Any], output_path: str) -> None:
        """Generate LaTeX file from intermediate JSON"""
        # Extract metadata
        metadata = data['metadata']
        course = metadata['course']
        assignment = metadata['assignment']
        
        # Group exercises by ID and sum parts
        grouped_exercises = self._group_exercises(data['exercises'])
        
        # Generate exercise content
        exercises_latex = self._generate_exercises_latex(grouped_exercises)
        
        # Fill template
        latex_content = self.template
        latex_content = latex_content.replace('<<ASSIGNMENT_TYPE>>', assignment['type'])
        latex_content = latex_content.replace('<<NUMBER>>', str(assignment['number']))
        latex_content = latex_content.replace('<<EXERCISES>>', exercises_latex)
        
        # Save LaTeX file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(latex_content)
        
        print(f"LaTeX file generated: {output_path}")
    
    def _group_exercises(self, exercises: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """Group exercises by ID+letter and sum decimal solutions"""
        groups = {}
        
        for exercise in exercises:
            # Create group key using id + id_letter combination
            key = str(exercise['id'])
            if exercise['id_letter']:
                key += exercise['id_letter']
            
            if key not in groups:
                # Initialize group with first exercise
                groups[key] = {
                    'id': exercise['id'],
                    'id_letter': exercise['id_letter'],
                    'combined_solution': {
                        'exact': None,
                        'decimal': 0.0,
                        'quantity_type': exercise.get('solution', {}).get('quantity_type'),
                        'units': exercise.get('solution', {}).get('units')
                    },
                    'display_settings': exercise.get('display_settings', {}),
                    'parts': [],
                    'has_multiple_parts': False
                }
            
            # Add this exercise as a part
            groups[key]['parts'].append(exercise)
            
            # Check if this group has multiple parts (any exercise with id_part)
            if exercise.get('id_part') is not None:
                groups[key]['has_multiple_parts'] = True
            
            # Sum decimal solutions
            if exercise.get('solution', {}).get('decimal') is not None:
                groups[key]['combined_solution']['decimal'] += exercise['solution']['decimal']
        
        # Create combined exact solutions for display
        for key, group in groups.items():
            if len(group['parts']) > 1:
                # Multiple parts - convert decimal sum to fraction if possible
                decimal_val = group['combined_solution']['decimal']
                group['combined_solution']['exact'] = self._decimal_to_fraction(decimal_val)
            else:
                # Single part - use original exact solution
                original_solution = group['parts'][0].get('solution', {})
                group['combined_solution']['exact'] = original_solution.get('exact')
                group['combined_solution']['decimal'] = original_solution.get('decimal', 0.0)
        
        return groups
    
    def _generate_exercises_latex(self, grouped_exercises: Dict[str, Dict[str, Any]]) -> str:
        """Generate LaTeX for all exercises"""
        latex_parts = []
        
        for group_id in sorted(grouped_exercises.keys(), key=self._sort_key):
            group = grouped_exercises[group_id]
            latex_parts.append(self._generate_exercise_latex(group, group_id))
        
        return '\n'.join(latex_parts)
    
    def _sort_key(self, key: str) -> tuple:
        """Create sort key for exercise IDs (handles numbers and letters)"""
        # Extract number and letter parts
        import re
        match = re.match(r'(\d+)([a-z]*)', key)
        if match:
            num_part = int(match.group(1))
            letter_part = match.group(2) or ''
            return (num_part, letter_part)
        return (0, key)
    
    def _generate_exercise_latex(self, group: Dict[str, Any], display_id: str) -> str:
        """Generate LaTeX for a single exercise or group"""
        settings = group['display_settings']
        solution = group['combined_solution']
        
        latex = "\\item \n\\begin{itemize}\n"
        
        if group['id_letter']:
            # Exercise with letter (like 5a, 5b)
            latex += f"    \\item[] \\textbf{{{group['id_letter']})}} "
        else:
            # Exercise without letter  
            latex += f"    \\item[] "
        
        # Show quantity label if enabled
        if settings.get('show_quantity_label', False) and solution.get('quantity_type'):
            quantity_type = solution['quantity_type']
            # Convert to single letter format
            if quantity_type == 'Area':
                latex += "A = "
            elif quantity_type == 'Volume':
                latex += "V = "
            elif quantity_type == 'Mass':
                latex += "M = "
        
        # Show integral equation ONLY if enabled AND it's NOT a multi-part exercise
        show_equation = settings.get('show_equation', False) and not group['has_multiple_parts']
        
        if show_equation:
            integral_latex = self._get_integral_latex(group)
            if integral_latex:
                # Format the integral LaTeX properly
                formatted_integral = self._format_mathematical_expression(integral_latex)
                latex += f"$\\displaystyle {formatted_integral} = "
                
                # Add exact solution if available
                if solution.get('exact'):
                    exact_str = str(solution['exact'])
                    if '/' in exact_str:
                        parts = exact_str.split('/')
                        if len(parts) == 2:
                            numerator = self._format_mathematical_expression(parts[0])
                            denominator = self._format_mathematical_expression(parts[1])
                            latex += f"\\dfrac{{{numerator}}}{{{denominator}}}"
                        else:
                            formatted_exact = self._format_mathematical_expression(exact_str)
                            latex += formatted_exact
                    else:
                        formatted_exact = self._format_mathematical_expression(exact_str)
                        latex += formatted_exact
                
                # Add decimal solution
                if solution.get('decimal') is not None:
                    precision = settings.get('decimal_precision', 4)
                    decimal_str = f"{solution['decimal']:.{precision}f}"
                    if solution.get('exact'):
                        latex += f" = {decimal_str}"
                    else:
                        latex += decimal_str
                
                # Add units
                dimension = self._get_dimension(group['parts'][0])
                latex += f" \\ \\text{{u}}^{{{dimension}}}$"
            else:
                # Fallback to just solution if no integral
                latex += self._format_solution_only(solution, settings, group)
        else:
            # Just show solution without integral
            latex += self._format_solution_only(solution, settings, group)
        
        latex += "\n\\end{itemize}"
        
        return latex
    
    def _get_integral_latex(self, group: Dict[str, Any]) -> str:
        """Get integral LaTeX from the first part or generate it"""
        # Try to get from first part's latex field
        first_part = group['parts'][0]
        if first_part.get('latex', {}).get('integral_setup'):
            return first_part['latex']['integral_setup']
        
        # If multiple parts, try to combine or use first
        if len(group['parts']) > 1:
            # For combined exercises, use the first integral as representative
            return first_part.get('latex', {}).get('integral_setup', '')
        
        return ''
    
    def _format_solution_only(self, solution: Dict[str, Any], settings: Dict[str, Any], group: Dict[str, Any]) -> str:
        """Format just the solution without integral"""
        latex = ""
        
        if solution.get('exact') or solution.get('decimal') is not None:
            exact_str = str(solution.get('exact', ''))
            
            if exact_str and '/' in exact_str:
                # Show fraction form with \dfrac
                parts = exact_str.split('/')
                if len(parts) == 2:
                    numerator = self._format_mathematical_expression(parts[0])
                    denominator = self._format_mathematical_expression(parts[1])
                    latex += f"$\\dfrac{{{numerator}}}{{{denominator}}} = "
                else:
                    # Fallback for complex fractions
                    formatted_exact = self._format_mathematical_expression(exact_str)
                    latex += f"${formatted_exact} = "
            elif exact_str:
                formatted_exact = self._format_mathematical_expression(exact_str)
                latex += f"${formatted_exact} = "
            else:
                latex += "$"
            
            if solution.get('decimal') is not None:
                precision = settings.get('decimal_precision', 4)
                decimal_str = f"{solution['decimal']:.{precision}f}"
                latex += f"{decimal_str}"
            
            # Add units and dimension
            dimension = self._get_dimension(group['parts'][0])
            latex += f" \\ \\text{{u}}^{{{dimension}}}$"
        
        return latex
    
    def _get_dimension(self, exercise: Dict[str, Any]) -> int:
        """Get dimension based on number of integrals"""
        return len(exercise.get('integrals', []))
    
    def compile_pdf(self, tex_path: str) -> bool:
        """Compile LaTeX to PDF (requires pdflatex)"""
        try:
            # Get the directory and filename
            tex_dir = os.path.dirname(os.path.abspath(tex_path))
            tex_filename = os.path.basename(tex_path)
            
            # Run pdflatex twice for references
            for _ in range(2):
                result = subprocess.run(
                    ['pdflatex', '-interaction=nonstopmode', tex_filename],
                    capture_output=True,
                    text=True,
                    cwd=tex_dir
                )
                
                if result.returncode != 0:
                    print(f"pdflatex error: {result.stdout}")
                    print(f"pdflatex stderr: {result.stderr}")
            
            # Check if PDF was created
            pdf_path = tex_path.replace('.tex', '.pdf')
            if os.path.exists(pdf_path):
                print(f"PDF generated: {pdf_path}")
                
                # Clean up auxiliary files
                for ext in ['.aux', '.log']:
                    aux_file = tex_path.replace('.tex', ext)
                    if os.path.exists(aux_file):
                        os.remove(aux_file)
                
                return True
            else:
                print("PDF compilation failed")
                return False
                
        except FileNotFoundError:
            print("pdflatex not found. Please install LaTeX distribution.")
            return False
        except Exception as e:
            print(f"Error compiling PDF: {e}")
            return False