from LMCCompiler import Compiler

def check(filename):
    with open("unittests/test_machine_code/"+filename,"r") as f:
        test_machine_code = f.read()
    with open("unittests/correct_machine_code/"+filename,"r") as f:
        correct_machine_code = f.read()
    if test_machine_code == correct_machine_code:
        return True
    return False


class TestCompiler (Compiler):
    def __init__(self, filename: str, debug: bool = False):
        self.filename = filename
        self.debug = debug
        try:
            with open(f"unittests/source_code/{self.filename}", "r") as f:
                self.instructions = []
                for line in f:
                    line = line.split("//")[0].strip().upper()  # Remove comments & uppercase
                    if line:
                        self.instructions.append(line)
        except FileNotFoundError:
            raise FileNotFoundError(f"Source file '{self.filename}' not found in 'unittests/source_code/' directory.")
        self.compiled_code = ""
        self.label_table = {}
    
    def write_output(self):
        with open(f"unittests/test_machine_code/{self.filename}", "w") as f:
            f.write(self.compiled_code)

unittest_paths = ["ADD.lmc","BRA.lmc","BRP.lmc","BRZ.lmc","LDA.lmc","STA.lmc","SUB.lmc"]
for test_path in unittest_paths:
    compiler = TestCompiler(test_path)
    compiler.compile()
    if check(test_path):
        print(test_path," was compiled correctly after comparing correct machine code with test machine code.")
    else:
        print(test_path, " was compiled incorrectly after comparing correct machine codde with test machine code.")