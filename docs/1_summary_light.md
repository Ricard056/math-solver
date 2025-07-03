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
Complex ID System and Auto-grouping
ID Structure
Input JSON uses separate fields for better clarity:

json
{
  "id": "4",
  "id_letter": null, 
  "id_part": 1,
  "type": "integral"
}
Grouping Behavior
* Intermediate JSON: Preserves ALL individual parts with complete traceability
* LaTeX Generator: Groups parts for display (4p1 + 4p2 → shows as "4")
* No ID generation: Intermediate JSON never creates combined IDs, maintains only original parts
Individual Display Settings
Settings Inheritance
* Input JSON: Global defaults in output_settings
* Intermediate JSON: Settings copied to each exercise as display_settings
* Manual Override: Individual exercises can be customized in Intermediate JSON
* LaTeX Generator: Reads individual display_settings per exercise
System Execution
Command Structure

bash
python main.py --input data/input/[specific_file].json
Processing Flow
1. Verifies specified Input JSON exists
2. Generates/overwrites Intermediate JSON (based on metadata iteration)
3. Generates .tex file (PDF compilation pending for future version)
Responsibilities by Module
main.py (Orchestrator)
* Load specified input JSON
* Generate Intermediate JSON structure with expanded metadata
* Coordinate processing of all exercises
* Save Intermediate JSON with auto-generated filename
* Call LaTeX generator
integral_solver.py (Specific Solver)
* Solve integrals mathematically (exact and decimal)
* Detect coordinate system automatically
* Determine quantity type (Area/Volume/Mass)
* Generate mathematical LaTeX code
* Calculate intermediate steps if required
latex_generator.py (Final Generator)
* Read Intermediate JSON
* Group exercise parts for display (4p1+4p2 → "4")
* Apply format configurations
* Generate complete .tex file
file_handler.py (Utilities)
* Load/save JSONs with proper error handling
* Generate filenames from metadata
* Validate data structure
* Handle Input/Intermediate JSON detection
* Copy global display settings to individual exercises

