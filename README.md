# Little Man Computer (LMC) Simulator & Compiler
Python implementation of the Little Man Computer (LMC) with a full assembler and simulator, including step-by-step execution and debugging features.

# Features

## Highlights
- Full LMC compiler + simulator in Python
- Step-by-step execution with accumulator and memory view
- Input/output support (INP/OUT)
- Robust error handling for invalid instructions and memory limits
- Fully tested with unit tests for each instruction

## LMC Compiler
- Converts LMC assembly language source code (.asm) into 3-digit machine code.
- Supports all standard LMC instructions: ADD, SUB, STA, LDA, BRA, BRZ, BRP, INP, OUT, END/HLT.
- Handles memory allocation for DAT variables.
- Detects duplicate labels, missing operands, and invalid operands with descriptive error messages.
- Optional memory dump for debugging compiled code.
- Allows comments using //

### Compiler Design

The compiler uses a two-pass architecture:
1. First pass: resolve labels and assign memory addresses.
2. Second pass: encode instructions into machine code.

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
├──TestLMC.py          # Unit tests for LMC simulator
├──TestLMCCompiler.py  # Unit tests for LMC compiler
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

# Testing

This project includes comprehensive unit tests for both the compiler and simulator.

Test Coverage

Each main LMC instruction (ADD, SUB, STA, LDA, BRA, BRZ, BRP) has dedicated unit tests.

Compiler tests validate:
- Correct machine code generation
- Label resolution
- DAT memory allocation
- Error handling (duplicate labels, invalid operands, etc.)

Simulator tests validate:
- Correct instruction execution
- Program counter behavior
- Accumulator updates
- Branching logic


Test Files
TestLMC.py — Tests for the simulator
TestLMCCompiler.py — Tests for the compiler

## How To Run
Terminal

python TestLMC.py
python TestLMCCompiler.py

# Contribution/Extensions
Add unit tests
Add more LMC instructions or extensions
Enhance debugging output

# License

MIT License. Free to use and modify.