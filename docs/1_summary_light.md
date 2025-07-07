# Math Solver - Automatic Math Exercise Generator

Automated Python system for generating mathematical exercises with complete solutions. Processes simple exercise definitions and produces PDFs with professionally formatted solutions.

## 🚀 Key Features

* **Automatic Resolution**: Solves integrals symbolically and numerically
* **Intelligent Detection**: Automatically identifies coordinate systems (Cartesian, polar, cylindrical, spherical)
* **Professional Format**: Generates LaTeX documents with academic formatting
* **Modular Architecture**: Designed to expand to other types of exercises
* **Batch Processing**: Handles multiple exercises in a single execution

## 📋 Requirements

* Python 3.9 or higher
* SymPy (for symbolic computation)
* LaTeX (optional, for PDF compilation)

## 🛠️ Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/math-solver.git
cd math-solver
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. (Optional) Install LaTeX for PDF compilation:
   * **Windows**: MiKTeX
   * **macOS**: MacTeX
   * **Linux**: `sudo apt-get install texlive-full`

## 💻 Usage

### Basic Command

```bash
python src/main.py --input data/input/your_file.json
```

### Workflow

1. **Create input file** in `data/input/` with exercises in JSON format
2. **Run the processor** with the command above
3. **Get results**:
   * Intermediate JSON (extended) in `data/temp/`
   * LaTeX file (.tex) in `data/output/`
   * Compiled PDF (if LaTeX is installed)

### Processing Pipeline

```
JSON Input → Python → Intermediate JSON → LaTeX Gen → .tex → PDF
(manual)     (solve)    (extended)        (format)
```

### Example Input

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
      "show_steps": false
    }
  },
  "exercises": [
    {
      "id": "1",
      "type": "integral",
      "function": "x**2 + 3*y**2",
      "integrals": [
        { "var": "y", "limits": { "lower": "1", "upper": "2" }, "order": 1 },
        { "var": "x", "limits": { "lower": "0", "upper": "2" }, "order": 2 }
      ]
    }
  ]
}
```

## 📁 Project Structure

```
math-solver/
├── data/
│   ├── input/          # Input JSONs
│   ├── output/         # Generated PDFs
│   └── temp/           # Intermediate JSONs
├── src/
│   ├── main.py         # Main orchestrator
│   ├── solvers/        # Mathematical solvers
│   ├── generators/     # LaTeX generators
│   ├── models/         # Data models
│   └── utils/          # Utilities
├── docs/               # Extended documentation
└── tests/              # Tests (pending)
```

## 🔧 Supported Exercise Types

### Currently Implemented
* ✅ **Integrals**: Single, double, triple in various coordinate systems

### In Development
* 🚧 Partial derivatives
* 🚧 Directional derivatives
* 🚧 Gradients
* 🚧 Limits
* 🚧 Series

## 🤝 Contributing

1. Fork the project
2. Create a feature branch (`git checkout -b feature/NewType`)
3. Commit your changes (`git commit -m 'Add new exercise type'`)
4. Push to the branch (`git push origin feature/NewType`)
5. Open a Pull Request

### Adding New Exercise Type

To add a new exercise type:
1. Create a new solver in `src/solvers/`
2. Extend the model in `src/models/exercise.py`
3. Update `main.py` to handle the new type
4. Add LaTeX formatting if necessary

## 📝 License

This project is under the MIT License - see the LICENSE file for more details.

## 🙏 Acknowledgments

* SymPy for the symbolic computation engine
* The Python community for incredible tools

## 📧 Contact

For questions or suggestions, please open an issue on GitHub.

# === PROJECT STRUCTURE (in development)===
# math_solver/
# ├── data/
# │   ├── input/     # Input JSONs (one per assignment)
# │   ├── output/    # Generated PDFs
# │   └── temp/      # Intermediate JSONs
# ├── src/
# │   ├── main.py                    # Main orchestrator
# │   ├── solvers/
# │   │   └── integral_solver.py     # Solves integrals
# │   ├── generators/
# │   │   └── latex_generator.py     # Generates LaTeX and PDF
# │   ├── models/
# │   │   └── exercise.py            # Data models
# │   └── utils/
# │       └── file_handler.py         # JSON file handling
