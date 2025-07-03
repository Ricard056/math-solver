
# === PROJECT STRUCTURE ===
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

```
math-solver
├─ CLAUDE.md
├─ config
├─ data
│  └─ input
│     ├─ C3_2025_T16_3_integrales.json
│     └─ C3_2025_T18_3_integrales.json
├─ docs
│  ├─ 1_summary_light.md
│  └─ 2_summary_json_transformation.md
├─ GitWorkflow.md
├─ LICENSE
├─ README.md
├─ requirements.txt
├─ src
│  ├─ generators
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