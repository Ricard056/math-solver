# Math Solver Data Formats

## Overview

Math Solver uses a structured JSON format for defining mathematical exercises. This document details the input JSON structure, field definitions, and configuration options.

## Input JSON Structure

The input JSON consists of two main sections: `metadata` and `exercises`.

```json
{
  "metadata": { ... },
  "exercises": [ ... ]
}
```

## Metadata Section

The metadata section contains course information, assignment details, and output settings.

### Structure

```json
"metadata": {
  "course": {
    "name": "Calculo 3",
    "subject_area": "calculo",
    "level": 3
  },
  "assignment": {
    "type": "TAREA",
    "number": 18,
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
}
```

### Field Definitions

#### course
- **name** (string): Full course name
- **subject_area** (string): Subject category (e.g., "calculo", "algebra", "geometry")
- **level** (integer): Course level/year

#### assignment
- **type** (string): Assignment type (e.g., "TAREA", "EXAMEN", "PRACTICA")
- **number** (integer): Assignment number within the course
- **year** (integer): Academic year
- **month** (integer): Month number (1-12)
- **iteration** (integer): Version number of this assignment

#### output_settings
- **units** (string): Base unit symbol (default: "u")
  - Used in output: "u", "u^2", "u^3"
  - Can be customized: "m", "cm", "ft", etc.
- **decimal_precision** (integer): Number of decimal places in numerical results
- **show_steps** (boolean): Whether to include step-by-step solutions
- **equation_format** (object):
  - **show_quantity_label** (boolean): Display quantity labels (A=, V=, etc.)
  - **show_equation** (boolean): Display the integral equation

## Exercises Section

Array of exercise objects, each representing a mathematical problem to solve.

### Exercise Structure

```json
{
  "id": "1",
  "id_letter": "a",
  "id_part": 1,
  "type": "integral",
  "function": "x**2 + 3*y**2",
  "integrals": [
    {
      "var": "y",
      "limits": {
        "lower": "1",
        "upper": "2"
      },
      "order": 1
    }
  ]
}
```

### Field Definitions

#### Core Fields
- **id** (string, required): Main exercise identifier
- **id_letter** (string, optional): Sub-exercise letter (a, b, c...)
- **id_part** (integer, optional): Sub-part number (1, 2, 3...)
- **type** (string, required): Exercise type
  - Currently supported: "integral"
  - Future: "derivative", "differential_equation", etc.

#### Function Field
- **function** (string, required): Mathematical expression to process
  - Uses Python/SymPy syntax
  - Exponents: `**` (e.g., `x**2`)
  - Multiplication: `*` (e.g., `2*x`)
  - Common functions: `sin()`, `cos()`, `exp()`, `sqrt()`
  - Constants: `pi`, `e`

#### Integrals Array
Array of integral objects defining integration variables and limits.

Each integral object contains:
- **var** (string): Integration variable
  - Cartesian: `x`, `y`, `z`
  - Polar: `r`, `theta`
  - Cylindrical: `r`, `theta`, `z`
  - Spherical: `rho`, `theta`, `phi`
- **limits** (object):
  - **lower** (string): Lower integration limit
  - **upper** (string): Upper integration limit
  - Can be constants, variables, or expressions
- **order** (integer): Integration order
  - 1 = innermost integral (evaluated first)
  - 2 = middle integral
  - 3 = outermost integral (evaluated last)

## Exercise Grouping Logic

The system uses `id`, `id_letter`, and `id_part` to organize exercises hierarchically:

### Grouping Rules

1. **Base Grouping**: All exercises with the same `id` are grouped together
2. **Letter Subdivision**: Within a group, exercises with `id_letter` create sub-items
3. **Part Aggregation**: Multiple `id_part` values can be summed if they represent components

### Examples

#### Simple Exercise
```json
{
  "id": "1",
  "id_letter": null,
  "id_part": null
}
```
Output: `1. [exercise]`

