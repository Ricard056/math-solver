Extended Project Documentation: Math Exercise Generator
Project Vision and Philosophy
Core Design Principles

Simplicity in Input: Manual JSON entry should be as straightforward as possible
Automation in Processing: Once input is provided, everything else is automatic
Modularity: Each component works independently and can be reused
Traceability: Complete history of how solutions are derived
Scalability: Easy to extend with new exercise types and features

User Experience Goals
The target user (university professor) should be able to:

Write a simple JSON with exercise definitions
Run a single command
Get a professional .tex file ready for compilation
Reuse and modify previous exercises effortlessly

Detailed Architecture Analysis
Stage 1: Input JSON Design
Philosophy: Minimize cognitive load for manual entry
The input format evolved from an even simpler structure to balance ease-of-use with functionality:
Original concept (abandoned):
json{
  "id": "1",
  "f": "x**2 + 3*y**2",
  "int1": { "var": "y", "low": "1", "up": "2" },
  "int2": { "var": "x", "low": "0", "up": "2" },
  "int3": null
}
Current design (adopted):
json{
  "id": "1",
  "id_letter": null,
  "id_part": null,
  "type": "integral",
  "function": "x**2 + 3*y**2",
  "integrals": [
    { "var": "y", "limits": { "lower": "1", "upper": "2" }, "order": 1 },
    { "var": "x", "limits": { "lower": "0", "upper": "2" }, "order": 2 }
  ]
}
Key improvements:

Separate ID components eliminate string parsing complexity
Structured integral definition supports any number of variables
Clear order specification prevents integration sequence errors

Stage 2: Processing Algorithm Deep Dive
Core Responsibilities:

Mathematical Processing: Solve integrals with exact and decimal results
System Detection: Automatically identify coordinate systems from variable patterns
Metadata Generation: Add comprehensive processing information
LaTeX Generation: Create mathematical notation for display
Error Handling: Graceful failure with detailed error reporting

Data Enrichment Process:

Original exercise data is preserved completely
New fields are added without modifying existing structure
All calculations are documented for debugging and verification
Processing metadata enables system monitoring and optimization

Stage 3: LaTeX Generator Strategy
Design Philosophy: Separation of calculation and presentation
The LaTeX generator operates on the principle that all mathematical work is complete by the time it receives the Intermediate JSON. Its responsibilities are purely presentational:
Key Operations:

Exercise Grouping: Combine related parts (4p1 + 4p2 → "4") for display
Format Application: Apply consistent styling and numbering
Decimal Rounding: Apply precision settings only for final presentation
Layout Management: Structure the document for professional appearance

Complex ID System - Detailed Analysis
Problem Statement
Academic exercises often have hierarchical relationships:

Exercise 4 has two parts that should be summed
Exercise 5a has two parts that should be summed separately from 5b
Exercise 6 has three parts with different combination rules

Solution Architecture
Input Level (optimized for manual entry):
json{ "id": "4", "id_letter": null, "id_part": 1 }
{ "id": "4", "id_letter": null, "id_part": 2 }
{ "id": "5", "id_letter": "a", "id_part": 1 }
{ "id": "5", "id_letter": "a", "id_part": 2 }
{ "id": "5", "id_letter": "b", "id_part": null }
Processing Level (maintains complete traceability):

Each part is solved independently
All intermediate steps are preserved
Relationships are maintained through ID structure

Presentation Level (groups for display):

latex_generator.py analyzes ID patterns
Combines results according to academic convention
Displays as "Exercise 4", "Exercise 5a", "Exercise 5b"

Benefits of This Approach

No ambiguous parsing: Clear field separation
Flexible grouping: Can handle any combination pattern
Complete audit trail: Every calculation step is preserved
Easy manual entry: Intuitive field structure
Future-proof: Can extend to more complex hierarchies

