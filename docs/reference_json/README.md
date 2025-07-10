# Reference JSON Files

This directory contains example JSON files demonstrating various features and use cases of the Math Solver system.

## Directory Structure

```
reference_json/
├── README.md                    # This file
├── basic/                       # Basic examples
│   ├── single_integral.json    # Simple single integral
│   ├── double_integral.json    # Double integral example
│   └── triple_integral.json    # Triple integral example
├── coordinate_systems/          # Different coordinate systems
│   ├── cartesian.json          # Cartesian coordinates
│   ├── polar.json              # Polar coordinates
│   ├── cylindrical.json        # Cylindrical coordinates
│   └── spherical.json          # Spherical coordinates
├── grouping/                    # Exercise grouping examples
│   ├── simple_list.json        # Basic numbered exercises
│   ├── lettered_parts.json     # Exercises with letter subdivisions
│   ├── summed_parts.json       # Parts that sum together
│   └── complex_grouping.json   # Mixed grouping patterns
├── advanced/                    # Advanced features
│   ├── variable_limits.json    # Limits as expressions
│   ├── custom_units.json       # Custom unit systems
│   ├── high_precision.json     # High decimal precision
│   └── mixed_exercises.json    # Multiple exercise types
└── templates/                   # Ready-to-use templates
    ├── homework_template.json   # Standard homework format
    ├── exam_template.json       # Exam format
    └── practice_template.json   # Practice problems
```

## Basic Examples

### single_integral.json
```json
{
  "metadata": {
    "course": {
      "name": "Calculus 2",
      "subject_area": "calculus",
      "level": 2
    },
    "assignment": {
      "type": "PRACTICE",
      "number": 1,
      "year": 2025,
      "month": 1,
      "iteration": 1
    },
    "output_settings": {
      "units": "u",
      "decimal_precision": 4
    }
  },
  "exercises": [
    {
      "id": "1",
      "type": "integral",
      "function": "x**2",
      "integrals": [
        {
          "var": "x",
          "limits": {"lower": "0", "upper": "1"},
          "order": 1
        }
      ]
    }
  ]
}
```

## Coordinate System Examples

### polar.json
Demonstrates area calculation in polar coordinates:
```json
{
  "exercises": [
    {
      "id": "1",
      "type": "integral",
      "function": "r",  // Jacobian for polar
      "integrals": [
        {"var": "r", "limits": {"lower": "0", "upper": "2"}, "order": 1},
        {"var": "theta", "limits": {"lower": "0", "upper": "pi"}, "order": 2}
      ]
    }
  ]
}
```

### spherical.json
Volume calculation with spherical coordinates:
```json
{
  "exercises": [
    {
      "id": "1",
      "type": "integral",
      "function": "rho**2*sin(phi)",  // Spherical Jacobian
      "integrals": [
        {"var": "rho", "limits": {"lower": "0", "upper": "1"}, "order": 1},
        {"var": "phi", "limits": {"lower": "0", "upper": "pi"}, "order": 2},
        {"var": "theta", "limits": {"lower": "0", "upper": "2*pi"}, "order": 3}
      ]
    }
  ]
}
```

## Grouping Examples

### lettered_parts.json
Shows how to create sub-exercises with letters:
```json
{
  "exercises": [
    {
      "id": "5",
      "id_letter": "a",
      "type": "integral",
      "function": "x*y",
      "integrals": [...]
    },
    {
      "id": "5",
      "id_letter": "b",
      "type": "integral",
      "function": "x**2",
      "integrals": [...]
    }
  ]
}
```

Output format:
```
5.
   a) Result for part a
   b) Result for part b
```

### summed_parts.json
Demonstrates automatic summation of parts:
```json
{
  "exercises": [
    {
      "id": "4",
      "id_part": 1,
      "type": "integral",
      "function": "2*r",
      "integrals": [...]
    },
    {
      "id": "4",
      "id_part": 2,
      "type": "integral",
      "function": "3*r**2",
      "integrals": [...]
    }
  ]
}
```

