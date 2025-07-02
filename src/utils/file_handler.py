import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path

class FileHandler:
    """Handles JSON file operations with proper error handling"""
    
    @staticmethod
    def create_directories():
        """Create necessary directory structure"""
        dirs = ['data/input', 'data/output', 'data/temp']
        for dir_path in dirs:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    def load_json(filepath: str) -> Dict[str, Any]:
        """Load JSON file with error handling"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {filepath}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {filepath}: {e}")
    
    @staticmethod
    def save_json(data: Dict[str, Any], filepath: str) -> None:
        """Save JSON file with pretty formatting"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    @staticmethod
    def generate_filename(metadata: Dict[str, Any], extension: str = 'json') -> str:
        """Generate filename from metadata"""
        course = metadata['course']
        assignment = metadata['assignment']
        
        # C3_2025_T18_integrales_v1
        filename = f"C{course['level']}_{assignment['year']}_"
        filename += f"{assignment['type'][0]}{assignment['number']}_"
        filename += f"integrales_v{assignment['iteration']}"
        
        return f"{filename}.{extension}"
    
    @staticmethod
    def is_intermediate_json(data: Dict[str, Any]) -> bool:
        """Detect if JSON is intermediate (has file_info)"""
        return 'file_info' in data.get('metadata', {})
    
    @staticmethod
    def copy_display_settings(global_settings: Dict[str, Any], exercise: Dict[str, Any]) -> Dict[str, Any]:
        """Copy global display settings to individual exercise"""
        display_settings = {
            'units': global_settings.get('units', 'u'),
            'decimal_precision': global_settings.get('decimal_precision', 4),
            'show_steps': global_settings.get('show_steps', False)
        }
        
        if 'equation_format' in global_settings:
            display_settings.update(global_settings['equation_format'])
        
        return display_settings

# === FILE: src/models/exercise.py ===
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Union

@dataclass
class IntegralLimit:
    """Represents integration limits"""
    lower: str
    upper: str

@dataclass
class Integral:
    """Represents a single integral"""
    var: str
    limits: IntegralLimit
    order: int
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Integral':
        return cls(
            var=data['var'],
            limits=IntegralLimit(
                lower=data['limits']['lower'],
                upper=data['limits']['upper']
            ),
            order=data['order']
        )

@dataclass
class Solution:
    """Represents exercise solution"""
    exact: Optional[str] = None
    decimal: Optional[float] = None
    quantity_type: Optional[str] = None
    units: Optional[str] = None

@dataclass
class LaTeXContent:
    """LaTeX representations"""
    integral_setup: Optional[str] = None
    solution_steps: Optional[str] = None
    final_result: Optional[str] = None

@dataclass
class ComputationDetails:
    """Computation process details"""
    intermediate_steps: Optional[List[str]] = None
    substitutions: Optional[Dict[str, str]] = None
    integration_method: Optional[str] = None

@dataclass
class Exercise:
    """Represents a complete exercise"""
    id: str
    id_letter: Optional[str]
    id_part: Optional[int]
    type: str
    function: str
    integrals: List[Integral]
    coordinate_system: Optional[str] = None
    solution: Optional[Solution] = None
    latex: Optional[LaTeXContent] = None
    computation_details: Optional[ComputationDetails] = None
    display_settings: Optional[Dict[str, Any]] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Exercise':
        integrals = [Integral.from_dict(i) for i in data['integrals']]
        
        exercise = cls(
            id=data['id'],
            id_letter=data.get('id_letter'),
            id_part=data.get('id_part'),
            type=data['type'],
            function=data['function'],
            integrals=integrals
        )
        
        # Load additional fields if present (for intermediate JSON)
        if 'coordinate_system' in data:
            exercise.coordinate_system = data['coordinate_system']
        if 'solution' in data:
            exercise.solution = Solution(**data['solution'])
        if 'display_settings' in data:
            exercise.display_settings = data['display_settings']
            
        return exercise
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert exercise to dictionary"""
        result = {
            'id': self.id,
            'id_letter': self.id_letter,
            'id_part': self.id_part,
            'type': self.type,
            'function': self.function,
            'integrals': [
                {
                    'var': i.var,
                    'limits': {
                        'lower': i.limits.lower,
                        'upper': i.limits.upper
                    },
                    'order': i.order
                }
                for i in self.integrals
            ]
        }
        
        if self.coordinate_system:
            result['coordinate_system'] = self.coordinate_system
        
        if self.solution:
            result['solution'] = {
                'exact': self.solution.exact,
                'decimal': self.solution.decimal,
                'quantity_type': self.solution.quantity_type,
                'units': self.solution.units
            }
        
        if self.latex:
            result['latex'] = {
                'integral_setup': self.latex.integral_setup,
                'solution_steps': self.latex.solution_steps,
                'final_result': self.latex.final_result
            }
        
        if self.computation_details:
            result['computation_details'] = {
                'intermediate_steps': self.computation_details.intermediate_steps,
                'substitutions': self.computation_details.substitutions,
                'integration_method': self.computation_details.integration_method
            }
        
        if self.display_settings:
            result['display_settings'] = self.display_settings
            
        return result