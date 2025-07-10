# Math Solver API Reference

## Table of Contents

- [Core Classes](#core-classes)
  - [MathSolverOrchestrator](#mathsolverorchestrator)
  - [Exercise](#exercise)
  - [IntegralSolver](#integralsolver)
  - [LaTeXGenerator](#latexgenerator)
  - [FileHandler](#filehandler)
- [Data Models](#data-models)
- [Utility Functions](#utility-functions)

## Core Classes

### MathSolverOrchestrator

Main orchestrator that coordinates the entire solving workflow.

```python
class MathSolverOrchestrator:
    def __init__(self)
```

#### Methods

##### `process_assignment(input_path: str) -> None`

Process a complete assignment from input JSON file.

**Parameters:**
- `input_path` (str): Path to the input JSON file

**Example:**
```python
orchestrator = MathSolverOrchestrator()
orchestrator.process_assignment("data/input/homework.json")
```

**Raises:**
- `FileNotFoundError`: If input file doesn't exist
- `ValueError`: If JSON is invalid
- `SystemExit`: On fatal errors

### Exercise

Core data model representing a mathematical exercise.

```python
@dataclass
class Exercise:
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
```

#### Class Methods

##### `from_dict(data: Dict[str, Any]) -> Exercise`

Create an Exercise instance from a dictionary.

**Parameters:**
- `data` (Dict): Dictionary containing exercise data

**Returns:**
- `Exercise`: New Exercise instance

**Example:**
```python
exercise_data = {
    "id": "1",
    "type": "integral",
    "function": "x**2",
    "integrals": [
        {"var": "x", "limits": {"lower": "0", "upper": "1"}, "order": 1}
    ]
}
exercise = Exercise.from_dict(exercise_data)
```

##### `to_dict() -> Dict[str, Any]`

Convert exercise to dictionary representation.

**Returns:**
- `Dict`: Dictionary representation of the exercise

### IntegralSolver

Solves integrals with automatic coordinate system detection.

```python
class IntegralSolver:
    def __init__(self)
```

#### Methods

##### `detect_coordinate_system(variables: List[str]) -> str`

Auto-detect coordinate system from variable names.

**Parameters:**
- `variables` (List[str]): List of variable names

**Returns:**
- `str`: Coordinate system ('cartesian', 'polar', 'cylindrical', 'spherical')

**Example:**
```python
solver = IntegralSolver()
system = solver.detect_coordinate_system(['r', 'theta'])  # Returns 'polar'
```

##### `solve_integral(exercise: Exercise) -> Tuple[Optional[str], Optional[float]]`

Solve the integral and return exact and decimal solutions.

**Parameters:**
- `exercise` (Exercise): Exercise to solve

**Returns:**
- `Tuple[Optional[str], Optional[float]]`: (exact_solution, decimal_solution)

**Example:**
```python
solver = IntegralSolver()
exact, decimal = solver.solve_integral(exercise)
# exact = "pi/4", decimal = 0.7853981633974483
```

##### `get_quantity_and_units(exercise: Exercise, base_unit: str = "u") -> Tuple[Optional[str], Optional[str]]`

Determine quantity type and units based on integral properties.

**Parameters:**
- `exercise` (Exercise): Exercise to analyze
- `base_unit` (str): Base unit symbol (default: "u")

**Returns:**
- `Tuple[Optional[str], Optional[str]]`: (quantity_type, units)

**Example:**
```python
quantity, units = solver.get_quantity_and_units(exercise, "m")
# quantity = "Volume", units = "m^3"
```

##### `generate_latex_integral(exercise: Exercise) -> str`

Generate LaTeX code for the integral setup.

**Parameters:**
- `exercise` (Exercise): Exercise to format

**Returns:**
- `str`: LaTeX representation of the integral

**Example:**
```python
latex = solver.generate_latex_integral(exercise)
# Returns: "\\int_{0}^{1} x^2 \\, dx"
```

### LaTeXGenerator

Generates LaTeX documents from processed exercise data.

```python
class LaTeXGenerator:
    def __init__(self)
```

#### Methods

##### `generate_latex(data: Dict[str, Any], output_path: str) -> None`

Generate complete LaTeX document.

**Parameters:**
- `data` (Dict): Intermediate JSON data with solutions
- `output_path` (str): Path for output LaTeX file

**Example:**
```python
generator = LaTeXGenerator()
generator.generate_latex(intermediate_data, "output/solutions.tex")
```

##### `compile_pdf(tex_path: str) -> None`

Compile LaTeX file to PDF using pdflatex.

**Parameters:**
- `tex_path` (str): Path to LaTeX file

**Example:**
```python
generator.compile_pdf("output/solutions.tex")
# Creates: output/solutions.pdf
```

### FileHandler

Handles all file I/O operations.

```python
class FileHandler:
    @staticmethod
    def create_directories()
    
    @staticmethod
    def load_json(filepath: str) -> Dict[str, Any]
    
    @staticmethod
    def save_json(data: Dict[str, Any], filepath: str) -> None
    
    @staticmethod
    def generate_filename(metadata: Dict[str, Any], extension: str = 'json') -> str
```

#### Methods

##### `load_json(filepath: str) -> Dict[str, Any]`

Load and parse JSON file.

**Parameters:**
- `filepath` (str): Path to JSON file

**Returns:**
- `Dict`: Parsed JSON data

**Raises:**
- `FileNotFoundError`: If file doesn't exist
- `ValueError`: If JSON is invalid

**Example:**
```python
data = FileHandler.load_json("input/exercises.json")
```

##### `generate_filename(metadata: Dict[str, Any], extension: str = 'json') -> str`

Generate standardized filename from metadata.

**Parameters:**
- `metadata` (Dict): Metadata containing course and assignment info
- `extension` (str): File extension (default: 'json')

**Returns:**
- `str`: Generated filename

**Example:**
```python
metadata = {
    "course": {"level": 3},
    "assignment": {"year": 2025, "type": "TAREA", "number": 18, "iteration": 1}
}
filename = FileHandler.generate_filename(metadata, 'tex')
# Returns: "C3_2025_T18_integrales_v1.tex"
```

## Data Models

### Integral

```python
@dataclass
class Integral:
    var: str                    # Integration variable
    limits: IntegralLimit      # Integration limits
    order: int                 # Order of integration (1 = innermost)
```

### IntegralLimit

```python
@dataclass
class IntegralLimit:
    lower: str                 # Lower limit expression
    upper: str                 # Upper limit expression
```

### Solution

```python
@dataclass
class Solution:
    exact: Optional[str] = None       # Exact symbolic solution
    decimal: Optional[float] = None   # Decimal approximation
    quantity_type: Optional[str] = None  # Physical quantity (Area, Volume, etc.)
    units: Optional[str] = None       # Units with proper exponent
```

### LaTeXContent

```python
@dataclass
class LaTeXContent:
    integral_setup: Optional[str] = None    # LaTeX for integral
    solution_steps: Optional[str] = None    # Step-by-step solution
    final_result: Optional[str] = None      # Final formatted result
```

## Utility Functions

### LaTeXFormatter

Utility class for LaTeX formatting operations.

#### Key Methods

##### `clean_integral_setup(integral_setup_str: str) -> str`

Clean and format integral LaTeX string.

**Example:**
```python
formatter = LaTeXFormatter()
clean = formatter.clean_integral_setup("\\int_{0}^{pi} sin(x) dx")
# Returns: "\\int_{0}^{\\pi} \\sin(x) dx"
```

##### `format_solution_display(exact: str, decimal: float, units: str, precision: int) -> str`

Format complete solution display.

**Example:**
```python
display = formatter.format_solution_display("pi/4", 0.7854, "m^2", 4)
# Returns: "\\dfrac{\\pi}{4} = 0.7854 \\ \\text{m}^{2}"
```

## Usage Examples

### Complete Example: Processing an Assignment

```python
from pathlib import Path
from src.main import MathSolverOrchestrator

# Create input file
input_data = {
    "metadata": {
        "course": {"name": "Calculus 3", "level": 3},
        "assignment": {"type": "HOMEWORK", "number": 1, "year": 2025, "iteration": 1},
        "output_settings": {"units": "u", "decimal_precision": 4}
    },
    "exercises": [{
        "id": "1",
        "type": "integral", 
        "function": "x**2",
        "integrals": [{"var": "x", "limits": {"lower": "0", "upper": "1"}, "order": 1}]
    }]
}

# Save input
Path("data/input").mkdir(exist_ok=True)
with open("data/input/test.json", "w") as f:
    json.dump(input_data, f)

# Process
orchestrator = MathSolverOrchestrator()
orchestrator.process_assignment("data/input/test.json")

# Results available in:
# - data/temp/C3_2025_H1_integrales_v1.json (solutions)
# - data/output/C3_2025_H1_integrales_v1.tex (LaTeX)
# - data/output/C3_2025_H1_integrales_v1.pdf (if pdflatex available)
```

### Example: Direct Solver Usage

```python
from src.solvers.integral_solver import IntegralSolver
from src.models.exercise import Exercise, Integral, IntegralLimit

# Create exercise
integral = Integral(
    var='x',
    limits=IntegralLimit(lower='0', upper='pi'),
    order=1
)
exercise = Exercise(
    id='1',
    type='integral',
    function='sin(x)',
    integrals=[integral]
)

# Solve
solver = IntegralSolver()
exercise.coordinate_system = solver.detect_coordinate_system(['x'])
exact, decimal = solver.solve_integral(exercise)
quantity, units = solver.get_quantity_and_units(exercise)

print(f"Result: {exact} = {decimal:.4f} {units}")
# Output: Result: 2 = 2.0000 u^2
```

## Error Handling

All methods follow consistent error handling patterns:

1. **Input Validation**: Check parameters before processing
2. **Graceful Degradation**: Return None/empty for non-fatal errors
3. **Error Propagation**: Raise exceptions for fatal errors
4. **Error Collection**: Accumulate errors for batch reporting

Example error handling:
```python
try:
    data = FileHandler.load_json("missing.json")
except FileNotFoundError:
    print("File not found")
except ValueError as e:
    print(f"Invalid JSON: {e}")
```