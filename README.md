# Math Solver

A modular Python system for automatically solving mathematical exercises and generating professional solution documents. Currently specialized in integral calculus with support for multiple coordinate systems (Cartesian, polar, cylindrical, and spherical).

## 🎯 Features

- **Automatic integral solving** with symbolic computation
- **Multi-coordinate system support** (Cartesian, polar, cylindrical, spherical)
- **Intelligent quantity detection** (length, area, volume, mass)
- **Professional LaTeX output** with customizable formatting
- **PDF generation** for solution documents
- **Modular architecture** for easy extension to other mathematical domains

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Input Format](#input-format)
- [Output Format](#output-format)
- [Architecture](#architecture)
- [Contributing](#contributing)
- [License](#license)

## 🚀 Installation

### Prerequisites

- Python 3.8+
- LaTeX distribution (for PDF generation)
  - **macOS**: `brew install --cask mactex`
  - **Ubuntu/Debian**: `sudo apt-get install texlive-full`
  - **Windows**: Install [MiKTeX](https://miktex.org/)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/math-solver.git
cd math-solver
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Dependencies

- `sympy` - Symbolic mathematics
- `numpy` - Numerical computations
- Standard library modules: `json`, `pathlib`, `subprocess`, `argparse`

## 🎮 Quick Start

1. Place your input JSON file in `data/input/`
2. Run the solver:
```bash
python src/main.py --input data/input/assignment.json
```
3. Find outputs in:
   - Intermediate JSON: `data/temp/`
   - LaTeX file: `data/output/`
   - PDF file: `data/output/` (if LaTeX is installed)

## 📁 Project Structure

```
math-solver/
├── data/
│   ├── input/          # Input JSON files
│   ├── output/         # Generated LaTeX and PDF files
│   └── temp/           # Intermediate JSON files with solutions
├── src/
│   ├── main.py         # Main orchestrator
│   ├── models/
│   │   └── exercise.py # Data models (Exercise, Solution, etc.)
│   ├── solvers/
│   │   └── integral_solver.py  # Integral solving logic
│   ├── generators/
│   │   ├── latex_generator.py  # LaTeX document generation
│   │   └── latex_formatter.py  # LaTeX formatting utilities
│   └── utils/
│       └── file_handler.py     # File I/O operations
├── docs/               # Documentation
├── tests/              # Unit tests
└── requirements.txt    # Python dependencies
```

## 📖 Usage

### Basic Usage

```bash
python src/main.py --input path/to/input.json
```

### Input Format

The input JSON must follow this structure:

```json
{
  "metadata": {
    "course": {
      "name": "Calculus 3",
      "subject_area": "calculus",
      "level": 3
    },
    "assignment": {
      "type": "HOMEWORK",
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
  },
  "exercises": [
    {
      "id": "1",
      "id_letter": null,
      "id_part": null,
      "type": "integral",
      "function": "x**2 + 3*y**2",
      "integrals": [
        {
          "var": "y",
          "limits": {"lower": "1", "upper": "2"},
          "order": 1
        },
        {
          "var": "x",
          "limits": {"lower": "0", "upper": "2"},
          "order": 2
        }
      ]
    }
  ]
}
```

### Output Format

The system generates three outputs:

1. **Intermediate JSON** (in `data/temp/`): Enhanced input with solutions
2. **LaTeX file** (in `data/output/`): Professional formatting
3. **PDF file** (in `data/output/`): Final solution document

## 🏗️ Architecture

The system follows a modular pipeline architecture:

```
Input JSON → Parser → Solver → Formatter → LaTeX Generator → PDF
                         ↓
                 Intermediate JSON
```

### Key Components

- **Orchestrator** (`main.py`): Coordinates the entire workflow
- **Models** (`exercise.py`): Data structures for exercises and solutions
- **Solver** (`integral_solver.py`): Mathematical computation engine
- **Generator** (`latex_generator.py`): Document creation
- **Formatter** (`latex_formatter.py`): LaTeX syntax formatting
- **File Handler** (`file_handler.py`): I/O operations

For detailed architecture documentation, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## 🤝 Contributing

We welcome contributions! Here's how to get started:

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Run tests: `python -m pytest tests/`
5. Submit a pull request

### Adding New Exercise Types

1. Create a new solver in `src/solvers/`
2. Extend the `Exercise` model if needed
3. Update the orchestrator to handle the new type
4. Add appropriate LaTeX formatting

### Code Style

- Follow PEP 8
- Use type hints where appropriate
- Document all public methods
- Write unit tests for new features

## 📝 Example

Input exercise:
```json
{
  "function": "r",
  "integrals": [
    {"var": "r", "limits": {"lower": "0", "upper": "1"}, "order": 1},
    {"var": "theta", "limits": {"lower": "0", "upper": "2*pi"}, "order": 2}
  ]
}
```

Generated output:
```latex
A = \int_{0}^{2\pi} \int_{0}^{1} r \, dr d\theta = \pi = 3.1416 \text{u}^2
```

## 🐛 Troubleshooting

### Common Issues

1. **PDF not generating**: Ensure LaTeX is installed and `pdflatex` is in PATH
2. **Import errors**: Check all dependencies are installed
3. **Parsing errors**: Validate input JSON format

### Debug Mode

Run with verbose output:
```bash
python src/main.py --input file.json --verbose
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- SymPy community for the symbolic computation engine
- LaTeX project for document formatting capabilities

```
math-solver
├─ CLAUDE.md
├─ config
├─ data
│  └─ input
│     ├─ C3_2025_T16_3_integrales.json
│     ├─ C3_2025_T18_3_integrales.json
│     └─ C3_2025_T18_3_integrales__entrada.json
├─ docs
│  ├─ API_REFERENCE.md
│  ├─ ARQUITECTURE.md
│  ├─ DATA_FORMATS.md
│  ├─ Helpful
│  │  ├─ Claude_Suggestions.md
│  │  ├─ CONTRIBUTING.md
│  │  ├─ EXTENSION_GUIDE.md
│  │  ├─ FORMATTING_GUIDE.md
│  │  ├─ ROADMAP.md
│  │  └─ TESTING_GUIDE.md
│  ├─ JSON_TRANSFORMATION.md
│  ├─ LATEX_OUTPUT.md
│  └─ reference_json
│     ├─ C3_2025_T18_integrales.json
│     ├─ C3_2025_T18_integrales_v1.json
│     └─ README.md
├─ GitWorkflow.md
├─ LICENSE
├─ README.md
├─ requirements.txt
├─ src
│  ├─ generators
│  │  ├─ latex_formatter.py
│  │  ├─ latex_generator.py
│  │  └─ __init__.py
│  ├─ main.py
│  ├─ models
│  │  ├─ exercise.py
│  │  └─ __init__.py
│  ├─ solvers
│  │  ├─ integral_solver.py
│  │  └─ __init__.py
│  └─ utils
│     ├─ file_handler.py
│     └─ __init__.py
└─ tests
   └─ TODAVIA SIN IMPLEMENTAR.txt

```