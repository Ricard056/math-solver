import os
import subprocess
from typing import Dict, Any, List
from pathlib import Path

class LaTeXGenerator:
    """Generates LaTeX files and PDFs from intermediate JSON"""
    
    def __init__(self):
        self.template = self._load_template()
    
    def _load_template(self) -> str:
        """Load LaTeX document template"""
        return r"""
\documentclass[12pt,letterpaper]{article}
\usepackage[utf8]{inputenc}
\usepackage[spanish]{babel}
\usepackage{amsmath,amssymb}
\usepackage{geometry}
\geometry{left=2cm,right=2cm,top=2.5cm,bottom=2.5cm}

\title{<<TITLE>>}
\author{<<COURSE>>}
\date{<<DATE>>}

\begin{document}
\maketitle

\section*{Ejercicios}

<<EXERCISES>>

\end{document}
"""
    
    def generate_latex(self, data: Dict[str, Any], output_path: str) -> None:
        """Generate LaTeX file from intermediate JSON"""
        # Extract metadata
        metadata = data['metadata']
        course = metadata['course']
        assignment = metadata['assignment']
        
        # Prepare title
        title = f"{assignment['type']} {assignment['number']} - Integrales"
        course_name = f"{course['name']} - {assignment['year']}"
        date = f"{self._month_name(assignment['month'])} {assignment['year']}"
        
        # Group exercises by ID
        grouped_exercises = self._group_exercises(data['exercises'])
        
        # Generate exercise content
        exercises_latex = self._generate_exercises_latex(grouped_exercises)
        
        # Fill template
        latex_content = self.template
        latex_content = latex_content.replace('<<TITLE>>', title)
        latex_content = latex_content.replace('<<COURSE>>', course_name)
        latex_content = latex_content.replace('<<DATE>>', date)
        latex_content = latex_content.replace('<<EXERCISES>>', exercises_latex)
        
        # Save LaTeX file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(latex_content)
        
        print(f"LaTeX file generated: {output_path}")
    
    def _group_exercises(self, exercises: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Group exercises by ID for display"""
        groups = {}
        
        for exercise in exercises:
            # Create group key
            key = exercise['id']
            if exercise['id_letter']:
                key += exercise['id_letter']
            
            if key not in groups:
                groups[key] = []
            groups[key].append(exercise)
        
        return groups
    
    def _generate_exercises_latex(self, grouped_exercises: Dict[str, List[Dict[str, Any]]]) -> str:
        """Generate LaTeX for all exercises"""
        latex_parts = []
        
        for group_id, exercises in sorted(grouped_exercises.items()):
            if len(exercises) == 1:
                # Single exercise
                latex_parts.append(self._generate_single_exercise(exercises[0], group_id))
            else:
                # Multiple parts
                latex_parts.append(self._generate_multi_part_exercise(exercises, group_id))
        
        return '\n\n'.join(latex_parts)
    
    def _generate_single_exercise(self, exercise: Dict[str, Any], display_id: str) -> str:
        """Generate LaTeX for a single exercise"""
        latex = f"\\subsection*{{Ejercicio {display_id}}}\n\n"
        
        settings = exercise.get('display_settings', {})
        
        if settings.get('show_equation', True):
            # Get LaTeX integral or generate it
            integral_latex = exercise.get('latex', {}).get('integral_setup')
            if not integral_latex:
                # Generate basic integral display
                integral_latex = self._generate_integral_display(exercise)
            
            if settings.get('show_quantity_label', True) and exercise.get('solution', {}).get('quantity_type'):
                latex += f"{exercise['solution']['quantity_type']} = "
            
            latex += f"$${integral_latex}$$\n\n"
        
        # Add solution
        solution = exercise.get('solution', {})
        if solution.get('exact') or solution.get('decimal'):
            latex += "\\textbf{Solución:} "
            
            if solution.get('exact'):
                latex += f"${solution['exact']}$"
            
            if solution.get('decimal'):
                precision = settings.get('decimal_precision', 4)
                decimal_str = f"{solution['decimal']:.{precision}f}"
                latex += f" $\\approx {decimal_str}$"
            
            if settings.get('units'):
                latex += f" {settings['units']}$^{self._get_dimension(exercise)}$"
            
            latex += "\n"
        
        return latex
    
    def _generate_multi_part_exercise(self, exercises: List[Dict[str, Any]], group_id: str) -> str:
        """Generate LaTeX for multi-part exercise"""
        latex = f"\\subsection*{{Ejercicio {group_id}}}\n\n"
        
        for i, exercise in enumerate(exercises):
            part_letter = chr(ord('a') + i)
            latex += f"\\textbf{{Parte {part_letter})}}\n\n"
            
            # Use same logic as single exercise but without subsection
            settings = exercise.get('display_settings', {})
            
            if settings.get('show_equation', True):
                integral_latex = exercise.get('latex', {}).get('integral_setup')
                if not integral_latex:
                    integral_latex = self._generate_integral_display(exercise)
                
                if settings.get('show_quantity_label', True) and exercise.get('solution', {}).get('quantity_type'):
                    latex += f"{exercise['solution']['quantity_type']} = "
                
                latex += f"$${integral_latex}$$\n\n"
            
            # Add solution
            solution = exercise.get('solution', {})
            if solution.get('exact') or solution.get('decimal'):
                latex += "Solución: "
                
                if solution.get('exact'):
                    latex += f"${solution['exact']}$"
                
                if solution.get('decimal'):
                    precision = settings.get('decimal_precision', 4)
                    decimal_str = f"{solution['decimal']:.{precision}f}"
                    latex += f" $\\approx {decimal_str}$"
                
                if settings.get('units'):
                    latex += f" {settings['units']}$^{self._get_dimension(exercise)}$"
                
                latex += "\n\n"
        
        return latex
    
    def _generate_integral_display(self, exercise: Dict[str, Any]) -> str:
        """Generate basic integral display"""
        sorted_integrals = sorted(exercise['integrals'], key=lambda x: -x['order'])
        
        latex = ""
        for integral in sorted_integrals:
            latex += f"\\int_{{{integral['limits']['lower']}}}^{{{integral['limits']['upper']}}} "
        
        function_latex = exercise['function'].replace('**', '^').replace('*', '\\cdot ')
        latex += f"{function_latex} \\, "
        
        for integral in sorted(exercise['integrals'], key=lambda x: x['order']):
            latex += f"d{integral['var']} "
        
        return latex.strip()
    
    def _get_dimension(self, exercise: Dict[str, Any]) -> int:
        """Get dimension based on number of integrals"""
        return len(exercise['integrals'])
    
    def _month_name(self, month: int) -> str:
        """Convert month number to Spanish name"""
        months = {
            1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
            5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
            9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
        }
        return months.get(month, "")
    
    def compile_pdf(self, tex_path: str) -> bool:
        """Compile LaTeX to PDF (requires pdflatex)"""
        try:
            # Run pdflatex twice for references
            for _ in range(2):
                result = subprocess.run(
                    ['pdflatex', '-interaction=nonstopmode', tex_path],
                    capture_output=True,
                    text=True,
                    cwd=os.path.dirname(tex_path)
                )
            
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