File Management and Naming Strategy
Academic Context
The naming convention reflects real academic workflow:
Professor's file organization:
T19_0_mecanografia.txt     # AI-generated initial content
T19_1_mecanografia         # Manually edited corrections
T19_3_JSON_de_Integrales.json  # Backup copy (rarely modified)
T19_4_resultados_integrales.txt # Old system output (now Intermediate JSON)
T19_5_latexcode.tex        # LaTeX source
T19_6_latex.pdf            # Final PDF
System mapping:
data/input/  → C3_2025_T16_3_integrales.json     # Input JSON
data/temp/   → C3_2025_T16_integrales_v1.json    # Intermediate JSON  
data/output/ → C3_2025_T16_integrales_v1.tex     # LaTeX output
Metadata-Driven Naming
Names are generated from JSON metadata, not filename parsing:
json{
  "course": { "name": "Calculo 3", "level": 3 },
  "assignment": { "type": "TAREA", "number": 16, "year": 2025, "month": 6, "iteration": 1 }
}
Generated pattern: C3_2025_T16_integrales_v1
This approach ensures:

Consistent naming regardless of input filename
Version tracking through iteration numbers
Course and assignment identification
Independence from file system paths

Display Settings Architecture
Problem: Need both global defaults and individual exercise control over display formatting.
Solution: Two-tier settings system:

Global defaults in Input JSON output_settings
Individual control via display_settings per exercise in Intermediate JSON

Workflow:
Input JSON (global) → Intermediate JSON (individual) → Manual customization → LaTeX output
Benefits:

Simplicity: Input JSON remains clean with global defaults
Flexibility: Can customize individual exercises post-processing
Backward compatibility: Works seamlessly when reusing Intermediate JSON as input
Granular control: Perfect for academic needs (show equations for some exercises, not others)

Settings Propagation Process
python# Pseudocode for settings inheritance
for exercise in exercises:
    exercise['display_settings'] = copy(global_output_settings)
    # User can manually edit specific exercises later
Design Challenge
How to make the Intermediate JSON (complex, expanded) usable as Input JSON (simple, minimal)?
Solution Strategy
Detection Logic:
pythondef detect_json_type(json_data):
    if 'file_info' in json_data.get('metadata', {}):
        return 'intermediate'
    return 'input'
Processing Adaptation:

For Input JSON: Process normally, create new Intermediate JSON
For Intermediate JSON: Extract original data, increment version, reprocess

Field Handling:

Ignore expanded fields that don't exist in Input schema
Preserve original exercise definitions
Update only metadata and processing information

Benefits

Reprocessing capability: Can refine calculations or change settings
Version control: Automatic version management
Data preservation: No loss of original exercise definitions
Workflow flexibility: Switch between input types seamlessly

Error Handling and Robustness
System Resilience

Graceful degradation: System continues processing even if individual exercises fail
Detailed error reporting: Specific error messages for debugging
Data validation: Input validation with helpful error messages
Recovery mechanisms: Partial processing with error summary

Quality Assurance

Mathematical verification: Cross-check calculations when possible
Format validation: Ensure LaTeX output is syntactically correct
Metadata consistency: Verify all generated metadata is accurate
Integration testing: End-to-end validation of complete workflow

Future Extensibility
Planned Extensions

PDF Compilation: Direct PDF generation from .tex files
Additional Exercise Types: Derivatives, limits, series
Batch Processing: Multiple input files in single run
Web Interface: Browser-based exercise definition
Template System: Predefined exercise templates

Architectural Readiness
The current design supports these extensions through:

Modular structure: New solvers can be added independently
Flexible data model: JSON structure can accommodate new exercise types
Plugin architecture: New generators can be added for different output formats
Configuration system: Settings can be extended without code changes

Performance and Scalability Considerations
Current Scope

Target load: 10-20 exercises per assignment
Processing time: Seconds per assignment
Memory usage: Minimal for typical academic workloads

Scalability Features

Streaming processing: Exercises processed independently
Caching potential: Intermediate results can be cached
Parallel processing: Natural parallelization points identified
Resource management: Minimal memory footprint design

Quality Metrics and Success Criteria
User Experience Metrics

Setup time: How quickly can a professor define new exercises?
Error rate: How often does manual input cause system failures?
Output quality: How professional is the generated LaTeX?
Workflow efficiency: How much time is saved vs. manual LaTeX writing?

Technical Metrics

Processing reliability: Percentage of exercises solved successfully
Mathematical accuracy: Verification of integral solutions
Code maintainability: Ease of adding new features
System modularity: Independence of component modules

This extended documentation provides the comprehensive context needed for full system development and future maintenance.