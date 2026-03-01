import argparse

# LMC Opcodes mapping
opcodes = {
    "LDA": 5,
    "STA": 3,
    "ADD": 1,
    "SUB": 2,
    "INP": 901,
    "OUT": 902,
    "END": 0,
    "BRA": 6,
    "BRZ": 7,
    "BRP": 8,
    "DAT": -1  # handled specially
}

class Compiler:
    """A simple Little Man Computer (LMC) assembler/compiler.

    Converts LMC assembly language source code into 3-digit machine code.
    
    Attributes:
        filename (str): Source code filename.
        debug (bool): If True, prints memory dump after compilation.
        instructions (list[str]): List of parsed source code lines.
        compiled_code (str): Concatenated 3-digit machine code instructions.
        label_table (dict): Maps labels to memory addresses.
    """

    def __init__(self, filename: str, debug: bool = False):
        """Initializes the compiler, reads the source file, cleans and stores lines."""
        self.filename = filename
        self.debug = debug
        try:
            with open(f"source_code/{self.filename}", "r") as f:
                self.instructions = []
                for line in f:
                    line = line.split("//")[0].strip().upper()  # Remove comments & uppercase
                    if line:
                        self.instructions.append(line)
        except FileNotFoundError:
            raise FileNotFoundError(f"Source file '{self.filename}' not found in 'source_code/' directory.")
        self.compiled_code = ""
        self.label_table = {}

    def parse_line(self, line: str) -> list[str]:
        """Parses a line into tokens, ignoring comments and empty lines."""
        line = line.split("//")[0].strip()
        return line.split() if line else []

    def first_pass(self):
        """Scans instructions and records labels with memory addresses. Raises error for duplicates."""
        current_address = 0
        for line_no, line in enumerate(self.instructions):
            tokens = self.parse_line(line)
            if not tokens:
                continue
            first_token = tokens[0]
            if first_token not in opcodes:
                # Treat as label
                if first_token in self.label_table:
                    raise ValueError(
                        f"Line {line_no}: duplicate label '{first_token}' already defined at address {self.label_table[first_token]}"
                    )
                self.label_table[first_token] = current_address
                tokens = tokens[1:]  # Remove label
            if tokens:  # Only increment if actual instruction
                current_address += 1

    def encode_zero_operand(self, opcode: str) -> str:
        """Encodes zero-operand instructions like INP, OUT, END."""
        return str(opcodes[opcode]).zfill(3)

    def encode_DAT(self, value: str) -> str:
        """Encodes DAT line; defaults to 000 if invalid."""
        if not value.isdigit():
            print(f"Warning: DAT value '{value}' invalid, defaulting to 000.")
        return str(int(value)).zfill(3) if value.isdigit() else "000"

    def encode_opcode_operand(self, opcode: str, operand_token: str, line_no: int, line: str) -> str:
        """Encodes instruction with an operand, resolving labels."""
        if operand_token in self.label_table:
            operand = self.label_table[operand_token]
        elif operand_token.isdigit():
            operand = int(operand_token)
        else:
            raise ValueError(
                f"Line {line_no}: Operand '{operand_token}' in '{line}' is not a number or a defined label. "
                "Ensure the label exists or use a numeric operand (0-99)."
            )
        if not (0 <= operand <= 99):
            raise ValueError(f"Line {line_no}: Operand '{operand}' in '{line}' is out of range 0–99.")
        return str(opcodes[opcode]) + str(operand).zfill(2)

    def second_pass(self):
        """Converts all instructions to 3-digit machine code, handles DAT, zero-operand, and normal instructions."""
        current_address = 0
        for line_no, line in enumerate(self.instructions):
            tokens = self.parse_line(line)
            if not tokens:
                continue

            # Remove label if present
            if tokens[0] not in opcodes:
                tokens = tokens[1:]
            if not tokens:
                continue

            opcode_token = tokens[0]

            if opcode_token in ["INP", "OUT", "END"]:
                compiled_line = self.encode_zero_operand(opcode_token)
            elif opcode_token == "DAT":
                value = tokens[1] if len(tokens) > 1 else "0"
                compiled_line = self.encode_DAT(value)
            else:
                if len(tokens) != 2:
                    raise ValueError(f"Line {line_no}: '{line}' missing operand for {opcode_token}")
                operand_token = tokens[1]
                compiled_line = self.encode_opcode_operand(opcode_token, operand_token, line_no, line)

            self.compiled_code += compiled_line
            current_address += 1

    def memory_dump(self):
        """Prints compiled machine code in readable format with line numbers and labels."""
        print("\nMemory Dump:")
        addr = 0
        for line_no, line in enumerate(self.instructions):
            tokens = self.parse_line(line)
            if not tokens:
                continue
            compiled_line = self.compiled_code[addr*3:(addr+1)*3]
            # Add label info if present
            label_info = ""
            if tokens[0] not in opcodes:
                label_info = f"(Label: {tokens[0]}) "
            print(f"{addr:02}: {label_info}{line} -> {compiled_line}")
            addr += 1
        print("End of memory dump.\n")

    def write_output(self):
        """Writes compiled machine code to 'machine_code/filename'."""
        with open(f"machine_code/{self.filename}", "w") as f:
            f.write(self.compiled_code)
        print(f"{len(self.instructions)} instructions were successfully compiled into 'machine_code/{self.filename}'!")

    def compile(self):
        """Runs the full compilation process: first pass, second pass, output, and optional memory dump."""
        self.first_pass()
        self.second_pass()
        self.write_output()
        if self.debug:
            self.memory_dump()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compile LMC source code into machine code.")
    parser.add_argument("filename", help="LMC source file (from 'source_code/' directory)")
    parser.add_argument("--debug", action="store_true", help="Print memory dump after compilation")
    args = parser.parse_args()
    compiler = Compiler(args.filename, debug=args.debug)
    compiler.compile()