#### Exercise with Sub-items
```json
[
  {"id": "5", "id_letter": "a", "id_part": null},
  {"id": "5", "id_letter": "b", "id_part": null}
]
```
Output:
```
5. 
   a) [exercise a]
   b) [exercise b]
```

#### Exercise with Summed Parts
```json
[
  {"id": "4", "id_letter": null, "id_part": 1},
  {"id": "4", "id_letter": null, "id_part": 2}
]
```
Output: `4. V = [part1] + [part2] = [total]`

#### Complex Grouping
```json
[
  {"id": "5", "id_letter": "a", "id_part": 1},
  {"id": "5", "id_letter": "a", "id_part": 2},
  {"id": "5", "id_letter": "b", "id_part": null}
]
```
Output:
```
5.
   a) V = [part1] + [part2] = [total]
   b) [exercise b]
```

## Supported Mathematical Syntax

### Functions
- Trigonometric: `sin(x)`, `cos(x)`, `tan(x)`
- Inverse trig: `arcsin(x)`, `arccos(x)`, `arctan(x)`
- Exponential: `exp(x)`, `e**x`
- Logarithmic: `log(x)`, `ln(x)`
- Square root: `sqrt(x)`
- Hyperbolic: `sinh(x)`, `cosh(x)`, `tanh(x)`

### Constants
- Pi: `pi` or `3.14159...`
- Euler's number: `e` or `2.71828...`
- Infinity: `oo` (for limits)

### Operations
- Addition: `+`
- Subtraction: `-`
- Multiplication: `*`
- Division: `/`
- Exponentiation: `**`

### Special Syntax
- Fractions: Use division (e.g., `1/2`, `3/4`)
- Complex expressions: Use parentheses for clarity
- Greek letters in variable names: `theta`, `phi`, `rho`

## Coordinate System Detection

The system automatically detects coordinate systems based on variable names:

| Variables       | System      | Jacobian     |
|-----------------|-------------|--------------|
| x, y, z         | Cartesian   | None         |
| r, theta        | Polar       | r            |
| r, theta, z     | Cylindrical | r            |
| rho, theta, phi | Spherical   | rho²sin(phi) |

## Configuration Examples

### Basic Configuration
```json
"output_settings": {
  "units": "m",
  "decimal_precision": 2
}
```

### Detailed Configuration
```json
"output_settings": {
  "units": "cm",
  "decimal_precision": 6,
  "show_steps": true,
  "equation_format": {
    "show_quantity_label": true,
    "show_equation": true,
    "show_intermediate_results": false
  }
}
```

## Validation Rules

1. **Required Fields**:
   - metadata.course
   - metadata.assignment
   - exercises array (non-empty)
   - Each exercise must have: id, type, function

2. **Type Constraints**:
   - level, number, year, iteration: positive integers
   - decimal_precision: integer between 1-10
   - order: positive integer

3. **Logical Constraints**:
   - Integration orders must be unique within an exercise
   - Variable names must be valid identifiers
   - Functions must be parseable expressions

## Complete Example

```json
{
  "metadata": {
    "course": {
      "name": "Multivariable Calculus",
      "subject_area": "mathematics",
      "level": 3
    },
    "assignment": {
      "type": "HOMEWORK",
      "number": 5,
      "year": 2025,
      "month": 3,
      "iteration": 2
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
      "id_letter": null,
      "id_part": null,
      "type": "integral",
      "function": "x*y",
      "integrals": [
        {
          "var": "y",
          "limits": {"lower": "0", "upper": "x"},
          "order": 1
        },
        {
          "var": "x",
          "limits": {"lower": "0", "upper": "1"},
          "order": 2
        }
      ]
    },
    {
      "id": "2",
      "id_letter": "a",
      "id_part": null,
      "type": "integral",
      "function": "r",
      "integrals": [
        {
          "var": "r",
          "limits": {"lower": "0", "upper": "2"},
          "order": 1
        },
        {
          "var": "theta",
          "limits": {"lower": "0", "upper": "pi"},
          "order": 2
        }
      ]
    }
  ]
}
```