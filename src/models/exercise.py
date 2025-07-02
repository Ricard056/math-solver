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
