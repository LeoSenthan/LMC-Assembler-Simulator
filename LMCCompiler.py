import sys
if len(sys.argv) != 2:
    raise ValueError("Only Arguement To Be Passed Is Source Code File Path")
else:
    filename = sys.argv[1]

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
    def __init__(self, filename):
        """
        Initializes the compiler by reading the source file,
        stripping whitespace, converting everything to uppercase,
        and removing empty lines.
        """
        with open(filename, "r") as f:
            self.instructions = []
            for line in f:
                # Convert to uppercase and remove inline comments
                line = line.split("//")[0].strip().upper()
                if line:
                    self.instructions.append(line)
        self.compiled_code = ""
        self.label_table = {}


    def parse_line(self, line):
        """
        Parses a single line into tokens, ignoring comments.
        Returns a list of tokens or an empty list for blank lines.
        """
        line = line.split("//")[0].strip()
        if not line:
            return []
        return line.split()

    def first_pass(self):
        """
        Scans instructions and records labels with their memory addresses.
        Raises error for duplicate labels.
        """
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
                        "Line {}: duplicate label '{}'".format(line_no, first_token)
                    )
                self.label_table[first_token] = current_address
                tokens = tokens[1:]  # Remove label

            if tokens:  # actual instruction or DAT
                current_address += 1


    def encode_zero_operand(self, opcode):
        """Encodes zero-operand instructions like INP, OUT, END."""
        return str(opcodes[opcode]).zfill(3)

    def encode_DAT(self, value):
        """Encodes a DAT line. Defaults to 000 if invalid."""
        if value.isdigit():
            return str(int(value)).zfill(3)
        return "000"

    def encode_opcode_operand(self, opcode, operand_token, line_no, line):
        """Encodes an instruction with an operand, resolving labels."""
        if operand_token in self.label_table:
            operand = self.label_table[operand_token]
        elif operand_token.isdigit():
            operand = int(operand_token)
        else:
            raise ValueError(
                "Line {}: '{}' unknown label or invalid operand '{}'".format(
                    line_no, line, operand_token
                )
            )
        if not (0 <= operand <= 99):
            raise ValueError(
                "Line {}: '{}' operand out of range 0-99".format(line_no, line)
            )
        return str(opcodes[opcode]) + str(operand).zfill(2)


    def second_pass(self):
        """
        Converts all instructions to 3-digit machine code.
        Supports DAT, zero-operand, and normal instructions.
        Raises errors for invalid instructions.
        """
        current_address = 0
        for line_no, line in enumerate(self.instructions):
            tokens = self.parse_line(line)
            if not tokens:
                continue

            # Remove label if present
            if tokens[0] not in opcodes:
                tokens = tokens[1:]
            if not tokens:
                continue  # label-only line

            opcode_token = tokens[0]

            # Zero-operand instructions
            if opcode_token in ["INP", "OUT", "END"]:
                compiled_line = self.encode_zero_operand(opcode_token)

            elif opcode_token == "DAT":
                value = tokens[1] if len(tokens) > 1 else "0"
                compiled_line = self.encode_DAT(value)

            # Normal opcode + operand
            else:
                if len(tokens) != 2:
                    raise ValueError(
                        "Line {}: '{}' missing operand for {}".format(line_no, line, opcode_token)
                    )
                operand_token = tokens[1]
                compiled_line = self.encode_opcode_operand(opcode_token, operand_token, line_no, line)

            # Append to compiled code
            self.compiled_code += compiled_line
            current_address += 1


    def memory_dump(self):
        """
        Prints compiled machine code in readable format.
        Each line: address | source line | compiled instruction
        """
        print("\nMemory Dump:")
        addr = 0
        for line_no, line in enumerate(self.instructions):
            tokens = self.parse_line(line)
            if not tokens:
                continue
            compiled_line = self.compiled_code[addr*3:(addr+1)*3]
            print("{:02}: {} -> {}".format(addr, line, compiled_line))
            addr += 1
        print("End of memory dump.\n")


    def write_output(self):
        """
        Writes compiled machine code to compiled_code.txt.
        """
        output_file = "compiled_code.txt"
        with open(output_file, "w") as f:
            f.write(self.compiled_code)
        print("{} instructions were successfully compiled into {}!".format(len(self.instructions), output_file))


    def compile(self):
        """
        Runs the full compilation process: first pass, second pass, output.
        """
        self.first_pass()
        self.second_pass()
        self.write_output()
        # Optional debug dump
        self.memory_dump()


compiler = Compiler(filename)
compiler.compile()