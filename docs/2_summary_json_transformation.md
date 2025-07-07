# Math Solver - Extended Technical Documentation

## Table of Contents

1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Detailed Data Flow](#detailed-data-flow)
4. [Main Components](#main-components)
5. [ID System and Grouping](#id-system-and-grouping)
6. [Extensibility and Scalability](#extensibility-and-scalability)
7. [Developer Guide](#developer-guide)
8. [Advanced Use Cases](#advanced-use-cases)

## Overview

Math Solver is a modular system designed to automate the generation of mathematical solutions. Its architecture allows easy expansion to new types of exercises while maintaining a consistent workflow.

### Design Principles

- **Modularity**: Each component has a unique and well-defined responsibility
- **Extensibility**: New exercise types can be added without modifying the core
- **Traceability**: Each data transformation is auditable
- **Reusability**: Intermediate JSONs can serve as input

## System Architecture

### 4-Stage Pipeline

```
┌─────────────┐     ┌──────────────┐     ┌────────────────┐     ┌───────────┐
│ JSON Input  │ --> │  Processing  │ --> │ Intermediate   │ --> │ LaTeX/PDF │
│  (Manual)   │     │   (Solver)   │     │ JSON (Extended)│     │   (.tex)  │
└─────────────┘     └──────────────┘     └────────────────┘     └───────────┘
```

### Detailed Flow:

1. JSON Input (manual, minimalist) →
2. main.py (solves and enriches) →
3. Intermediate JSON (with solutions and metadata) →
4. latex_generator.py (formats) →
5. .tex → PDF

### Layer Responsibilities

**Input Layer**
- Minimal exercise definitions
- Course metadata and configuration
- Simple and readable JSON format

**Processing Layer**
- Mathematical resolution (SymPy)
- Automatic property detection
- Metadata enrichment
- Intermediate JSON generation

**Output Layer**
- Professional LaTeX formatting
- Intelligent exercise grouping
- PDF compilation

## Detailed Data Flow

### 1. Loading and Validation

```python
# main.py
input_data = file_handler.load_json(input_path)
# Validates structure and detects JSON type
```

### 2. Intermediate Structure Creation

```python
intermediate_data = {
    'metadata': {
        'course': {...},
        'assignment': {...},
        'file_info': {           # NEW
            'base_name': 'C3_2025_T18_integrals_v1',
            'source_file': 'input.json',
            'generated_date': '2025-07-03'
        },
        'processing_info': {...}  # NEW
    },
    'exercises': []
}
```

### 3. Processing per Exercise

For each exercise:

**Coordinate System Detection**
```python
# Analyzes variables: {r, theta} → 'polar'
coordinate_system = solver.detect_coordinate_system(variables)
```

**Mathematical Resolution**
```python
exact_solution, decimal_solution = solver.solve_integral(exercise)
```

**LaTeX Generation**
```python
latex_setup = solver.generate_latex_integral(exercise)
```

**Configuration Copy**
```python
display_settings = copy_display_settings(global, individual)
```

### 4. Output Generation

```python
# LaTeX Generator
- Groups exercises by ID
- Applies academic formatting
- Compiles to PDF
```

## Main Components

### main.py - Orchestrator

**Responsibilities:**
- Coordinate the complete flow
- Handle errors globally
- Generate processing metadata
- Invoke specific components

**Extension Points:**
```python
if exercise['type'] == 'integral':
    solver = IntegralSolver()
elif exercise['type'] == 'derivative':  # FUTURE
    solver = DerivativeSolver()
```

### integral_solver.py - Specific Solver

**Capabilities:**
- Symbolic and numerical resolution
- Coordinate system detection
- Quantity type determination (Area/Volume/Mass)
- Mathematical LaTeX generation

**Detection Algorithm:**
```python
COORDINATE_PATTERNS = {
    'cartesian': {'x', 'y', 'z'},
    'polar': {'r', 'theta'},
    'cylindrical': {'r', 'theta', 'z'},
    'spherical': {'rho', 'theta', 'phi'}
}
```

### latex_generator.py - Document Generator

**Features:**
- Conditional formatting per exercise type
- Support for sub-items (a, b, c...)
- Optional PDF compilation

### latex_formatter.py - Expression Formatter

**Transformations:**
- ** → ^ (exponents)
- sin(x) → \sin(x) (functions)
- pi → \pi (constants)
- Spacing cleanup

## ID System and Grouping

### ID Structure

```json
{
  "id": "4",           // Base ID
  "id_letter": "a",    // Sub-group (optional)
  "id_part": 1         // Numeric part (optional)
}
```

### Grouping Logic

- **Simple Exercises**: Unique ID → Numbered item
- **Multiple Parts**: Same ID → Grouped together
- **With Letters**: 5a, 5b → Separate items with letters
- **Summable Parts**: 4p1 + 4p2 → Automatic sum if same type

### Grouping Example

**Input:** 4p1 (Area=1.13), 4p2 (Volume=4.71)
**Output:** 
```
4. 
   a) A = 1.13 u²
   b) V = 4.71 u³
```

**Input:** 6p1 (Volume=2.0), 6p2 (Volume=1.0), 6p3 (Volume=0.21)
**Output:**
```
6. V = 2.0 + 1.0 + 0.21 = 3.21 u³
```

## Extensibility and Scalability

### Current vs Future Architecture

```
Current:                          Future:
├── solvers/                     ├── solvers/
│   └── integral_solver.py       │   ├── integral_solver.py
                                │   ├── derivative_solver.py
                                │   ├── limit_solver.py
                                │   └── series_solver.py
```

### Solver Contract

Each solver must implement:
```python
class BaseSolver:
    def detect_properties(self, exercise) -> Dict
    def solve(self, exercise) -> Tuple[str, float]
    def generate_latex(self, exercise) -> str
    def determine_quantity_type(self, exercise) -> str
```

### LaTeX System Robustness

**Strengths:**
- LaTeXFormatter is generic for mathematical expressions
- LaTeXGenerator uses flexible templates
- Grouping system is independent of type

**Current Limitations:**
- Hardcoded templates for homework format
- Assumes "exercise → solution" structure

**Expansion Recommendations:**
- Create templates per exercise type
- Extend LaTeXFormatter for new notations
- Maintain formatting/generation separation

## Developer Guide

### Adding New Exercise Type

1. **Create Solver** (`src/solvers/new_solver.py`):
```python
class NewSolver:
    def solve(self, exercise):
        # Implement logic
        return exact, decimal
```

2. **Extend Model** (`src/models/exercise.py`):
```python
# Add specific fields if necessary
```

3. **Update Orchestrator** (`src/main.py`):
```python
if exercise['type'] == 'new_type':
    solver = NewSolver()
```

4. **Adjust LaTeX** (if necessary):
   - New patterns in `latex_formatter.py`
   - New templates in `latex_generator.py`

### Testing and Validation

```bash
# Recommended structure for tests
tests/
├── test_solvers/
│   ├── test_integral_solver.py
│   └── test_derivative_solver.py
├── test_generators/
└── test_integration/
```

## Advanced Use Cases

### Intermediate JSON Reuse

```bash
# First execution
python main.py --input original.json
# Generates: intermediate.json

# Manually modify intermediate.json
# Reuse as input
python main.py --input intermediate.json
```

### Selective Processing

```python
# Future: Process only certain types
python main.py --input mixed.json --types integral,derivative
```

### Variant Generation

```python
# Future: Generate multiple versions
python main.py --input base.json --variants 3
```

## Conclusions

The system is well-architected for expansion. The clear separation of responsibilities allows adding new exercise types without affecting existing components. The LaTeX system is robust enough to handle various types of mathematical notation with minimal adjustments.