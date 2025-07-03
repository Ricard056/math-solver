Requirements for Implementation
Target Environment
* Python Version: 3.9+
* Primary Dependency: SymPy for integral solving
* Output Format: LaTeX (.tex files)
Key Implementation Notes
1. Modular Design: Each module should work independently
2. Error Handling: Graceful failure for unsolvable integrals
3. Backward Compatibility: Intermediate JSON must work as Input
4. File Naming: Generated from metadata, not input filename
5. Display Settings: Copy global to individual, allow manual override

Notes: When talking to the user, do it in Spanish, but if it is about documentation or code then in English.