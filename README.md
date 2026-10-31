# Generator Project

**Status:** Paused indefinitely (cost & no actual use case) — last worked on April 16, 2026

FEMM, Python scripts, and my handwritten notes for my AC generator project. The goal was to build an AC generator, but it is currently paused indefinitely due to cost.


All the files are for simulations, going from version 2 to 5; each version is basically a redesign; the number after a dash (-) indicates smaller changes within the same version (e.g. Crappy Generator 5-3.FEM is version 5, change 3).

All Python files simulate the generator by rotating the magnets (1 degree, adjustable in code) in the FEM file and outputting the results to an Excel sheet.

## Simulation Requirements
- FEMM installed (https://www.femm.info/) — the script drives it via COM/pyfemm
- Python packages: `pip install -r requirements.txt` (pyfemm, openpyxl)
- Update the two hardcoded paths in `Crappy_Generator_5.py` (`.FEM` input line 9, `.xlsx` output line 239) to match your local setup

## Where it left off
I 3D printed the rough structure and went on Digi-Key to order materials. Turns out a spool of wire and everything else is ~$300, so I decided to put it on hold until I have more funds to finish the project.
