# Little Man Computer (LMC) Simulator & Compiler
A Python implementation of the Little Man Computer (LMC), including both a compiler/assembler and a machine code simulator.
This project allows you to write LMC assembly language programs, compile them to machine code, and execute them step by step with optional debugging.

# Features

## LMC Compiler
- Converts LMC assembly language source code (.asm) into 3-digit machine code.
- Supports all standard LMC instructions: ADD, SUB, STA, LDA, BRA, BRZ, BRP, INP, OUT, END/HLT.
- Handles memory allocation for DAT variables.
- Detects duplicate labels, missing operands, and invalid operands with descriptive error messages.
- Optional memory dump for debugging compiled code.

## LMC Simulator
- Executes compiled machine code files.
- Step-by-step execution mode with program counter and accumulator display.
- Input/output support for standard LMC instructions (INP, OUT).
- Prevents memory overflow and invalid opcodes.
- Robust Error Handling
- Safeguards against exceeding memory limits (100 locations).

Project Structure
LMC/
├── source_code/       # Folder for assembly (.asm) source files
├── machine_code/      # Folder where compiled machine code is saved
├── LMC.py             # Simulator (interpreter) implementation
├── Compiler.py        # LMC compiler/assembler
└── README.md          # This file

# Requirements

Python 3.10+ (uses match-case for instruction execution)
No external dependencies

# How To Use

## Compiling an LMC Program

1) Save your LMC assembly code in source_code/ (e.g., program.asm).
2) Run the compiler:

python Compiler.py program.asm --debug

--debug prints a memory dump after compilation.

3) Compiled machine code is saved in machine_code/program.asm.

## Running Machine Code

1) Run the simulator on the compiled file:

python LMC.py program.asm --step

--step enables step-by-step execution for debugging.

Normal execution runs the program and outputs results via OUT instructions.

## Example 

Example LMC Program
// Simple addition
INP
STA FIRST
INP
ADD FIRST
OUT
END

FIRST DAT 0

Compile with: python Compiler.py add.asm --debug
Run with: python LMC.py add.asm --step

# Error Handling

The compiler and simulator will raise descriptive errors for:
- Duplicate labels
- Missing operands
- Invalid operand values (not a number or undefined label)
- Exceeding memory limits
- Invalid opcode execution

# Contribution/Extensions
Add unit tests
Add more LMC instructions or extensions
Enhance debugging output

# License

MIT License. Free to use and modify.