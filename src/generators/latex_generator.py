#!/usr/bin/env python3
import subprocess
import os
from typing import Dict, Any, List, Optional
from collections import defaultdict, OrderedDict
from .latex_formatter import LaTeXFormatter

class LaTeXGenerator:
    """Generates LaTeX documents from processed exercise data"""
    
    def __init__(self):
        self.formatter = LaTeXFormatter()
    
    def generate_latex(self, data: Dict[str, Any], output_path: str) -> None:
        """Generate complete LaTeX document"""
        print(f"  Generating LaTeX file: {output_path}")
        
        try:
            # Generate document content
            latex_content = self._generate_document(data)
            
            # Write to file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(latex_content)
            
            print(f"  LaTeX file generated successfully: {output_path}")
            
        except Exception as e:
            print(f"  Error generating LaTeX: {e}")
            raise
    
    def _generate_document(self, data: Dict[str, Any]) -> str:
        """Generate the complete LaTeX document"""
        metadata = data['metadata']
        exercises = data['exercises']
        
        # Document header
        doc_parts = []
        doc_parts.append(self._generate_header(metadata))
        
        # Group and process exercises
        grouped_exercises = self._group_exercises(exercises)
        
        # Generate exercise items
        exercise_content = self._generate_exercises_section(grouped_exercises)
        doc_parts.append(exercise_content)
        
        # Document footer
        doc_parts.append(self._generate_footer())
        
        return "\n".join(doc_parts)
    
    def _generate_header(self, metadata: Dict[str, Any]) -> str:
        """Generate LaTeX document header"""
        assignment = metadata['assignment']
        
        assignment_type = assignment['type']
        assignment_number = assignment['number']
        
        title = f"{assignment_type} {assignment_number}"
        
        header = f"""\\documentclass[12pt]{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage{{amsmath}}
\\usepackage{{geometry}}
\\usepackage{{fancyhdr}}
\\usepackage{{titling}}
\\usepackage{{lmodern}}
\\geometry{{letterpaper, margin=1in}}
\\pagestyle{{fancy}}
\\fancyhf{{}}
\\rhead{{{title}}}
\\lhead{{Solucionario}}
\\cfoot{{\\thepage}}
\\setlength{{\\droptitle}}{{-4em}}
\\title{{\\textbf{{{title} \\\\[0.5em] \\large Solucionario}}}}
\\author{{}}
\\date{{}}
\\begin{{document}}
\\maketitle
\\section*{{Resultados}}
\\everymath{{\\displaystyle}}
\\setlength{{\\jot}}{{10pt}}
\\begin{{enumerate}}"""
        
        return header
    
    def _generate_footer(self) -> str:
        """Generate LaTeX document footer"""
        return "\\end{enumerate}\n\\end{document}"
    
    def _group_exercises(self, exercises: List[Dict[str, Any]]) -> OrderedDict:
        """Group exercises correctly - LA CLAVE ESTÁ AQUÍ"""
        grouped = OrderedDict()
        
        for exercise in exercises:
            base_id = exercise['id']
            id_letter = exercise.get('id_letter')
            
            # REGLA CORREGIDA: 
            # Solo agrupar por base_id (sin considerar id_letter para agrupación)
            # El id_letter se usa solo para display, no para agrupación
            group_key = base_id
            
            # Initialize group if not exists
            if group_key not in grouped:
                grouped[group_key] = {
                    'base_id': base_id,
                    'parts': []
                }
            
            # Add exercise to group
            grouped[group_key]['parts'].append(exercise)
        
        return grouped
    
    def _generate_exercises_section(self, grouped_exercises: OrderedDict) -> str:
        """Generate the exercises section"""
        items = []
        
        for group_key, group_data in grouped_exercises.items():
            item_content = self._generate_exercise_item(group_data)
            items.append(item_content)
        
        return "\n".join(items)
    
    def _generate_exercise_item(self, group_data: Dict[str, Any]) -> str:
        """Generate a single exercise item"""
        base_id = group_data['base_id']
        parts = group_data['parts']
        
        # Organizar las partes por id_letter y id_part
        organized_parts = self._organize_parts(parts)
        
        # Generar el item
        if len(organized_parts) == 1 and len(organized_parts[0]['exercises']) == 1:
            # Caso simple: un solo ejercicio
            return self._generate_single_exercise(organized_parts[0]['exercises'][0])
        else:
            # Caso complejo: multiple sub-ejercicios
            return self._generate_complex_exercise(organized_parts)
    
    def _organize_parts(self, parts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Organize parts by id_letter and id_part"""
        # Agrupar por id_letter
        letter_groups = {}
        
        for part in parts:
            id_letter = part.get('id_letter')
            key = id_letter if id_letter else 'no_letter'
            
            if key not in letter_groups:
                letter_groups[key] = []
            letter_groups[key].append(part)
        
        # Organizar cada grupo de letras
        organized = []
        for letter_key in sorted(letter_groups.keys()):
            exercises = letter_groups[letter_key]
            
            # Si el grupo tiene múltiples partes con id_part, decidir si sumar
            if len(exercises) > 1:
                # Verificar si se pueden sumar
                if self._should_sum_parts(exercises):
                    # Crear una entrada sumada
                    organized.append({
                        'id_letter': exercises[0].get('id_letter'),
                        'is_sum': True,
                        'exercises': exercises
                    })
                else:
                    # Mantener por separado
                    for ex in exercises:
                        organized.append({
                            'id_letter': ex.get('id_letter'),
                            'is_sum': False,
                            'exercises': [ex]
                        })
            else:
                # Un solo ejercicio
                organized.append({
                    'id_letter': exercises[0].get('id_letter'),
                    'is_sum': False,
                    'exercises': exercises
                })
        
        return organized
    
    def _should_sum_parts(self, parts: List[Dict[str, Any]]) -> bool:
        """Determine if parts should be summed"""
        if len(parts) <= 1:
            return False
        
        # Verificar que todas las partes tengan valores decimales válidos
        for part in parts:
            solution = part.get('solution', {})
            if solution.get('decimal') is None:
                return False
        
        # Si no tienen id_letter, siempre sumar (ej: ejercicio 4, 6)
        if not parts[0].get('id_letter'):
            return True
        
        # Si tienen id_letter, verificar si tienen mismas unidades
        first_units = parts[0].get('solution', {}).get('units')
        if not first_units:
            return False
        
        for part in parts:
            if part.get('solution', {}).get('units') != first_units:
                return False
        
        return True
    
    def _generate_single_exercise(self, exercise: Dict[str, Any]) -> str:
        """Generate a single exercise display"""
        solution = exercise.get('solution', {})
        latex_data = exercise.get('latex', {})
        
        quantity_type = solution.get('quantity_type')
        quantity_label = self.formatter.get_quantity_label(quantity_type)
        
        integral_setup = latex_data.get('integral_setup', '')
        integral_clean = self.formatter.clean_integral_setup(integral_setup)
        
        exact = solution.get('exact')
        decimal = solution.get('decimal')
        units = solution.get('units')
        precision = exercise.get('display_settings', {}).get('decimal_precision', 4)
        
        solution_display = self.formatter.format_solution_display(
            exact, decimal, units, precision
        )
        
        if integral_setup and exact and decimal is not None:
            content = f"{quantity_label} = ${integral_clean} = {solution_display}$"
        else:
            content = f"{quantity_label} = {solution_display}"
        
        return f"    \\item \n    \\begin{{itemize}}\n        \\item[] {content}\n    \\end{{itemize}}"
    
    def _generate_complex_exercise(self, organized_parts: List[Dict[str, Any]]) -> str:
        """Generate complex exercise with multiple sub-parts"""
        item_lines = []
        
        item_lines.append("    \\item ")
        item_lines.append("    \\begin{itemize}")
        
        for part_data in organized_parts:
            id_letter = part_data['id_letter']
            is_sum = part_data['is_sum']
            exercises = part_data['exercises']
            
            if is_sum:
                # Generar suma
                content = self._generate_sum_content(exercises)
                letter_label = f"[{id_letter})]" if id_letter else "[]"
                item_lines.append(f"        \\item{letter_label} {content}")
            else:
                # Generar ejercicio individual
                exercise = exercises[0]
                content = self._generate_exercise_content(exercise)
                letter_label = f"[{id_letter})]" if id_letter else "[]"
                item_lines.append(f"        \\item{letter_label} {content}")
        
        item_lines.append("    \\end{itemize}")
        
        return "\n".join(item_lines)
    
    def _generate_sum_content(self, exercises: List[Dict[str, Any]]) -> str:
        """Generate sum content for multiple exercises"""
        # Calculate sum
        total_decimal = sum(ex.get('solution', {}).get('decimal', 0) for ex in exercises)
        
        # Determine dominant quantity and units
        dominant_quantity = "Volume"
        dominant_units = "u^3"
        
        # Buscar Volume en las partes
        for ex in exercises:
            solution = ex.get('solution', {})
            if solution.get('quantity_type') == 'Volume':
                dominant_quantity = 'Volume'
                dominant_units = solution.get('units', 'u^3')
                break
        else:
            # Si no hay Volume, usar la primera parte
            first_solution = exercises[0].get('solution', {})
            dominant_quantity = first_solution.get('quantity_type', 'Volume')
            dominant_units = first_solution.get('units', 'u^3')
        
        quantity_label = self.formatter.get_quantity_label(dominant_quantity)
        precision = exercises[0].get('display_settings', {}).get('decimal_precision', 4)
        
        # Build sum expression
        decimal_values = [f"{ex.get('solution', {}).get('decimal', 0):.{precision}f}" 
                         for ex in exercises]
        sum_expression = " + ".join(decimal_values)
        total_str = f"{total_decimal:.{precision}f}"
        
        units_formatted = self.formatter._format_units(dominant_units) if dominant_units else ""
        if units_formatted:
            return f"{quantity_label} = ${sum_expression} = {total_str} \\ {units_formatted}$"
        else:
            return f"{quantity_label} = ${sum_expression} = {total_str}$"
    
    def _generate_exercise_content(self, exercise: Dict[str, Any]) -> str:
        """Generate content for a single exercise"""
        solution = exercise.get('solution', {})
        latex_data = exercise.get('latex', {})
        
        quantity_type = solution.get('quantity_type')
        quantity_label = self.formatter.get_quantity_label(quantity_type)
        
        integral_setup = latex_data.get('integral_setup', '')
        integral_clean = self.formatter.clean_integral_setup(integral_setup)
        
        exact = solution.get('exact')
        decimal = solution.get('decimal')
        units = solution.get('units')
        precision = exercise.get('display_settings', {}).get('decimal_precision', 4)
        
        solution_display = self.formatter.format_solution_display(
            exact, decimal, units, precision
        )
        
        if integral_setup and exact and decimal is not None:
            return f"{quantity_label} = ${integral_clean} = {solution_display}$"
        else:
            return f"{quantity_label} = {solution_display}"
    
    def compile_pdf(self, tex_path: str) -> None:
        """Attempt to compile LaTeX to PDF"""
        try:
            print(f"  Attempting to compile PDF from: {tex_path}")
            
            # Change to output directory
            output_dir = os.path.dirname(tex_path)
            tex_filename = os.path.basename(tex_path)
            
            # Run pdflatex
            result = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', tex_filename],
                cwd=output_dir,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                pdf_path = tex_path.replace('.tex', '.pdf')
                print(f"  PDF compiled successfully: {pdf_path}")
            else:
                print(f"  PDF compilation failed. LaTeX errors:")
                print(result.stdout[-500:])  # Show last 500 chars of output
                
        except subprocess.TimeoutExpired:
            print("  PDF compilation timed out")
        except FileNotFoundError:
            print("  pdflatex not found. Please install LaTeX to compile PDFs")
        except Exception as e:
            print(f"  PDF compilation error: {e}")