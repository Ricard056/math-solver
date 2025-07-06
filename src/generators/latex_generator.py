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
        """Group exercises by id and id_letter for proper display"""
        grouped = OrderedDict()
        
        for exercise in exercises:
            # Create grouping key
            base_id = exercise['id']
            id_letter = exercise.get('id_letter')
            
            if id_letter:
                group_key = f"{base_id}{id_letter}"
            else:
                group_key = base_id
            
            # Initialize group if not exists
            if group_key not in grouped:
                grouped[group_key] = {
                    'base_id': base_id,
                    'id_letter': id_letter,
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
        """Generate a single exercise item (may contain multiple parts)"""
        base_id = group_data['base_id']
        id_letter = group_data['id_letter']
        parts = group_data['parts']
        
        # Determine if this is a single exercise or multiple parts
        if len(parts) == 1:
            return self._generate_single_exercise(parts[0], id_letter)
        else:
            return self._generate_multi_part_exercise(base_id, id_letter, parts)
    
    def _generate_single_exercise(self, exercise: Dict[str, Any], id_letter: Optional[str]) -> str:
        """Generate a single exercise display"""
        # Get exercise data
        solution = exercise.get('solution', {})
        latex_data = exercise.get('latex', {})
        display_settings = exercise.get('display_settings', {})
        
        # Format item number
        item_format = ""
        if id_letter:
            item_format = f"[{id_letter})]"
        
        # Get quantity label
        quantity_type = solution.get('quantity_type')
        quantity_label = self.formatter.get_quantity_label(quantity_type)
        
        # Clean integral setup
        integral_setup = latex_data.get('integral_setup', '')
        integral_clean = self.formatter.clean_integral_setup(integral_setup)
        
        # Format solution
        exact = solution.get('exact')
        decimal = solution.get('decimal')
        units = display_settings.get('units', 'u')
        precision = display_settings.get('decimal_precision', 4)
        
        # Determine units based on quantity type
        units_display = self._determine_units_display(quantity_type, units)
        
        solution_display = self.formatter.format_solution_display(
            exact, decimal, units_display, precision
        )
        
        # Build the item
        if integral_setup and exact and decimal is not None:
            content = f"{quantity_label} = ${integral_clean} = {solution_display}$"
        else:
            content = f"{quantity_label} = {solution_display}"
        
        return f"    \\item {item_format}\n    \\begin{{itemize}}\n        \\item[] {content}\n    \\end{{itemize}}"
    
    def _generate_multi_part_exercise(self, base_id: str, id_letter: Optional[str], parts: List[Dict[str, Any]]) -> str:
        """Generate multi-part exercise with summed results"""
        # Check if we should sum the parts
        if self._should_sum_parts(parts):
            return self._generate_summed_exercise(base_id, id_letter, parts)
        else:
            return self._generate_individual_parts_exercise(base_id, id_letter, parts)
    
    def _should_sum_parts(self, parts: List[Dict[str, Any]]) -> bool:
        """Determine if parts should be summed or displayed individually"""
        # Sum if all parts have the same quantity type and are numerical
        if len(parts) <= 1:
            return False
        
        first_quantity = parts[0].get('solution', {}).get('quantity_type')
        if not first_quantity:
            return False
        
        # Check if all parts have same quantity type and valid decimal values
        for part in parts:
            solution = part.get('solution', {})
            if (solution.get('quantity_type') != first_quantity or 
                solution.get('decimal') is None):
                return False
        
        return True
    
    def _generate_summed_exercise(self, base_id: str, id_letter: Optional[str], parts: List[Dict[str, Any]]) -> str:
        """Generate exercise with summed parts"""
        # Calculate sum
        total_decimal = sum(part.get('solution', {}).get('decimal', 0) for part in parts)
        
        # Get quantity info from first part
        first_part = parts[0]
        quantity_type = first_part.get('solution', {}).get('quantity_type')
        quantity_label = self.formatter.get_quantity_label(quantity_type)
        
        # Get display settings
        display_settings = first_part.get('display_settings', {})
        precision = display_settings.get('decimal_precision', 4)
        units = display_settings.get('units', 'u')
        units_display = self._determine_units_display(quantity_type, units)
        
        # Build sum expression
        decimal_values = [f"{part.get('solution', {}).get('decimal', 0):.{precision}f}" 
                         for part in parts]
        sum_expression = " + ".join(decimal_values)
        total_str = f"{total_decimal:.{precision}f}"
        
        # Format item
        item_format = ""
        if id_letter:
            item_format = f"[{id_letter})]"
        
        units_formatted = self.formatter._format_units(units_display)
        content = f"{quantity_label} = ${sum_expression} = {total_str} \\ {units_formatted}$"
        
        return f"    \\item {item_format}\n    \\begin{{itemize}}\n        \\item[] {content}\n    \\end{{itemize}}"
    
    def _generate_individual_parts_exercise(self, base_id: str, id_letter: Optional[str], parts: List[Dict[str, Any]]) -> str:
        """Generate exercise with individual parts displayed"""
        item_lines = []
        
        # Generate main item
        item_format = ""
        if id_letter:
            item_format = f"[{id_letter})]"
        
        item_lines.append(f"    \\item {item_format}")
        item_lines.append("    \\begin{itemize}")
        
        # Generate each part
        for i, part in enumerate(parts):
            part_number = part.get('id_part')
            if part_number:
                # Convert to letter: 1→a, 2→b, etc.
                part_letter = chr(ord('a') + part_number - 1)
                part_label = f"[{part_letter})]"
            else:
                part_label = ""
            
            # Generate part content
            solution = part.get('solution', {})
            latex_data = part.get('latex', {})
            display_settings = part.get('display_settings', {})
            
            quantity_type = solution.get('quantity_type')
            quantity_label = self.formatter.get_quantity_label(quantity_type)
            
            integral_setup = latex_data.get('integral_setup', '')
            integral_clean = self.formatter.clean_integral_setup(integral_setup)
            
            exact = solution.get('exact')
            decimal = solution.get('decimal')
            units = display_settings.get('units', 'u')
            precision = display_settings.get('decimal_precision', 4)
            
            units_display = self._determine_units_display(quantity_type, units)
            solution_display = self.formatter.format_solution_display(
                exact, decimal, units_display, precision
            )
            
            if integral_setup and exact and decimal is not None:
                content = f"{quantity_label} = ${integral_clean} = {solution_display}$"
            else:
                content = f"{quantity_label} = {solution_display}"
            
            item_lines.append(f"        \\item{part_label} {content}")
        
        item_lines.append("    \\end{itemize}")
        
        return "\n".join(item_lines)
    
    def _determine_units_display(self, quantity_type: Optional[str], base_units: str) -> str:
        """Determine appropriate units based on quantity type"""
        if not quantity_type:
            return base_units
        
        if quantity_type == "Area":
            return f"{base_units}^2"
        elif quantity_type == "Volume":
            return f"{base_units}^3"
        elif quantity_type == "Mass":
            return base_units  # Mass units don't change
        else:
            return base_units
    
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