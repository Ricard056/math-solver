# Project Summary: Automatic Math Exercise Generator

## General Project Objective

Development of an automated Python system that generates math exercises (specifically integrals) with their complete solutions. The system processes simple exercise definitions and produces a final PDF with professionally formatted solutions.

## System Architecture (3 Stages)

### 1. **Input JSON** (Manual, Minimalist)
- **Purpose**: Define exercises in a compact and quick-to-write format
- **Characteristics**: No unnecessary metadata, reusable as template
- **Filling**: Manual by user (teacher)

### 2. **Processing Algorithm** (Python - System Core)
- **Input**: Input JSON
- **Automated Processes**:
  - Solve integrals (exact and decimal solutions)
  - Automatically detect coordinate system (cartesian/polar/cylindrical/spherical)
  - Generate LaTeX code for formulas
  - Calculate quantity type (Area/Volume/Mass)
  - Add processing metadata
- **Output**: Intermediate JSON (expanded with all calculated information)

### 3. **LaTeX Generator**
- **Input**: Intermediate JSON
- **Output**: .tex file → Final PDF
- **Function**: Apply visual formatting, decimal rounding only for presentation

## Data Flow
```
Input JSON → main.py → Intermediate JSON → latex_generator.py → Final PDF
```

## Project File Structure

```
math_solver/
├─ data/
│  ├─ input/     # Input JSONs (one per assignment)
│  ├─ output/    # Generated PDFs
│  └─ temp/      # Intermediate JSONs
├─ src/
│  ├─ main.py                    # Main orchestrator
│  ├─ solvers/
│  │  └─ integral_solver.py      # Solves integrals
│  ├─ generators/
│  │  └─ latex_generator.py      # Generates LaTeX and PDF
│  ├─ models/
│  │  └─ exercise.py             # Data models
│  └─ utils/
│     └─ file_handler.py         # JSON file handling
```

## Input JSON Structure (Simplified)

```json
{
  "metadata": {
    "course": {
      "name": "Calculo 3",
      "subject_area": "calculo",
      "level": 3
    },
    "assignment": {
      "type": "TAREA",
      "number": 20,
      "year": 2025,
      "month": 6,
      "iteration": 1
    },
    "output_settings": {
      "units": "u",
      "decimal_precision": 4,
      "show_steps": false,
      "equation_format": {
        "show_quantity_label": true,
        "show_equation": true
      }
    }
  },
  "exercises": [
    {
      "id": "1",
      "type": "integral",
      "function": "r",
      "integrals": [
        { "var": "r", "limits": { "lower": "0", "upper": "tan(theta)" }, "order": 1 },
        { "var": "theta", "limits": { "lower": "0", "upper": "pi/4" }, "order": 2 }
      ]
    }
    // ... more exercises
  ]
}
```

## Intermediate JSON Structure (Expanded)

The intermediate JSON maintains the **same base structure** as the input, but adds:

### Expanded Metadata:
- `file_info`: Automatically generated base name, processing dates
- `processing_info`: General statistics (total exercises, types, errors)

### Expanded Exercises:
Each original exercise is enriched with:
- `coordinate_system`: Automatically detected ("polar", "cartesian", "cylindrical", "spherical")
- `solution`: Exact result, decimal, quantity type, units
- `latex`: LaTeX code for setup, steps, and final result
- `computation_details`: Intermediate steps, substitutions, method used

**Key Principle**: The intermediate JSON must be **backward compatible** - if used as input, it must work.

## Responsibilities by Module

### `main.py` (Orchestrator)
- Load input JSON
- Coordinate processing of all exercises
- Generate base structure of intermediate JSON
- Invoke specific modules for each exercise
- Save intermediate JSON
- Call LaTeX generator

### `integral_solver.py` (Specific Solver)
- Solve integrals mathematically
- Detect coordinate system
- Determine quantity type (A/V/M)
- Generate mathematical LaTeX code
- Calculate intermediate steps if required

### `latex_generator.py` (Final Generator)
- Read intermediate JSON
- Apply format configurations
- Generate complete .tex file
- Compile to PDF

### `file_handler.py` (Utilities)
- Load/save JSONs
- Generate file names automatically
- Validate data structure

## Modularization Objective

Each module must be **independent and reusable**:
- `integral_solver.py` can be used alone to solve integrals
- `latex_generator.py` can generate PDFs from any valid intermediate JSON
- `main.py` orchestrates but doesn't perform direct calculations
- Extensible system for future functionalities (derivatives, limits, etc.)

## Usage Context

System developed for university professor who needs to:
- Quickly generate math exercises with solutions
- Maintain assignment history by course
- Reuse exercise definitions
- Produce professional PDFs for students

The system prioritizes **ease of manual use** in input and **complete automation** in processing.