Output format:
```
4. V = [result1] + [result2] = [total]
```

## Advanced Features

### variable_limits.json
Integration limits as expressions:
```json
{
  "integrals": [
    {
      "var": "y",
      "limits": {
        "lower": "x**2",
        "upper": "2*x"
      },
      "order": 1
    }
  ]
}
```

### custom_units.json
Using custom measurement units:
```json
{
  "metadata": {
    "output_settings": {
      "units": "cm",
      "decimal_precision": 3
    }
  }
}
```

Results will show: `= 5.234 cm³`

## Usage Tips

### 1. Function Syntax
- Use `**` for exponents: `x**2`
- Use `*` for multiplication: `2*x`
- Use parentheses for clarity: `(x + 1)**2`
- Constants: `pi`, `e`

### 2. Common Functions
```json
"function": "sin(x)"
"function": "cos(theta)"
"function": "exp(x + y)"
"function": "sqrt(x**2 + y**2)"
"function": "x*log(y)"
```

### 3. Greek Variables
Variables automatically convert to Greek letters:
- `theta` → θ
- `phi` → φ
- `rho` → ρ

### 4. Integration Order
- Order 1 = innermost (evaluated first)
- Order 2 = middle
- Order 3 = outermost (evaluated last)

## Validation Checklist

Before processing, ensure:

1. ✓ Valid JSON syntax
2. ✓ Required metadata fields present
3. ✓ Each exercise has unique combination of (id, id_letter, id_part)
4. ✓ Integration orders are sequential (1, 2, 3...)
5. ✓ Function expressions are valid
6. ✓ Variable names are consistent

## Common Patterns

### Area of a Circle (Polar)
```json
{
  "function": "r",
  "integrals": [
    {"var": "r", "limits": {"lower": "0", "upper": "R"}, "order": 1},
    {"var": "theta", "limits": {"lower": "0", "upper": "2*pi"}, "order": 2}
  ]
}
```

### Volume of a Sphere (Spherical)
```json
{
  "function": "rho**2*sin(phi)",
  "integrals": [
    {"var": "rho", "limits": {"lower": "0", "upper": "R"}, "order": 1},
    {"var": "phi", "limits": {"lower": "0", "upper": "pi"}, "order": 2},
    {"var": "theta", "limits": {"lower": "0", "upper": "2*pi"}, "order": 3}
  ]
}
```

### Surface Integral (Cartesian)
```json
{
  "function": "sqrt(1 + (2*x)**2 + (2*y)**2)",
  "integrals": [
    {"var": "y", "limits": {"lower": "0", "upper": "1"}, "order": 1},
    {"var": "x", "limits": {"lower": "0", "upper": "1"}, "order": 2}
  ]
}
```

## Error Examples

### Invalid JSON (Don't do this)
```json
{
  "exercises": [
    {
      "id": "1"
      "type": "integral"  // Missing comma
    }
  ]
}
```

### Missing Required Fields
```json
{
  "exercises": [
    {
      "id": "1",
      // Missing "type" field
      "function": "x**2"
    }
  ]
}
```

### Invalid Expression
```json
{
  "function": "x^2"  // Should be x**2
}
```

## Quick Start Template

Copy this template to start a new assignment:

```json
{
  "metadata": {
    "course": {
      "name": "Your Course Name",
      "subject_area": "calculus",
      "level": 3
    },
    "assignment": {
      "type": "HOMEWORK",
      "number": 1,
      "year": 2025,
      "month": 1,
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
      "id_letter": null,
      "id_part": null,
      "type": "integral",
      "function": "your_function_here",
      "integrals": [
        {
          "var": "x",
          "limits": {
            "lower": "0",
            "upper": "1"
          },
          "order": 1
        }
      ]
    }
  ]
}
```