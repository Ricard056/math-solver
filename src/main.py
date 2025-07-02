#!/usr/bin/env python3
import argparse
import sys
import time
from datetime import datetime
from typing import Dict, Any, List
from pathlib import Path

# Import project modules
from utils.file_handler import FileHandler
from models.exercise import Exercise
from solvers.integral_solver import IntegralSolver
from generators.latex_generator import LaTeXGenerator

class MathSolverOrchestrator:
    """Main orchestrator for the Math Solver system"""
    
    def __init__(self):
        self.file_handler = FileHandler()
        self.integral_solver = IntegralSolver()
        self.latex_generator = LaTeXGenerator()
        
        # Create necessary directories
        self.file_handler.create_directories()
    
    def process_assignment(self, input_path: str) -> None:
        """Process a complete assignment from input JSON"""
        print(f"Processing: {input_path}")
        start_time = time.time()
        
        try:
            # Load input JSON
            input_data = self.file_handler.load_json(input_path)
            
            # Check if it's already an intermediate JSON
            if self.file_handler.is_intermediate_json(input_data):
                print("Warning: Input appears to be an intermediate JSON")
            
            # Create intermediate JSON structure
            intermediate_data = self._create_intermediate_structure(input_data, input_path)
            
            # Process each exercise
            errors = []
            for i, exercise_data in enumerate(input_data['exercises']):
                try:
                    print(f"  Processing exercise {i+1}/{len(input_data['exercises'])}...")
                    processed_exercise = self._process_exercise(
                        exercise_data,
                        input_data['metadata']['output_settings']
                    )
                    intermediate_data['exercises'].append(processed_exercise)
                except Exception as e:
                    error_msg = f"Error in exercise {exercise_data.get('id', 'unknown')}: {str(e)}"
                    print(f"    {error_msg}")
                    errors.append(error_msg)
                    # Add exercise with null solutions
                    intermediate_data['exercises'].append(
                        self._create_empty_exercise(exercise_data, input_data['metadata']['output_settings'])
                    )
            
            # Update processing info
            processing_time = time.time() - start_time
            intermediate_data['metadata']['processing_info']['processing_time'] = f"{processing_time:.2f}s"
            intermediate_data['metadata']['processing_info']['errors'] = errors
            intermediate_data['metadata']['file_info']['processed_date'] = datetime.now().strftime('%Y-%m-%d')
            
            # Calculate exercise statistics
            self._update_exercise_statistics(intermediate_data)
            
            # Save intermediate JSON
            intermediate_filename = self.file_handler.generate_filename(
                intermediate_data['metadata'],
                'json'
            )
            intermediate_path = f"data/temp/{intermediate_filename}"
            self.file_handler.save_json(intermediate_data, intermediate_path)
            print(f"\nIntermediate JSON saved: {intermediate_path}")
            
            # Generate LaTeX
            tex_filename = self.file_handler.generate_filename(
                intermediate_data['metadata'],
                'tex'
            )
            tex_path = f"data/output/{tex_filename}"
            self.latex_generator.generate_latex(intermediate_data, tex_path)
            
            # Try to compile PDF
            self.latex_generator.compile_pdf(tex_path)
            
            print(f"\nProcessing completed in {processing_time:.2f} seconds")
            if errors:
                print(f"Encountered {len(errors)} errors during processing")
            
        except Exception as e:
            print(f"Fatal error: {e}")
            sys.exit(1)
    
    def _create_intermediate_structure(self, input_data: Dict[str, Any], input_path: str) -> Dict[str, Any]:
        """Create the intermediate JSON structure"""
        metadata = input_data['metadata'].copy()
        
        # Add file_info
        metadata['file_info'] = {
            'base_name': self.file_handler.generate_filename(metadata).replace('.json', ''),
            'source_file': Path(input_path).name,
            'generated_date': datetime.now().strftime('%Y-%m-%d'),
            'processed_date': None,
            'version': '1.0'
        }
        
        # Add processing_info
        metadata['processing_info'] = {
            'total_exercises': len(input_data['exercises']),
            'individual_exercises': 0,
            'grouped_exercises': 0,
            'exercise_types': ['integral'],
            'processing_time': None,
            'errors': []
        }
        
        return {
            'metadata': metadata,
            'exercises': []
        }
    
    def _process_exercise(self, exercise_data: Dict[str, Any], global_settings: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single exercise"""
        # Create Exercise object
        exercise = Exercise.from_dict(exercise_data)
        
        # Detect coordinate system
        variables = [integral.var for integral in exercise.integrals]
        exercise.coordinate_system = self.integral_solver.detect_coordinate_system(variables)
        
        # Solve integral
        exact_solution, decimal_solution = self.integral_solver.solve_integral(exercise)
        
        # Create solution object
        from models.exercise import Solution, LaTeXContent, ComputationDetails
        
        exercise.solution = Solution(
            exact=exact_solution,
            decimal=decimal_solution,
            quantity_type=self.integral_solver.determine_quantity_type(exercise),
            units=None  # Will be determined later if needed
        )
        
        # Generate LaTeX
        exercise.latex = LaTeXContent(
            integral_setup=self.integral_solver.generate_latex_integral(exercise),
            solution_steps=None,  # TODO: Implement step-by-step solution
            final_result=None
        )
        
        # Add computation details (placeholder)
        exercise.computation_details = ComputationDetails(
            intermediate_steps=None,
            substitutions=None,
            integration_method="symbolic"
        )
        
        # Copy display settings
        exercise.display_settings = self.file_handler.copy_display_settings(
            global_settings,
            exercise_data
        )
        
        return exercise.to_dict()
    
    def _create_empty_exercise(self, exercise_data: Dict[str, Any], global_settings: Dict[str, Any]) -> Dict[str, Any]:
        """Create exercise with null solutions for failed processing"""
        result = exercise_data.copy()
        
        # Add null fields
        result['coordinate_system'] = None
        result['solution'] = {
            'exact': None,
            'decimal': None,
            'quantity_type': None,
            'units': None
        }
        result['latex'] = {
            'integral_setup': None,
            'solution_steps': None,
            'final_result': None
        }
        result['computation_details'] = {
            'intermediate_steps': None,
            'substitutions': None,
            'integration_method': None
        }
        result['display_settings'] = self.file_handler.copy_display_settings(
            global_settings,
            exercise_data
        )
        
        return result
    
    def _update_exercise_statistics(self, data: Dict[str, Any]) -> None:
        """Update exercise statistics in processing_info"""
        exercises = data['exercises']
        
        # Count individual vs grouped
        id_counts = {}
        for ex in exercises:
            base_id = ex['id']
            if ex['id_letter']:
                base_id += ex['id_letter']
            id_counts[base_id] = id_counts.get(base_id, 0) + 1
        
        individual = sum(1 for count in id_counts.values() if count == 1)
        grouped = sum(1 for count in id_counts.values() if count > 1)
        
        data['metadata']['processing_info']['individual_exercises'] = individual
        data['metadata']['processing_info']['grouped_exercises'] = grouped

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Math Solver - Automatic Math Exercise Generator'
    )
    parser.add_argument(
        '--input',
        required=True,
        help='Path to input JSON file'
    )
    
    args = parser.parse_args()
    
    # Verify input file exists
    if not Path(args.input).exists():
        print(f"Error: Input file '{args.input}' does not exist")
        sys.exit(1)
    
    # Create orchestrator and process
    orchestrator = MathSolverOrchestrator()
    orchestrator.process_assignment(args.input)

if __name__ == '__main__':
    main()
    
    
'''
python src/main.py --input data/input/C3_2025_T18_3_integrales.json
'''
