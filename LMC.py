from enum import Enum

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
    def __init__(self):
        self.memory = [0] * 100
        self.load_program()

    def load_program(self):
        compiled_code = "compiled_code.txt"
        with open(compiled_code, "r") as f:
            data = f.read().strip()

        instructions = [int(data[i:i+3]) for i in range(0, len(data), 3)]

        for i, instr in enumerate(instructions):
            self.memory[i] = instr

    def run(self):
        self.PC = 0
        self.ACC = 0
        self.running = True

        while self.running:
            instruction = self.memory[self.PC]
            self.PC += 1
            self.decode_execute(instruction)

    def decode_execute(self, instruction):
        if instruction in (901, 902, 0):
            opcode = Opcode(instruction)
            operand = 0
        else:
            opcode = Opcode(instruction // 100)
            operand = instruction % 100

        self.execute(opcode, operand)

    def execute(self, opcode, operand):

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
                    value = input("Enter number (0–999): ")
                self.ACC = int(value)

            case Opcode.OUT:
                print(self.ACC)

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

lmc = LMC()
lmc.run()