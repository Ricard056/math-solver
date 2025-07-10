# Math Solver Architecture

## System Overview

Math Solver is built on a modular pipeline architecture that processes mathematical exercises through distinct stages, each with well-defined responsibilities. The system is designed for extensibility, allowing new exercise types and output formats to be added with minimal changes to existing code.

## Data Flow Diagram

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌──────────────┐
│  Input JSON │ --> │   Parser &   │ --> │   Solver    │ --> │ Intermediate │
│    File     │     │   Validator  │     │   Engine    │     │     JSON     │
└─────────────┘     └──────────────┘     └─────────────┘     └──────┬───────┘
                                                                       │
                    ┌──────────────┐     ┌─────────────┐              │
                    │     PDF      │ <-- │    LaTeX    │ <────────────┘
                    │   Document   │     │  Generator  │
                    └──────────────┘     └─────────────┘
```

## Core Components

### 1. Orchestrator (`main.py`)

**Responsibility**: Coordinates the entire workflow and manages the pipeline execution.

**Key Functions**:
- Process command-line arguments
- Initialize all subsystem components
- Handle error propagation and recovery
- Manage file I/O through FileHandler
- Track processing statistics

**Design Pattern**: Facade Pattern - provides a simplified interface to the complex subsystem.

### 2. Data Models (`models/exercise.py`)

**Responsibility**: Define data structures that flow through the system.

**Key Classes**:
- `Exercise`: Core exercise representation
- `Integral`: Integration parameters (variable, limits, order)
- `Solution`: Computation results (exact, decimal, quantity type, units)
- `LaTeXContent`: Formatted mathematical expressions
- `ComputationDetails`: Step-by-step solution information

**Design Pattern**: Data Transfer Object (DTO) pattern for clean data passing between layers.

### 3. Solver Engine (`solvers/integral_solver.py`)

**Responsibility**: Mathematical computation and analysis.

**Key Features**:
- Coordinate system detection (Cartesian, polar, cylindrical, spherical)
- Symbolic integration using SymPy
- Quantity type determination (length, area, volume, mass)
- Unit calculation based on dimensions

**Design Decisions**:
- Uses SymPy for symbolic mathematics
- Implements heuristics for quantity detection
- Separates Jacobian detection from actual integrands

### 4. LaTeX Generation (`generators/`)

Split into two components for separation of concerns:

#### LaTeXGenerator (`latex_generator.py`)
- Document structure generation
- Exercise grouping logic
- PDF compilation interface

#### LaTeXFormatter (`latex_formatter.py`)
- Mathematical expression formatting
- Symbol conversion (Greek letters, functions)
- Fraction and exponential formatting
- Unit formatting

**Design Pattern**: Strategy Pattern for different formatting rules.

### 5. File Handler (`utils/file_handler.py`)

**Responsibility**: All file I/O operations and filename generation.

**Key Functions**:
- JSON loading/saving with error handling
- Directory structure management
- Filename generation from metadata
- Format detection (input vs intermediate JSON)

## Architectural Patterns

### 1. Pipeline Architecture

Each component processes data and passes it to the next stage:
```
Input → Parse → Solve → Format → Generate → Output
```

### 2. Separation of Concerns

- **Models**: Data representation only
- **Solvers**: Mathematical logic only
- **Generators**: Presentation logic only
- **Utils**: Cross-cutting concerns

### 3. Dependency Injection

Components receive dependencies through constructors, making testing easier:
```python
class MathSolverOrchestrator:
    def __init__(self):
        self.file_handler = FileHandler()
        self.integral_solver = IntegralSolver()
        self.latex_generator = LaTeXGenerator()
```

## Extension Points

### Adding New Exercise Types

1. **Create a new solver**:
```python
# src/solvers/derivative_solver.py
class DerivativeSolver:
    def solve_derivative(self, exercise: Exercise) -> Tuple[str, float]:
        # Implementation
```

2. **Extend the Exercise model**:
```python
@dataclass
class DerivativeExercise(Exercise):
    order: int
    point: Optional[float]
```

3. **Update the orchestrator**:
```python
def _process_exercise(self, exercise_data, settings):
    if exercise_data['type'] == 'derivative':
        return self.derivative_solver.solve(exercise_data)
```

### Adding New Output Formats

1. **Create a new generator**:
```python
# src/generators/html_generator.py
class HTMLGenerator:
    def generate_html(self, data: Dict, output_path: str):
        # Implementation
```

2. **Register in orchestrator**:
```python
self.generators = {
    'latex': LaTeXGenerator(),
    'html': HTMLGenerator()
}
```

## Key Design Decisions

### 1. Intermediate JSON

**Decision**: Generate an intermediate JSON with solutions before creating output documents.

**Rationale**:
- Enables debugging and inspection
- Allows multiple output formats from same computation
- Provides checkpointing for long computations
- Facilitates testing

### 2. Modular Solvers

**Decision**: Each mathematical domain gets its own solver module.

**Rationale**:
- Independent development and testing
- Domain-specific optimizations
- Easy to add new mathematical capabilities
- Clear separation of mathematical logic

### 3. Quantity Type Detection

**Decision**: Automatically detect what physical quantity an integral represents.

**Rationale**:
- Better user experience (no manual specification needed)
- Ensures correct units in output
- Enables domain-specific formatting

### 4. LaTeX as Primary Output

**Decision**: Generate LaTeX first, then compile to PDF.

**Rationale**:
- LaTeX provides professional mathematical typesetting
- Source files can be edited if needed
- Platform-independent document generation
- Standard in academic contexts

## Performance Considerations

### Current Optimizations

1. **Lazy Loading**: SymPy symbols created on demand
2. **Early Simplification**: Expressions simplified after each integration
3. **Caching**: Reusable LaTeX formatter instance

### Future Optimizations

1. **Parallel Processing**: Solve independent exercises concurrently
2. **Result Caching**: Cache solutions for repeated integrals
3. **Incremental Compilation**: Only recompile changed LaTeX sections

## Error Handling Strategy

### Graceful Degradation

- If an exercise fails, others continue processing
- Failed exercises get null solutions in output
- Errors collected and reported at end

### Error Categories

1. **Input Errors**: Invalid JSON, missing fields
2. **Computation Errors**: Unsolvable integrals, SymPy exceptions
3. **Output Errors**: LaTeX compilation failures
4. **System Errors**: File I/O, missing dependencies

## Testing Strategy

### Unit Tests

- Each solver method tested independently
- Model serialization/deserialization
- Formatter edge cases

### Integration Tests

- Full pipeline with sample exercises
- Various coordinate systems
- Error scenarios

### System Tests

- Complete assignments
- Performance benchmarks
- PDF output validation

## Future Architecture Enhancements

### 1. Plugin System

Allow third-party solvers:
```python
class SolverPlugin:
    def can_solve(self, exercise_type: str) -> bool
    def solve(self, exercise: Exercise) -> Solution
```

### 2. Configuration Management

External configuration for:
- Default units and precision
- LaTeX templates
- Output preferences

### 3. Async Processing

For web service deployment:
- Async exercise solving
- Progress callbacks
- Result streaming

### 4. Caching Layer

- Solution caching with hash-based keys
- LaTeX template caching
- PDF output caching