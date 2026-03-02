from enum import Enum
import argparse


class Opcode(Enum):
    ADD = 1
    SUB = 2
    STA = 3
    LDA = 5
    BRA = 6
    BRZ = 7
    BRP = 8
    INP = 901
    OUT = 902
    HLT = 0


class LMC:
    """A simulator for the Little Man Computer (LMC).

    Attributes:
        memory (list[int]): 100 memory locations initialized to 0.
        filename (str): The file containing machine code to execute.
        step (bool): If True, enables step-by-step debugging output.
        PC (int): Program Counter, points to the current instruction.
        ACC (int): Accumulator register.
        running (bool): Flag to control execution loop.
    """

    def __init__(self, filename: str, step: bool = False, dump: bool = False):
        """Initializes the LMC simulator.

        Args:
            filename (str): Name of the machine code file to execute.
            step (bool): If True, enables step-by-step execution for debugging.
        """
        self.memory = [0] * 100
        self.filename = filename
        self.step = step
        self.dump = dump
        self.load_program()

    def load_program(self):
        """Loads the machine code from the file into memory.

        Raises:
            FileNotFoundError: If the machine code file does not exist.
            ValueError: If the program exceeds 100 memory locations.
        """
        try:
            with open("machine_code/" + self.filename, "r") as f:
                data = f.read().strip()
        except FileNotFoundError:
            raise FileNotFoundError(f"Machine code file '{self.filename}' was not found in 'machine_code/' directory.")

        instructions = [int(data[i:i + 3]) for i in range(0, len(data), 3)]
        if len(instructions) > 100:
            raise ValueError(f"Program exceeds 100 memory locations ({len(instructions)}).")
        for i, instr in enumerate(instructions):
            self.memory[i] = instr

    def run(self):
        """Runs the LMC program from memory.

        Continuously fetches, decodes, and executes instructions
        until a HLT instruction is encountered.
        """
        self.PC = 0
        self.ACC = 0
        self.running = True

        while self.running:
            instruction = self.memory[self.PC]
            self.PC += 1
            self.decode_execute(instruction)
        
        if self.dump:
            self.memory_dump()

    def decode_execute(self, instruction: int):
        """Decodes a single instruction and executes it.

        Args:
            instruction (int): The 3-digit instruction code.

        Raises:
            ValueError: If the instruction contains an invalid opcode.
        """
        if instruction in (901, 902, 0):
            opcode = Opcode(instruction)
            operand = 0
        else:
            try:
                opcode = Opcode(instruction // 100)
            except ValueError:
                raise ValueError(f"Invalid opcode at memory address {self.PC - 1}: {instruction}")
            operand = instruction % 100

        if self.step:
            current_pc = self.PC - 1
            print(f"DEBUG: PC-{current_pc} ACC-{self.ACC} CURRENT INSTRUCTION {instruction}")
            input("Press Enter to continue...")

        self.execute(opcode, operand)

    def execute(self, opcode: Opcode, operand: int):
        """Executes a single decoded instruction.

        Args:
            opcode (Opcode): The operation code to execute.
            operand (int): The memory address used by the instruction (if applicable).
        """
        match opcode:
            case Opcode.LDA:
                self.ACC = self.memory[operand]

            case Opcode.STA:
                self.memory[operand] = self.ACC

            case Opcode.ADD:
                self.ACC = (self.ACC + self.memory[operand]) % 1000

            case Opcode.SUB:
                self.ACC = (self.ACC - self.memory[operand]) % 1000

            case Opcode.INP:
                value = input("Enter number (0–999): ")
                while not value.isdigit() or not (0 <= int(value) <= 999):
                    print("Invalid input. Please enter an integer between 0 and 999.")
                    value = input("Enter number (0–999): ")
                self.ACC = int(value)

            case Opcode.OUT:
                if self.ACC < 500:
                    print("ACC: "+str(self.ACC ))
                else:
                    print("ACC: OVERFLOW")

            case Opcode.BRA:
                self.PC = operand

            case Opcode.BRZ:
                if self.ACC == 0:
                    self.PC = operand

            case Opcode.BRP:
                if self.ACC < 500:
                    self.PC = operand

            case Opcode.HLT:
                self.running = False
    
    def memory_dump(self):
        print("\nMemory Dump:")
        for addr, val in enumerate(self.memory):
            print(f"{addr:02}: {val:03}")
        print("End of memory dump.\n")            


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run LMC machine code.")
    parser.add_argument("filename", help="Machine code file to execute (from 'machine_code/' directory)")
    parser.add_argument("--step", action="store_true", help="Enable step-by-step debug mode")
    parser.add_argument("--dump", action = "store_true", help="Enable output of final values in memory")
    args = parser.parse_args()

    lmc = LMC(args.filename, step=args.step, dump = args.dump)
    lmc.run()