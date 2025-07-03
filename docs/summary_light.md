Project Summary: Automatic Math Exercise Generator
General Project Objective
Development of an automated Python system that generates math exercises (specifically integrals) with their complete solutions. The system processes simple exercise definitions and produces a final PDF with professionally formatted solutions.
System Architecture (3 Stages)
1. Input JSON (Manual, Minimalist)
* Purpose: Define exercises in a compact and quick-to-write format
* Characteristics: No unnecessary metadata, reusable as template
* Filling: Manual by user (teacher)
2. Processing Algorithm (Python - System Core)
* Input: Input JSON
* Automated Processes:
   * Solve integrals (exact and decimal solutions)
   * Automatically detect coordinate system (cartesian/polar/cylindrical/spherical)
   * Generate LaTeX code for formulas
   * Calculate quantity type (Area/Volume/Mass)
   * Add processing metadata
* Output: Intermediate JSON (expanded with all calculated information)
3. LaTeX Generator
* Input: Intermediate JSON
* Output: .tex file → Final PDF
* Function: Apply visual formatting, decimal rounding only for presentation
Data Flow

Input JSON → main.py → Intermediate JSON → latex_generator.py → Final PDF
Project File Structure

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
